import typing as _typing
import datetime as _dt

from pydantic import BaseModel as _BM, Field as _Field


"""
pydantic - структуры, используемые в приложении

"""

#
#
#
# Пользовательские типы
#
#
#

users_roles = _typing.Literal["student", "teacher"]

mark_values = _typing.Literal[None, 2, 3, 4, 5]

link_actions = _typing.Literal[
    "join chat",
    "join group",
    "verify email"
]

contacts_types = _typing.Literal[
    "phone",
    "address",
    "email",
    "site",
    "vk",
    "ok",
    "telegram",
]

email_templates = _typing.Literal[
    "verify_email",
    "create_company_promise",
    "create_company_reject",
    "create_company_success",
    "update_company_promice",
    "update_company_reject",
    "update_company_success",
    "delete_company_promise",
    "delete_company_reject",
    "delete_company_success",
    "create_tags_promise",
    "create_tags_success",
    "create_tags_reject",
]

static_logos = _typing.Literal["logo.png", "alter-logo.png"]

static_templates = _typing.Literal[
    "link_expired",
    "link_invalid",
    "link_overused",
    "link_join_useless",
    "verify_email_success",
    "account_not_activated",
    "internal_server_error"
]

companies_sort_types = _typing.Literal["id", "name"]

allowed_image_extensions = _typing.Literal["png", "jpeg", "jpg"]


class _Base(_BM):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


#
#
#
# структуры, связанные с базой данных
#
#
#


class _User(_Base):

    id: int
    email: str
    fname: str
    lname: str
    sname: _typing.Optional[str] = _Field(default="")
    date_online: _dt.datetime


class Student(_User):
    pass


class StudentUpdate(_Base):

    confirmation_password: str
    confirmation_email: str
    password: _typing.Optional[str]
    fname: _typing.Optional[str]
    lname: _typing.Optional[str]
    sname: _typing.Optional[str]


class Teacher(_User):

    company: str
    specializations: _typing.List[str]
    bio: _typing.Optional[str] = _Field(default="")


class SqlUser(_User):

    role: users_roles
    password: str
    date_created: _dt.datetime


class StudentCreate(_Base):

    email: str
    fname: str
    lname: str
    sname: _typing.Optional[str] = _Field(default="")
    password: str


class TeacherCreate(_Base):

    email: str
    fname: str
    lname: str
    sname: _typing.Optional[str] = _Field(default="")
    company: int
    specializations: _typing.List[str]
    bio: _typing.Optional[str] = _Field(default="")
    password: str


class TeacherUpdate(_Base):

    confirmation_password: str
    confirmation_email: str
    password: _typing.Optional[str]
    email: _typing.Optional[str]
    fname: _typing.Optional[str]
    lname: _typing.Optional[str]
    sname: _typing.Optional[str]
    company:  _typing.Optional[int]
    specializations: _typing.Optional[_typing.List[str]]
    bio: _typing.Optional[str]


class StudentShort(_Base):

    id: int
    fname: str
    lname: str


class TeacherShort(_Base):

    id: int
    fname: str
    lname: str
    sname: _typing.Optional[str] = _Field(default="")
    company: str


class _UserFull(_Base):

    activities: _typing.List[_dt.datetime]


class StudentFull(Student, _UserFull):
    pass


class TeacherFull(Teacher, _UserFull):
    pass


class CompanyContact(_Base):

    id: int
    kind: contacts_types
    value: str


class CompanyContactCreate(_Base):

    kind: contacts_types
    value: str


class Company(_Base):

    id: int
    name: str
    teachers: _typing.List[Teacher]
    tags: _typing.List[str]
    contacts: _typing.List[CompanyContact]


class Specialization(_Base):

    id: int
    name: str


class CompanyCreate(_Base):

    name: str
    tags: _typing.List[str]
    contacts: _typing.List[CompanyContactCreate]


class CompanyUpdate(_Base):

    name: _typing.Optional[str]
    tags: _typing.Optional[_typing.List[str]]
    contacts: _typing.Optional[_typing.List[CompanyContactCreate]]


class LessonShort(_Base):

    id: int
    number: int
    name: str


class Course(_Base):

    id: int
    name: str
    description: str
    author: _typing.Union[StudentShort, TeacherShort]
    date_created: _dt.date
    date_updated: _typing.Optional[_dt.date] = None
    views: int = _Field(default=1)
    tags: _typing.List[Specialization]
    lessons: _typing.List[LessonShort]


class CourseShort(_Base):

    id: int
    name: str


