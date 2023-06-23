import typing as _typing

import sqlalchemy as _sql
import sqlalchemy.orm as _orm

import database as _db


"""
Определение базы данных

"""


class User(_db.Base):

    __tablename__ = "user"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    role = _sql.Column(_sql.String, nullable=False, default="student")
    email = _sql.Column(_sql.String, unique=True, index=True)
    password = _sql.Column(_sql.String, nullable=False)
    fname = _sql.Column(_sql.String, nullable=False)
    lname = _sql.Column(_sql.String, nullable=False)
    sname = _sql.Column(_sql.String, nullable=True)
    date_created = _sql.Column(_sql.DateTime)
    date_online = _sql.Column(_sql.DateTime)
    sign = _sql.Column(_sql.String, nullable=False)
    telegram = _sql.Column(_sql.Integer, nullable=True, index=True)
    confirmed = _sql.Column(_sql.Boolean, nullable=False, index=True, default=False)

    groups: _orm.Mapped[_typing.List["GroupStudents"]] = \
        _orm.relationship(back_populates="student")

    sessions: _orm.Mapped[_typing.List["IndividualSessions"]] = \
        _orm.relationship(back_populates="user")

    hometasks: _orm.Mapped[_typing.List["Hometask"]] = \
        _orm.relationship(back_populates="student")

    progresses: _orm.Mapped[_typing.List["Progress"]] = \
        _orm.relationship(back_populates="student")

    chats: _orm.Mapped[_typing.List["ChatMembers"]] = \
        _orm.relationship(back_populates="member")

    activities: _orm.Mapped[_typing.List["UserActivities"]] = \
        _orm.relationship(back_populates="user")

    notifications: _orm.Mapped[_typing.List["Notification"]] = \
        _orm.relationship(back_populates="user")

    teacher: _orm.Mapped["Teacher"] = \
        _orm.relationship(back_populates="user", cascade="delete")


class UserActivities(_db.Base):

    __tablename__ = "user_activities"

    id = _sql.Column(_sql.Integer,  primary_key=True, index=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"))
    date = _sql.Column(_sql.DateTime)

    user: _orm.Mapped["User"] = \
        _orm.relationship(back_populates="activities", cascade="delete")


class Company(_db.Base):

    __tablename__ = "company"

    id = _sql.Column(_sql.Integer,  primary_key=True, index=True)
    name = _sql.Column(_sql.String, unique=True, index=True)

    specializations: _orm.Mapped[_typing.List["CompanySpecializations"]] = \
        _orm.relationship(back_populates="company")

    teachers: _orm.Mapped[_typing.List["Teacher"]] = \
        _orm.relationship(back_populates="company")

    contacts = _orm.Mapped[_typing.List["CompanyContacts"]] = \
        _orm.relationship(back_populates="company")


class CompanyContacts(_db.Base):

    __tablename__ = "company_contacts"

    id = _sql.Column(_sql.Integer,  primary_key=True, index=True)
    company_id = _sql.Column(_sql.Integer, _sql.ForeignKey("company_id"), nullable=False, index=True)
    kind = _sql.Column(_sql.String, nullable=False, index=True)
    value = _sql.Column(_sql.String, nullable=False, unique=True)

    company: _orm.Mapped["Company"] = \
        _orm.relationship(back_populates="contacts", cascade="delete")


class Specialization(_db.Base):

    __tablename__ = "specialization"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, unique=True, nullable=False, index=True)

    companies: _orm.Mapped[_typing.List["CompanySpecializations"]] = \
        _orm.relationship(back_populates="specialization")

    teachers: _orm.Mapped[_typing.List["TeacherSpecializations"]] = \
        _orm.relationship(back_populates="specialization")

    courses: _orm.Mapped[_typing.List["CourseTags"]] = \
        _orm.relationship(back_populates="specialization")


class CompanySpecializations(_db.Base):

    __tablename__ = "company_specializations"

    company_id = _sql.Column(_sql.Integer, _sql.ForeignKey("company.id"), primary_key=True)
    specialization_id = _sql.Column(_sql.Integer, _sql.ForeignKey("specialization.id"), primary_key=True)

    company: _orm.Mapped["Company"] = \
        _orm.relationship(back_populates="specializations", cascade="delete")

    specialization: _orm.Mapped["Specialization"] = \
        _orm.relationship(back_populates="companies", cascade="delete")


