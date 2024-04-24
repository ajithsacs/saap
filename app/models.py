from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String, Text,text

from database import Base

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(50), index=True)  # Specify the length here
    description = Column(String(255), index=True)  # Specify the length here


class Subject(Base):
    __tablename__ = "subject"

    subject_id = Column(Integer, primary_key=True, index=True, nullable=False)
    subject_name =Column(String(255),index=True,nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    deleted = Column(SmallInteger, nullable=False, server_default=text("0"))
    record_status = Column(SmallInteger, nullable=False, server_default=text("1"))
    created_by_id = Column(Integer, nullable=False)
    updated_by_id = Column(Integer)

# class Years(Base):
#     __tablename__= "years"

#     year_id = Column(Integer, primary_key=True, index=True, nullable=False)
#     year_number =Column(Integer,nullable=False)
#     created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
#     updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
#     deleted = Column(SmallInteger, nullable=False, server_default=text("0"))
#     record_status = Column(SmallInteger, nullable=False, server_default=text("1"))
#     created_by_id = Column(Integer, nullable=False)
#     updated_by_id = Column(Integer)



# class Question(Base):
#     __tablename__ = "questions"

#     question_id = Column(Integer, primary_key=True, index=True, nullable=False)
#     subject_id = Column(Integer, ForeignKey("subject.subject_id"),nullable=False)
#     year_id = Column(Integer, ForeignKey("years.year_id"),nullable=False)
#     question_text = Column(Text,nullable=False)
#     created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
#     updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
#     deleted = Column(SmallInteger, nullable=False, server_default=text("0"))
#     record_status = Column(SmallInteger, nullable=False, server_default=text("1"))
#     created_by_id = Column(Integer, nullable=False)
#     updated_by_id = Column(Integer)
