from fastapi import FastAPI

from app.dto.request_models import Transition, Comment, Priority
from app.requests.jira_methods import transition_commit, comment_add, priority_change

app = FastAPI()


@app.post('/api/v1/add/comment')
async def add_comment(comment: Comment):
    return await comment_add(comment)


@app.put('/api/v1/change/transition')
async def change_status(transition: Transition):
    return await transition_commit(transition)


@app.put('/api/v1/change/priority')
async def change_status(priority: Priority):
    return await priority_change(priority)