class Teacher(_db.Base):

    __tablename__ = "teacher"

    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"), primary_key=True, index=True)
    company_id = _sql.Column(_sql.Integer, _sql.ForeignKey("company.id"), index=True)
    bio = _sql.Column(_sql.String, nullable=True, index=False)

    user: _orm.Mapped["User"] = \
        _orm.relationship(back_populates="teacher", cascade="delete")

    company: _orm.Mapped["Company"] = \
        _orm.relationship(back_populates="teachers")

    specializations: _orm.Mapped[_typing.List["TeacherSpecializations"]] = \
        _orm.relationship(back_populates="teacher")

    groups: _orm.Mapped[_typing.List["Group"]] = \
        _orm.relationship(back_populates="teacher")


class TeacherSpecializations(_db.Base):

    __tablename__ = "teacher_specializations"

    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("teacher.user_id"), primary_key=True)
    specialization_id = _sql.Column(_sql.Integer, _sql.ForeignKey("specialization.id"), primary_key=True)

    teacher: _orm.Mapped["Teacher"] = \
        _orm.relationship(back_populates="specializations", cascade="delete")

    specialization: _orm.Mapped["Specialization"] = \
        _orm.relationship(back_populates="teachers", cascade="delete")


class Course(_db.Base):

    __tablename__ = "course"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, unique=True, index=True, nullable=False)
    description = _sql.Column(_sql.String, nullable=False, index=False)
    author_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"), index=True, nullable=False)
    date_created = _sql.Column(_sql.Date)
    date_updated = _sql.Column(_sql.Date)
    views = _sql.Column(_sql.Integer, nullable=False, default=0)

    tags: _orm.Mapped[_typing.List["CourseTags"]] = \
        _orm.relationship(back_populates="course")

    sessions: _orm.Mapped[_typing.List["Session"]] = \
        _orm.relationship(back_populates="course")

    progresses: _orm.Mapped[_typing.List["Progress"]] = \
        _orm.relationship(back_populates="course")

    lessons: _orm.Mapped[_typing.List["Lesson"]] = \
        _orm.relationship(back_populates="course")


class CourseTags(_db.Base):

    __tablename__ = "course_tags"

    course_id = _sql.Column(_sql.Integer, _sql.ForeignKey("course.id"), primary_key=True)
    specialization_id = _sql.Column(_sql.Integer, _sql.ForeignKey("specialization.id"), primary_key=True)

    course: _orm.Mapped["Course"] = \
        _orm.relationship(back_populates="tags", cascade="delete")

    specialization: _orm.Mapped["Specialization"] = \
        _orm.relationship(back_populates="courses", cascade="delete")


class Lesson(_db.Base):

    __tablename__ = "lesson"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    course_id = _sql.Column(_sql.Integer, _sql.ForeignKey("course.id"), index=True)
    number = _sql.Column(_sql.Integer, nullable=False)
    name = _sql.Column(_sql.String, nullable=False)
    description = _sql.Column(_sql.String, nullable=True, index=False)
    duration = _sql.Column(_sql.Time, nullable=False)

    course: _orm.Mapped["Course"] = \
        _orm.relationship(back_populates="lessons", cascade="delete")


class Group(_db.Base):

    __tablename__ = "group"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, unique=True, nullable=False, index=True)
    teacher_id = _sql.Column(_sql.Integer, _sql.ForeignKey("teacher.user_id"))

    teacher: _orm.Mapped["Teacher"] = \
        _orm.relationship(back_populates="groups")

    students: _orm.Mapped[_typing.List["GroupStudents"]] = \
        _orm.relationship(back_populates="group")

    sessions: _orm.Mapped[_typing.List["GroupSessions"]] = \
        _orm.relationship(back_populates="group")


class GroupStudents(_db.Base):

    __tablename__ = "group_students"

    student_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"), primary_key=True)
    group_id = _sql.Column(_sql.Integer, _sql.ForeignKey("group.id"), primary_key=True)

    student: _orm.Mapped["User"] = \
        _orm.relationship(back_populates="groups", cascade="delete")

    group: _orm.Mapped["Group"] = \
        _orm.relationship(back_populates="students", cascade="delete")


class Session(_db.Base):

    __tablename__ = "session"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    course_id = _sql.Column(_sql.Integer, _sql.ForeignKey("course.id"))
    date_started = _sql.Column(_sql.Date)
    date_ended = _sql.Column(_sql.Date, nullable=True)
    active = _sql.Column(_sql.Boolean, nullable=False, default=True)

    course: _orm.Mapped["Course"] = \
        _orm.relationship(back_populates="sessions")

    group: _orm.Mapped["GroupSessions"] = \
        _orm.relationship(back_populates="session", cascade="delete")

    user: _orm.Mapped["IndividualSessions"] = \
        _orm.relationship(back_populates="session", cascade="delete")

    hometasks: _orm.Mapped[_typing.List["Hometask"]] = \
        _orm.relationship(back_populates="session")


