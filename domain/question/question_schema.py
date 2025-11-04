import datetime

from pydantic import BaseModel, field_validator
from domain.answer.answer_schema import Answer

from domain.user.user_schema import User

class Question(BaseModel):
    id: int
    board_id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []
    user: User | None
    modify_date: datetime.datetime | None = None
    voter: list[User] = []

    @field_validator("answers", mode="after")
    def print_answers(cls, v):
        v = [a for a in v if hasattr(a, "content") and a.content.strip() and a.content != 'string']
        # print([f"content: {a.content}" for a in v if hasattr(a, "content")])
        return v

class QuestionDetails(Question):
    a_total: int = 0

class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []

class QuestionUpdate(QuestionCreate):
    question_id: int


class QuestionDelete(BaseModel):
    question_id: int

class QuestionVote(BaseModel):
    question_id: int

class NoticeList(BaseModel):
    question_list: list[Question] = []