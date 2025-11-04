from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from database import get_db
# from database import SessionLocal
from domain.question import question_schema,question_crud
# from models import Question
from starlette import status
from domain.user.user_router import get_current_user
from models import User, Question

router = APIRouter(
    prefix="/api/question", #공통 하위 주소
)

@router.get("/list/{board_id}", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10, keyword: str = '',board_id:int=1):
    total, _question_list = question_crud.get_question_list(
        db, skip=page*size, limit=size,keyword=keyword,board_id=board_id)
    print(f"게시판 번호 : {board_id}")
    return {
        'total': total,
        'question_list': _question_list
    }



# @router.get("/detail/{question_id}", response_model=question_schema.Question)
# def question_detail(question_id: int, db: Session = Depends(get_db)):
#     question = question_crud.get_question(db, question_id=question_id)
#     return question

@router.get("/detail/{question_id}", response_model=question_schema.QuestionDetails)
def question_detail(question_id: int,page: int = 0, size : int =10, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id,skip=page*size, limit=size)
    print(f"질문 갯수 : {page}")
    return question

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT) #204는 응답없을을 뜻한다
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    question_crud.create_question(db=db, question_create=_question_create,user=current_user)


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    question_crud.update_question(db=db, db_question=db_question,
                                  question_update=_question_update)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    question_crud.delete_question(db=db, db_question=db_question)

@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote: question_schema.QuestionVote,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    question_crud.vote_question(db, db_question=db_question, db_user=current_user)

@router.get("/notice", response_model=question_schema.NoticeList)
def notice_list(db: Session = Depends(get_db)):
    db_notice  = question_crud.get_notice(db)
    return db_notice
