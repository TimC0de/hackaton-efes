from datetime import datetime
import dateparser
from dateutil.relativedelta import relativedelta

from app.core.mongodb.models.cv import CV, WorkExperience, Education


def parse_date(date_str):
    if not date_str:
        return datetime.now()
    # Handle the case where 'present' is given
    if date_str.lower() == "present":
        return datetime.now()  # Return the current date and time
    else:
        # Use dateparser to parse other dates
        parsed_date = dateparser.parse(date_str)
        if not parsed_date:
            return datetime.now()
        return parsed_date


def work_experience_represent(work_experience: WorkExperience) -> str:
    return (
        f"{work_experience.title}. "
        f"{work_experience.company}. "
        f"{work_experience.location}. "
        f"{relativedelta(parse_date(work_experience.end_date), parse_date(work_experience.start_date)).years}. "
        f"{'; '.join(work_experience.responsibilities)}. "
    )


def education_represent(education: Education) -> str:
    return (
        f"{education.institution}. "
        f"{education.location}. "
        f"{relativedelta(parse_date(education.end_date), parse_date(education.start_date)).years}. "
        f"{education.coursework or ""}. "
    )


def cv_represent(cv: CV) -> str:
    return (
        f"{cv.job_position}. "
        f"{cv.summary}. "
        f"{'; '.join([work_experience_represent(work_experience) for work_experience in cv.work_experience])}. "
        f"{'; '.join([education_represent(education) for education in cv.education])}. "
        f"{'; '.join(cv.skills)}. "
        f"{'; '.join(cv.certifications) if cv.certifications else ''}. "
    )