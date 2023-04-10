from pydantic import BaseModel

from app.dto.priority_enum import PriorityEnumZD


class Transition(BaseModel):
    id: str
    issue_key: str


class Comment(BaseModel):
    body: str
    issue_key: str
    author_name: str


class Priority(BaseModel):
    value: PriorityEnumZD
    issue_key: str
