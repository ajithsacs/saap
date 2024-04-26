from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    text,
)
from database import Base


# The `Subject` class defines a database table for storing information about subjects, including
# subject ID, name, creation and update timestamps, deletion status, record status, and
# creator/updater IDs.
# The `Subject` class represents a database table for storing information about subjects, including
# subject ID, name, creation and update timestamps, deletion status, record status, and
# creator/updater IDs.
class Subject(Base):
    __tablename__ = "subject"

    subject_id = Column(Integer, primary_key=True, index=True, nullable=False)
    subject_name = Column(String(255), index=True, nullable=False)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    deleted = Column(SmallInteger, nullable=False, server_default=text("0"))
    record_status = Column(SmallInteger, nullable=False, server_default=text("1"))
    created_by_id = Column(Integer, nullable=False)
    updated_by_id = Column(Integer)


class Years(Base):
    __tablename__ = "subject_years"

    year_id = Column(Integer, primary_key=True, index=True, nullable=False)
    year_number = Column(Integer, nullable=False)
    assessment_specification = Column(String(255), nullable=False)
    subject_id = Column(Integer, ForeignKey("subject.subject_id"), nullable=False)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    deleted = Column(SmallInteger, nullable=False, server_default=text("0"))
    record_status = Column(SmallInteger, nullable=False, server_default=text("1"))
    created_by_id = Column(Integer, nullable=False)
    updated_by_id = Column(Integer)


class Question(Base):
    __tablename__ = "questions_table"

    question_id = Column(Integer, primary_key=True, index=True, nullable=False)
    subject_id = Column(Integer, ForeignKey("subject.subject_id"), nullable=False)
    year_id = Column(Integer, ForeignKey("subject_years.year_id"), nullable=False)
    question_text = Column(Text, nullable=False)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    deleted = Column(SmallInteger, nullable=False, server_default=text("0"))
    record_status = Column(SmallInteger, nullable=False, server_default=text("1"))
    created_by_id = Column(Integer, nullable=False)
    updated_by_id = Column(Integer)


class Options(Base):
    __tablename__ = "options_table"

    option_id = Column(Integer, primary_key=True, index=True, nullable=False)
    question_id = Column(
        Integer, ForeignKey("questions_table.question_id"), nullable=False
    )
    option_value = Column(Text, nullable=False)
    feedback = Column(Text, nullable=False)
    is_correct = Column(SmallInteger, nullable=False)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    deleted = Column(SmallInteger, nullable=False, server_default=text("0"))
    record_status = Column(SmallInteger, nullable=False, server_default=text("1"))
    created_by_id = Column(Integer, nullable=False)
    updated_by_id = Column(Integer)


class QuestionType(Base):
    __tablename__ = "question_type"

    question_type_id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(Text, nullable=False)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    deleted = Column(SmallInteger, nullable=False, server_default=text("0"))
    record_status = Column(SmallInteger, nullable=False, server_default=text("1"))
    created_by_id = Column(Integer, nullable=False)
    updated_by_id = Column(Integer)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    google_id = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    deleted = Column(SmallInteger, nullable=False, server_default=text("0"))
    record_status = Column(SmallInteger, nullable=False, server_default=text("1"))
    created_by_id = Column(Integer, nullable=False)
    updated_by_id = Column(Integer)
