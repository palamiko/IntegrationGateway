import json
import logging

import aiohttp
from fastapi import status, Response

from app.conf.config import settings
from app.dto.request_models import Transition, Comment, Priority
from app.util.const import ERROR_MESSAGE, HEADERS
from app.util.funs import mapping_priority

logger = logging.getLogger(__name__)


async def transition_commit(transition: Transition, response: Response):
    """ Ф-ия отправляет запрос для изменения статуса тикета """

    try:
        async with aiohttp.ClientSession(headers=HEADERS, auth=settings.jira_auth()) as session:
            async with session.post(url=f'{settings.jira_url}/rest/api/2/issue/{transition.issue_key}/transitions',
                                    data=json.dumps({"transition": {"id": transition.id}})) as rs:
                logger.info(f'{rs.request_info.url} {rs.status}')
                logger.debug(f'status {rs.status}' + await rs.text())

                if rs.status == status.HTTP_204_NO_CONTENT:
                    response.status_code = status.HTTP_204_NO_CONTENT
                elif ERROR_MESSAGE in await rs.text():
                    return status.HTTP_400_BAD_REQUEST
                else:
                    response.status_code = rs.status
                    return dict(await rs.json())

    except aiohttp.ClientOSError as ex:
        logger.exception(f'status {rs.status}' + await rs.text(), exc_info=ex)
        response.status_code = rs.status
        return dict(await rs.json())


async def comment_add(comment: Comment, response: Response):
    """ Ф-ия отправляет запрос для добавления комментария """
    try:

        async with aiohttp.ClientSession(headers=HEADERS, auth=settings.jira_auth()) as session:
            async with session.post(url=f'{settings.jira_url}/rest/api/2/issue/{comment.issue_key}/comment',
                                    data=json.dumps({"body": comment.body + '\n\n' + comment.author_name})) as rs:
                logger.info(f'{rs.request_info.url} {rs.status}')
                logger.debug(f'status {rs.status}' + await rs.text())

                if rs.status == status.HTTP_201_CREATED:
                    response.status_code = status.HTTP_204_NO_CONTENT
                else:
                    response.status_code = rs.status
                    return dict(await rs.json())

    except aiohttp.ClientOSError as ex:
        logger.exception(f'status {rs.status}' + await rs.text(), exc_info=ex)
        response.status_code = rs.status
        return dict(await rs.json())


async def priority_change(priority: Priority, response: Response):
    """ Ф-ия отправляет запрос для изменения приоритета тикета """

    jira_priority = mapping_priority(priority.value)
    data_load = {
        "fields": {
            "priority": {
                "name": jira_priority.value
            }
        }
    }
    try:
        async with aiohttp.ClientSession(headers=HEADERS, auth=settings.jira_auth()) as session:
            async with session.put(url=f'{settings.jira_url}/rest/api/2/issue/{priority.issue_key}',
                                   data=json.dumps(data_load)) as rs:
                logger.info(f'{rs.request_info.url} {rs.status}')
                logger.debug(f'status {rs.status}' + await rs.text())

                if rs.status == status.HTTP_204_NO_CONTENT:
                    response.status_code = status.HTTP_204_NO_CONTENT
                else:
                    response.status_code = rs.status
                    return dict(await rs.json())

    except aiohttp.ClientOSError as ex:
        logger.exception(f'status {rs.status}' + await rs.text(), exc_info=ex)
        response.status_code = rs.status
        return dict(await rs.json())
