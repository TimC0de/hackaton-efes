import datetime
from typing import Optional

from pydantic import BaseModel


class WorkExperience(BaseModel):
    title: str
    company: str
    location: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    responsibilities: list[str]


class Education(BaseModel):
    institution: str
    location: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    coursework: Optional[str]


class CV(BaseModel):
    id: Optional[str] = None
    name: str
    job_position: str
    lang: Optional[str] = None
    document_url: Optional[str] = None
    phone_number: Optional[str]
    email: Optional[str]
    linkedin: Optional[str]
    summary: str
    work_experience: list[WorkExperience]
    education: list[Education]
    skills: list[str]
    certifications: Optional[list[str]]
    languages: Optional[list[str]]
    volunteer_work: Optional[str]
    created_at: datetime.datetime = datetime.datetime.now()