class CourseCreate(_Base):

    name: str
    description: str
    author_id: int
    tags: _typing.List[str]


class CourseUpdate(_Base):

    name: _typing.Optional[str]
    description: _typing.Optional[str]
    tags: _typing.Optional[_typing.List[str]]


class SqlLesson(_Base):

    id: int
    number: int
    name: str
    description: str
    duration: _dt.time


class Step(_Base):

    title: str
    text: str
    media_src: str


class LessonFull(SqlLesson):

    steps: _typing.List[str]


class LessonCreate(_Base):

    number: int
    name: str
    description: str
    duration: _dt.time


class LessonUpdate(_Base):

    name: _typing.Optional[str]
    description: _typing.Optional[str]
    duration: _typing.Optional[_dt.time]


class CourseFull(Course):

    lessons: _typing.List[LessonShort]
    duration: _dt.time


class Group(_Base):

    id: int
    name: str
    teacher: Teacher
    students: _typing.List[Student]


class GroupCreate(_Base):

    name: str
    teacher: int
    students: _typing.List[int]


class Session(_Base):

    course: CourseShort
    date_started: _dt.datetime
    date_endend: _typing.Optional[_dt.datetime] = None
    active: bool


class GroupSession(Session):

    group: Group


class IndividualSession(Session):

    student: StudentShort


class Hometask(_Base):

    id: int
    description: str
    session: GroupSession
    student: StudentShort
    date_given: _dt.datetime
    date_done: _typing.Optional[_dt.datetime] = None
    deadline: _dt.datetime
    mark: mark_values


class HometaskCreate(_Base):

    description: str
    teacher: int
    students: _typing.List[int]
    deadline: _dt.datetime


class Progress(_Base):

    student: StudentShort
    course: CourseShort
    lesson: int
    step: int
    percent: float


class Chat(_Base):

    id: int
    date_created: _dt.datetime
    name: _typing.Optional[str] = None
    members: _typing.List[StudentShort]


class ChatCreate(_Base):

    name: _typing.Optional[str] = None
    members: _typing.List[int]


class Message(_Base):

    sender: int
    date: _dt.datetime
    text: _typing.Optional[str] = None
    image: _typing.Optional[str] = None


class Admin(_Base):

    login: str
    password: str


class Link(_Base):

    url: str
    action: link_actions
    date_expired:  _typing.Optional[_dt.datetime]
    limit: _typing.Optional[int] = None
    target: int
    count_used: int


class CreateLink(_Base):

    action: link_actions
    limit: _typing.Optional[int] = None
    ttl: _typing.Optional[_dt.time] = None
    target: int


class Notification(_Base):

    id: int
    title: str
    description: _typing.Optional[str] = None
    url: _typing.Optional[str] = None
    date: _dt.datetime


class CreateNotification(_Base):

    title: str
    description: _typing.Optional[str] = None
    date: _dt.datetime


class AuthSchema(_Base):

    login: str
    password: str


#
#
#
#  структуры заявок
#
#
#


class _ApplicationBase(_Base):

    applicant_email: str
    reason: _typing.Optional[str]


class _JsonApplicationBase(_ApplicationBase):

    id: int
    date: _dt.datetime


class _TagApplicationBase(_ApplicationBase):

    names: _typing.List[str]


class CreateTagApplicationCreate(_TagApplicationBase):
    pass


class CreateTagApplication(_TagApplicationBase, _JsonApplicationBase):
    pass


class CreateCompanyApplicationCreate(CompanyCreate, _ApplicationBase):
    pass


class CreateCompanyApplication(CompanyCreate, _JsonApplicationBase):
    pass


class DeleteCompanyApplicationCreate(_ApplicationBase):

    company_id: str
    reason: str


class DeleteCompanyApplication(_JsonApplicationBase):

    company_id: str
    reason: str


class UpdateCompanyApplicationCreate(CompanyUpdate, _ApplicationBase):
    pass


class UpdateCompanyApplication(CompanyUpdate, _JsonApplicationBase):
    pass


class AllCompanyApplications(_Base):

    create: _typing.List[CreateCompanyApplication]
    update: _typing.List[UpdateCompanyApplication]
    delete: _typing.List[DeleteCompanyApplication]


class AllApplications(_Base):

    tags: _typing.List[CreateTagApplication]
    companies: AllCompanyApplications


class ApplicationDecision(_Base):

    apply: bool
    reason: _typing.Optional[str] = _Field(default="")


class StepText(_Base):

    text: str