class GroupSessions(_db.Base):

    __tablename__ = "group_sessions"

    session_id = _sql.Column(_sql.Integer, _sql.ForeignKey("session.id"), primary_key=True)
    group_id = _sql.Column(_sql.Integer,  _sql.ForeignKey("group.id"), primary_key=True)

    session: _orm.Mapped["Session"] = \
        _orm.relationship(back_populates="group", cascade="delete")

    group: _orm.Mapped["Group"] = \
        _orm.relationship("Group", back_populates="sessions", cascade="delete")


class IndividualSessions(_db.Base):

    __tablename__ = "individual_sessions"

    session_id = _sql.Column(_sql.Integer, _sql.ForeignKey("session.id"), primary_key=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"), primary_key=True)

    session: _orm.Mapped["Session"] = \
        _orm.relationship(back_populates="user", cascade="delete")

    user: _orm.Mapped["User"] = \
        _orm.relationship(back_populates="sessions", cascade="delete")


class Hometask(_db.Base):

    __tablename__ = "hometask"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    description = _sql.Column(_sql.String, nullable=False)
    session_id = _sql.Column(_sql.Integer, _sql.ForeignKey("session.id"))
    student_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"))
    date_given = _sql.Column(_sql.DateTime)
    date_done = _sql.Column(_sql.DateTime)
    deadline = _sql.Column(_sql.DateTime)
    mark = _sql.Column(_sql.DateTime)

    session: _orm.Mapped["Session"] = \
        _orm.relationship(back_populates="hometasks", cascade="delete")

    student: _orm.Mapped["User"] = \
        _orm.relationship(back_populates="hometasks")


class Progress(_db.Base):

    __tablename__ = "progress"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    student_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"))
    course_id = _sql.Column(_sql.Integer, _sql.ForeignKey("course.id"))
    lesson = _sql.Column(_sql.Integer, nullable=False)
    step = _sql.Column(_sql.Integer, nullable=False)

    student: _orm.Mapped["User"] = \
        _orm.relationship(back_populates="progresses", cascade="delete")

    course: _orm.Mapped["Course"] = \
        _orm.relationship(back_populates="progresses", cascade="delete")


class Chat(_db.Base):

    __tablename__ = "chat"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, nullable=True)
    date_created = _sql.Column(_sql.DateTime)

    members: _orm.Mapped[_typing.List["ChatMembers"]] = \
        _orm.relationship(back_populates="chat")


class ChatMembers(_db.Base):

    __tablename__ = "chat_members"

    chat_id = _sql.Column(_sql.Integer, _sql.ForeignKey("chat.id"), primary_key=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"), primary_key=True)
    admin = _sql.Column(_sql.Boolean)

    chat: _orm.Mapped["Chat"] = \
        _orm.relationship(back_populates="members", cascade="delete")

    member: _orm.Mapped["User"] = \
        _orm.relationship(back_populates="chats", cascade="delete")


class Admin(_db.Base):

    __tablename__ = "admin"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    login = _sql.Column(_sql.String, unique=True, index=True)
    password = _sql.Column(_sql.String, nullable=False)
    sign = _sql.Column(_sql.String)
    telegram = _sql.Column(_sql.Integer, nullable=True, index=True)


class Link(_db.Base):

    __tablename__ = "link"

    url = _sql.Column(_sql.String, primary_key=True)
    action = _sql.Column(_sql.String, nullable=False)
    target = _sql.Column(_sql.Integer, nullable=False, index=True)
    date_expired = _sql.Column(_sql.DateTime, nullable=True)
    limit = _sql.Column(_sql.Integer, nullable=True)
    count_used = _sql.Column(_sql.Integer, default=0)


class Notification(_db.Base):

    __tablename__ = "notification"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"), index=True)
    date_alarm = _sql.Column(_sql.DateTime, nullable=False)
    title = _sql.Column(_sql.String, nullable=False)
    descritption = _sql.Column(_sql.String, nullable=True)
    url = _sql.Column(_sql.String, nullable=True)

    user: _orm.Mapped["User"] = \
        _orm.relationship(back_populates="notifications", cascade="delete")


signable = _typing.Union[Admin, User]
