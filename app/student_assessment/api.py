import shutil
from typing import List
from fastapi import File, HTTPException, UploadFile
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.auth import JWTBearer
from app.models import Options, Question, QuestionType, Subject, Years
from app.student_assessment.basemodel import (
    CreateQuestionTypeRequest,
    CreateSubjectPaperRequest,
    CreateSubjectRequest,
    OptionCreate,
    QuestionCreate,
    QuestionsRequest,
    SubjectYearsRequest,
)
from database import get_db
from starlette import status


router = APIRouter(prefix="/mcq")


@router.post("/subjects")
async def create_subject(
    subject_request: CreateSubjectRequest,
    db: Session = Depends(get_db),
    user_data: dict = Depends(JWTBearer()),
):
    try:
        subject = Subject(subject_name=subject_request.subject_name, created_by_id=1)
        db.add(subject)
        db.commit()
        return {"Message": "Subject Added Successfully"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}


@router.post(
    "/question_type",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(JWTBearer)],
)
async def create_question_type(
    question_type_request: CreateQuestionTypeRequest,
    db: Session = Depends(get_db),
    user_data: dict = Depends(JWTBearer()),
):
    try:
        question_type = QuestionType(
            name=question_type_request.question_type, created_by_id=1
        )
        db.add(question_type)
        db.commit()
        return {"Message": "Question Type Added Successfully"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}


@router.post(
    "/subjects_paper",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(JWTBearer)],
)
async def create_subject(
    subject_paper_request: CreateSubjectPaperRequest,
    db: Session = Depends(get_db),
    user_data: dict = Depends(JWTBearer()),
):
    try:
        subject = (
            db.query(Subject)
            .filter(Subject.subject_id == subject_paper_request.subjects_id)
            .first()
        )
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Subject does not exist"
            )
        subject_year = Years(
            year_number=subject_paper_request.subject_year,
            created_by_id=1,
            assessment_specification=subject_paper_request.assessment_name,
            subject_id=subject_paper_request.subjects_id,
        )
        db.add(subject_year)
        db.commit()
        return {"Message": "Subject Year Added Successfully"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}


@router.post(
    "/questions", status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer)]
)
async def create_question(
    question_create: QuestionCreate,
    db: Session = Depends(get_db),
    user_data: dict = Depends(JWTBearer()),
):
    try:
        subject = (
            db.query(Subject)
            .filter(Subject.subject_id == question_create.subject_id)
            .first()
        )
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Subject does not exist"
            )
        year = db.query(Years).filter(Years.year_id == question_create.year_id).first()
        if not year:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Year does not exist"
            )

        question = Question(
            subject_id=question_create.subject_id,
            year_id=question_create.year_id,
            question_text=question_create.question_text,
            created_by_id=1,
        )
        db.add(question)
        db.commit()
        db.refresh(question)
        return {"Message": "Question added successfully", "data": question}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post(
    "/options", status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer)]
)
async def create_options(
    option_create: OptionCreate,
    db: Session = Depends(get_db),
    user_data: dict = Depends(JWTBearer()),
):
    try:
        quesion = (
            db.query(Question)
            .filter(Question.question_id == option_create.question_id)
            .first()
        )
        if not quesion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Questions does not exist"
            )

        options = Options(
            question_id=option_create.question_id,
            option_value=option_create.option_value,
            feedback=option_create.feedback,
            is_correct=option_create.is_correct,
            created_by_id=1,
        )
        db.add(options)
        db.commit()
        db.refresh(options)
        return {"Message": "Options added successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    # @router.get("/questions/get")
    # def get_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return questions


@router.get("/subjects/paper", dependencies=[Depends(JWTBearer)])
async def get_subject_years(
    subject_years_request: SubjectYearsRequest,
    db: Session = Depends(get_db),
    user_data: dict = Depends(JWTBearer()),
):
    try:
        subject_years = (
            db.query(Years)
            .filter(Years.subject_id == subject_years_request.subject_id)
            .all()
        )
        if not subject_years:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No papers found for this subject",
            )
        return subject_years
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/question_options", dependencies=[Depends(JWTBearer)])
def get_questions_by_year_and_subject(
    questions_request: QuestionsRequest,
    db: Session = Depends(get_db),
    user_data: dict = Depends(JWTBearer()),
):
    try:
        questions_with_options = []
        questions = (
            db.query(Question)
            .filter(
                Question.year_id == questions_request.year_id,
                Question.subject_id == questions_request.subject_id,
            )
            .all()
        )
        if not questions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Years not found"
            )

        for question in questions:
            options = (
                db.query(Options)
                .filter(Options.question_id == question.question_id)
                .all()
            )
            options_list = []
            for option in options:
                options_list.append(
                    {
                        "option_id": option.option_id,
                        "option_value": option.option_value,
                        "feedback": option.feedback,
                        "is_correct": option.is_correct,
                    }
                )
            questions_with_options.append(
                {
                    "question_id": question.question_id,
                    "question_text": question.question_text,
                    "options": options_list,
                }
            )

        return questions_with_options
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/upload/", dependencies=[Depends(JWTBearer)])
async def upload_file(
    file: UploadFile = File(...),
    user_data: dict = Depends(JWTBearer()),
):
    try:
        with open(f"uploads/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return JSONResponse(content={"message": "File uploaded successfully"})
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"error": f"Error uploading file: {e}"}
        )
