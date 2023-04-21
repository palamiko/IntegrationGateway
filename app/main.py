import logging.config
import random
import string
import time
from typing import Annotated

from fastapi import FastAPI, Response, status, UploadFile, Form, Request


from app.dto.request_models import Transition, Comment, Priority
from app.requests.jira_methods import transition_commit, comment_add, priority_change
from app.requests.zendesk_methods import sent_file_to_zd, attach_file
from app.util.funs import get_log_conf

app = FastAPI()


logging.config.dictConfig(get_log_conf())
logger = logging.getLogger(__name__)


@app.post('/api/v1/add/comment')
async def add_comment(comment: Comment, response: Response):
    return await comment_add(comment, response)


@app.put('/api/v1/change/transition')
async def change_status(transition: Transition, response: Response):
    try_count = 0
    result = await transition_commit(transition, response)
    if result == status.HTTP_400_BAD_REQUEST and try_count == 0:
        try_count += 1
        transition.id = 931
        await transition_commit(transition, response)
    else:
        return result


@app.put('/api/v1/change/priority')
async def change_status(priority: Priority, response: Response):
    return await priority_change(priority, response)


@app.post("/api/v1/upload/file")
async def upload_file(file: UploadFile, zd_id: Annotated[str, Form()], response: Response,
                      file_name: Annotated[str, Form()] = 'unknown'):
    upload_token = await sent_file_to_zd(file, file_name, response)
    return await attach_file(upload_token, zd_id, response)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response



