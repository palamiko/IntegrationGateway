import json

import aiohttp
from fastapi import status

from app.conf.config import settings
from app.dto.request_models import Transition, Comment, Priority
from app.util.funs import mapping_priority


async def transition_commit(transition: Transition):
    async with aiohttp.ClientSession(base_url=settings.url_jira,
                                     headers=settings.headers,
                                     auth=settings.jira_auth()) as session:
        async with session.post(f'/rest/api/2/issue/{transition.issue_key}/transitions',
                                data=json.dumps({"transition": {"id": transition.id}})) as rs:
            if rs.status == status.HTTP_204_NO_CONTENT:
                return status.HTTP_204_NO_CONTENT
            else:
                return rs


async def comment_add(comment: Comment):
    async with aiohttp.ClientSession(base_url=settings.url_jira,
                                     headers=settings.headers,
                                     auth=settings.jira_auth()) as session:
        async with session.post(f'/rest/api/2/issue/{comment.issue_key}/comment',
                                data=json.dumps({"body": comment.body + '\n\n' + comment.author_name})) as rs:
            if rs.status == status.HTTP_201_CREATED:
                return status.HTTP_201_CREATED
            else:
                return rs


async def priority_change(priority: Priority):
    jira_priority = mapping_priority(priority.value)
    data_load = {
        "fields": {
            "priority": {
                "name": jira_priority.value
            }
        }
    }

    async with aiohttp.ClientSession(base_url=settings.url_jira,
                                     headers=settings.headers,
                                     auth=settings.jira_auth()) as session:
        async with session.put(f'/rest/api/2/issue/{priority.issue_key}',
                               data=json.dumps(data_load)) as rs:
            if rs.status == status.HTTP_204_NO_CONTENT:
                return status.HTTP_204_NO_CONTENT
            else:
                return rs
