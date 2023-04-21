import json
import logging
from typing import Any

import aiohttp
from fastapi import UploadFile, status
from fastapi.openapi.models import Response

from app.conf.config import settings
from app.requests.jira_methods import logger
from app.util.const import HEADERS


async def sent_file_to_zd(file: UploadFile, name, response: Response) -> dict[Any, Any] | str:
    params = {'filename': name}
    headers = {'Content-Type': file.content_type}

    try:
        async with aiohttp.ClientSession(headers=headers, auth=settings.zd_auth()) as session:
            async with session.post(url=f'{settings.zendesk_url}/api/v2/uploads.json',
                                    data=file.file,
                                    params=params) as rs:
                logger.info(f'{rs.request_info.url} {rs.status}')
                logger.debug(f'status {rs.status}' + await rs.text())

                if rs.status == status.HTTP_201_CREATED:
                    rs_json = json.loads(await rs.text())
                    upload_token = rs_json['upload']['token']
                    return upload_token
                else:
                    response.status_code = rs.status
                    logging.error(f'status {rs.status}' + await rs.text())
    except aiohttp.ClientOSError as ex:
        logger.exception(f'status {rs.status}' + await rs.text(), exc_info=ex)
        response.status_code = rs.status
        return dict(await rs.json())


async def attach_file(upload_token: str, zd_id: str, response: Response):
    try:
        async with aiohttp.ClientSession(auth=settings.zd_auth(), headers=HEADERS) as session:
            payload = {
                'ticket': {
                    'comment': {
                        'body': 'Добавлен файл',
                        'uploads': [upload_token]
                    }
                }
            }
            async with session.put(url=f'{settings.zendesk_url}/api/v2/tickets/{zd_id}',
                                   data=json.dumps(payload)) as rs:
                logger.info(f'{rs.request_info.url} {rs.status}')
                logger.debug(f'status {rs.status}' + await rs.text())

                if rs.status == status.HTTP_200_OK:
                    response.status_code = status.HTTP_200_OK
                else:
                    logging.error(f'status {rs.status}' + await rs.text())
                    response.status_code = rs.status
    except aiohttp.ClientOSError as ex:
        logger.exception(f'status {rs.status}' + await rs.text(), exc_info=ex)
        response.status_code = rs.status
        return dict(await rs.json())
