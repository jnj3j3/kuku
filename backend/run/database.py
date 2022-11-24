from option import *
from sqlalchemy.orm import Session, joinedload
import sqlalchemy
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from utils.exception import *
from datetime import datetime


class code_jobs(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    language: str
    code: str

    status: str
    status_updated: datetime = Field(default=datetime.now())

    output: Optional[str]
    last_read_line: Optional[int]

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.language = kwargs.get("language", None)
        self.code = kwargs.get("code", None)
        self.status = kwargs.get("status", None)
        self.status_updated = kwargs.get("status_updated", None)
        self.output = kwargs.get("output", None)
        self.last_read_line = kwargs.get("last_read_line", None)


def create_run_requst(form: code_jobs, session: Session) -> Result[int, str]:
    try:
        session.add(form)
        session.commit()
        session.refresh(form)
        return Ok(form.id)
    except Exception as e:
        return Err(str(e))


def get_run_requst(run_id: int, session: Session) -> Result[code_jobs, str]:
    try:
        run = (
            session.query(
                code_jobs.status,
                code_jobs.status_updated,
                code_jobs.output,
                code_jobs.last_read_line,
            )
            .filter(code_jobs.id == run_id)
            .first()
        )
        print(run)
        return Ok(run)
    except Exception as e:
        return Err(str(e))


def update_run_request_last_read_line(
    run_id: int, last_read_line: int, session: Session
) -> Result[code_jobs, str]:
    try:
        run = session.select(code_jobs).filter(code_jobs.id == run_id).first()
        run.last_read_line = last_read_line
        session.commit()
        return Ok(run)
    except Exception as e:
        return Err(str(e))
