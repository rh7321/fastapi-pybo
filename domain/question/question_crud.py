from datetime import datetime
from domain.question.question_schema import QuestionCreate, QuestionUpdate
from sqlalchemy import and_

from models import Question, User, Answer
from sqlalchemy.orm import Session


def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = '',board_id:int=1):
    question_list = db.query(Question)
    if keyword:
        search = '%%{}%%'.format(keyword)
        sub_query = db.query(Answer.question_id, Answer.content, User.username) \
            .outerjoin(User, and_(Answer.user_id == User.id)).subquery()
        question_list = question_list \
            .outerjoin(User) \
            .outerjoin(sub_query, and_(sub_query.c.question_id == Question.id)) \
            .filter(Question  .subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    )

    total = question_list.distinct().count()

    question_list = question_list.order_by(Question.create_date.desc()).filter(Question.board_id == board_id) \
        .offset(skip).limit(limit).distinct().all()
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)


def get_question(db: Session, question_id: int,skip: int = 0, limit: int = 10):
    question = db.query(Question).get(question_id)
    question.a_total = len([a for a in question.answers if a.content != ''])
    answer = db.query(Answer).filter(Answer.question_id == question_id,Answer.content != '',
                                     Answer.content !='string').offset(skip).limit(limit).all()
    question.answers = answer
    return question


def create_question(db: Session, question_create: QuestionCreate, user: User):
    # user = db.merge(user) # 다른 세션에서 가져온 user를 현재 세션으로 동기화
    db_question = Question(subject=question_create.subject,
                           content=question_create.content,board_id=question_create.board_id,
                           create_date=datetime.now(),user=user)
    print(f"유저처리 되나? : {user.id}")
    db.add(db_question)
    db.commit()


def update_question(db: Session, db_question: Question,
                    question_update: QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()
    db.add(db_question)
    db.commit()


def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()


def vote_question(db: Session, db_question: Question, db_user: User):
    db_question.voter.append(db_user)
    db.commit()


def get_notice(db: Session):
    notice_list = db.query(Question)
    notice_list = notice_list.order_by(Question.create_date.desc()).filter(Question.board_id == 2).all()
    return notice_list

