import json
import logging
from typing import Any

import aiohttp
from fastapi import status, Response, UploadFile

from app.conf.config import settings, ERROR_MESSAGE
from app.dto.request_models import Transition, Comment, Priority
from app.util.funs import mapping_priority


async def transition_commit(transition: Transition, response: Response):
    try:
        async with aiohttp.ClientSession(base_url=settings.jira_url,
                                         headers=settings.headers,
                                         auth=settings.jira_auth()) as session:
            async with session.post(f'/rest/api/2/issue/{transition.issue_key}/transitions',
                                    data=json.dumps({"transition": {"id": transition.id}})) as rs:
                if rs.status == status.HTTP_204_NO_CONTENT:
                    response.status_code = status.HTTP_204_NO_CONTENT
                elif ERROR_MESSAGE in await rs.text():
                    return status.HTTP_400_BAD_REQUEST
                else:
                    response.status_code = rs.status
                    return dict(await rs.json())

    except aiohttp.ClientOSError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


async def comment_add(comment: Comment, response: Response):
    async with aiohttp.ClientSession(base_url=settings.jira_url,
                                     headers=settings.headers,
                                     auth=settings.jira_auth()) as session:
        async with session.post(f'/rest/api/2/issue/{comment.issue_key}/comment',
                                data=json.dumps({"body": comment.body + '\n\n' + comment.author_name})) as rs:
            if rs.status == status.HTTP_201_CREATED:
                response.status_code = status.HTTP_204_NO_CONTENT
            else:
                response.status_code = rs.status
                return dict(await rs.json())


async def priority_change(priority: Priority, response: Response):
    jira_priority = mapping_priority(priority.value)
    data_load = {
        "fields": {
            "priority": {
                "name": jira_priority.value
            }
        }
    }

    async with aiohttp.ClientSession(base_url=settings.jira_url,
                                     headers=settings.headers,
                                     auth=settings.jira_auth()) as session:
        async with session.put(f'/rest/api/2/issue/{priority.issue_key}',
                               data=json.dumps(data_load)) as rs:
            if rs.status == status.HTTP_204_NO_CONTENT:
                response.status_code = status.HTTP_204_NO_CONTENT
            else:
                response.status_code = rs.status
                return dict(await rs.json())


async def sent_file_to_zd(file: UploadFile, name, response: Response) -> dict[Any, Any] | str:
    params = {'filename': name}
    headers = {'Content-Type': file.content_type}

    try:
        async with aiohttp.ClientSession(base_url=settings.zendesk_url,
                                         headers=headers,
                                         auth=settings.zd_auth()) as session:
            async with session.post('/api/v2/uploads.json', data=file.file, params=params) as rs:
                if rs.status == status.HTTP_201_CREATED:
                    rs_json = json.loads(await rs.text())
                    upload_token = rs_json['upload']['token']
                    return upload_token
                else:
                    response.status_code = rs.status
                    logging.debug('')
    except aiohttp.ClientOSError:
        response.status_code = rs.status
        return dict(await rs.json())


async def attach_file(upload_token: str, zd_id: str, response: Response):
    try:
        async with aiohttp.ClientSession(base_url=settings.zendesk_url,
                                         auth=settings.zd_auth(),
                                         headers=settings.headers) as session:
            payload = {
                'ticket': {
                    'comment': {
                        'body': 'Добавлен файл',
                        'uploads': [upload_token]
                    }
                }
            }
            async with session.put(f'/api/v2/tickets/{zd_id}', data=json.dumps(payload)) as rs:
                if rs.status == status.HTTP_200_OK:
                    response.status_code = status.HTTP_200_OK
                else:
                    response.status_code = rs.status
    except aiohttp.ClientOSError:
        response.status_code = rs.status
        return dict(await rs.json())

