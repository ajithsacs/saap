from pydantic import BaseModel


class QuestionsRequest(BaseModel):
    year_id: int
    subject_id: int

class SubjectYearsRequest(BaseModel):
    subject_id: int

class OptionCreate(BaseModel):
    question_id: int
    option_value: str
    feedback: str
    is_correct: int

class QuestionCreate(BaseModel):
    subject_id: int
    year_id: int
    question_text: str

class CreateSubjectPaperRequest(BaseModel):
    subject_year: int
    assessment_name: str
    subjects_id: int

class CreateQuestionTypeRequest(BaseModel):
    question_type: str

class CreateSubjectRequest(BaseModel):
    subject_name: str

class SubjectIdRequest(BaseModel):
    subject_id: int