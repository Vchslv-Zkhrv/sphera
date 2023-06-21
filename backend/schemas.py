import typing as _typing
import datetime as _dt

from pydantic import BaseModel as _BM, Field as _Field


users_roles = _typing.Literal["student", "teacher"]
mark_values = _typing.Literal[None, 2, 3, 4, 5]
link_actions = _typing.Literal[
    "join chat",
    "join group"
]


class _Base(_BM):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


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
    email: _typing.Optional[str]
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
    passowrd: str


class StudentShort(_Base):

    id: int
    fname: str
    lname: str


class TeacherShort(_Base):

    id: int
    fname: str
    lname: str
    sname: _typing.Optional[str] = _Field(default="")
    company: int


class _UserFull(_Base):

    activities: _typing.List[int]


class StudentFull(Student, _UserFull):
    pass


class TeacherFull(Teacher, _UserFull):
    pass


class Company(_Base):

    id: int
    name: str


class Specialization(_Base):

    id: int
    name: str


class CompanyCreate(_Base):

    name: str
    specializations: _typing.List[str]


class Course(_Base):

    id: int
    name: str
    description: str
    author: _User
    date_created: _dt.datetime
    date_updated: _typing.Optional[_dt.datetime] = None
    views: int = _Field(default=1)
    tags: _typing.List[Specialization]


class CourseShort(_Base):

    id: int
    name: str


class CourseCreate(_Base):

    name: str
    description: str
    author_id: int
    tags: _typing.List[str]


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


class LessonShort(_Base):

    id: int
    number: int
    name: str


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
