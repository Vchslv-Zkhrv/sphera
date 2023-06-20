import sqlalchemy as _sql
import sqlalchemy.orm as _orm

import database as _db


class User(_db.Base):

    __tablename__ = "user"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    role = _sql.Column(_sql.String, nullable=False, default="student")
    email = _sql.Column(_sql.String, unique=True, index=True)
    passsword = _sql.Column(_sql.String, nullable=False)
    fname = _sql.Column(_sql.String, nullable=False)
    lname = _sql.Column(_sql.String, nullable=False)
    sname = _sql.Column(_sql.String, nullable=True)
    date_created = _sql.Column(_sql.DateTime)
    date_online = _sql.Column(_sql.DateTime)
    online = _sql.Column(_sql.Boolean)
    sign = _sql.Column(_sql.String, nullable=False)

    groups = _orm.relationship("GroupStudents", back_populates="student")
    sessions = _orm.relationship("IndividualSessions", back_populates="user")
    hometasks = _orm.relationship("Hometask", back_populates="student")
    progresses = _orm.relationship("Progress", back_populates="student")
    chats = _orm.relationship("ChatMembers", back_populates="member")
    activities = _orm.relationship("UserActivities", back_populates="user")
    notifications = _orm.relationship("Notification", back_populates="user")


class UserActivities(_db.Base):

    __tablename__ = "user_activities"

    id = _sql.Column(_sql.Integer,  primary_key=True, index=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"))
    date = _sql.Column(_sql.DateTime)

    user = _orm.relationship("User", back_populates="activities")


class Company(_db.Base):

    __tablename__ = "company"

    id = _sql.Column(_sql.Integer,  primary_key=True, index=True)
    name = _sql.Column(_sql.String, unique=True, index=True)

    specializations = _orm.relationship("CompanySpecializations", back_populates="company")
    teachers = _orm.relationship("Teacher", back_populates="company")


class Specialization(_db.Base):

    __tablename__ = "specialization"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, unique=True, nullable=False, index=True)

    companies = _orm.relationship("CompanySpecializations", back_populates="specialization")
    teachers = _orm.relationship("TeacherSpecializations", back_populates="specialization")
    courses = _orm.relationship("CourseTags", back_populates="specialization")


class CompanySpecializations(_db.Base):

    __tablename__ = "company_specializations"

    company_id = _sql.Column(_sql.Integer, _sql.ForeignKey("company.id"), primary_key=True)
    specialization_id = _sql.Column(_sql.Integer, _sql.ForeignKey("specialization.id"), primary_key=True)

    company = _orm.relationship("Company", back_populates="specializations")
    specialization = _orm.relationship("Specialization", back_populates="companies")


class Teacher(_db.Base):

    __tablename__ = "teacher"

    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"), primary_key=True, index=True)
    company_name = _sql.Column(_sql.String, _sql.ForeignKey("company.name"), index=True)
    bio = _sql.Column(_sql.String, nullable=True, index=False)

    company = _orm.relationship("Company", back_populates="teachers")
    specializations = _orm.relationship("TeacherSpecializations", back_populates="teacher")
    groups = _orm.relationship("Group", back_populates="teacher")


class TeacherSpecializations(_db.Base):

    __tablename__ = "teacher_specializations"

    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("teacher.user_id"), primary_key=True)
    specialization_id = _sql.Column(_sql.Integer, _sql.ForeignKey("specialization.id"), primary_key=True)

    teacher = _orm.relationship("Teacher", back_populates="specializations")
    specialization = _orm.relationship("Specialization", back_populates="teachers")


class Course(_db.Base):

    __tablename__ = "course"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, unique=True, index=True, nullable=False)
    description = _sql.Column(_sql.String, nullable=False, index=False)
    author_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"), index=True, nullable=False)
    date_created = _sql.Column(_sql.Date)
    date_updated = _sql.Column(_sql.Date)
    views = _sql.Column(_sql.Integer, nullable=False, default=0)

    tags = _orm.relationship("CourseTags", back_populates="course")
    sessions = _orm.relationship("Session", back_populates="course")
    progresses = _orm.relationship("Progress", back_populates="course")


class CourseTags(_db.Base):

    __tablename__ = "course_tags"

    course_id = _sql.Column(_sql.Integer, _sql.ForeignKey("course.id"), primary_key=True)
    specialization_id = _sql.Column(_sql.Integer, _sql.ForeignKey("specialization.id"), primary_key=True)

    course = _orm.relationship("Course", back_populates="tags")
    specialization = _orm.relationship("Specialization", back_populates="courses")


class Lesson(_db.Base):

    __tablename__ = "lesson"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    course_id = _sql.Column(_sql.Integer, _sql.ForeignKey("course.id"), index=True)
    number = _sql.Column(_sql.Integer, nullable=False)
    name = _sql.Column(_sql.String, nullable=False)
    description = _sql.Column(_sql.String, nullable=True, index=False)
    duration = _sql.Column(_sql.Time, nullable=False)


class Group(_db.Base):

    __tablename__ = "group"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, unique=True, nullable=False, index=True)
    teacher_id = _sql.Column(_sql.Integer, _sql.ForeignKey("teacher.user_id"))

    teacher = _orm.relationship("Teacher", back_populates="groups")
    students = _orm.relationship("GroupStudents", back_populates="group")
    sessions = _orm.relationship("GroupSessions", back_populates="group")


class GroupStudents(_db.Base):

    __tablename__ = "group_students"

    student_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"), primary_key=True)
    group_id = _sql.Column(_sql.Integer, _sql.ForeignKey("group.id"), primary_key=True)

    student = _orm.relationship("User", back_populates="groups")
    group = _orm.relationship("Group", back_populates="students")


class Session(_db.Base):

    __tablename__ = "session"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    course_id = _sql.Column(_sql.Integer, _sql.ForeignKey("course.id"))
    date_started = _sql.Column(_sql.Date)
    date_ended = _sql.Column(_sql.Date, nullable=True)
    active = _sql.Column(_sql.Boolean, nullable=False, default=True)

    course = _orm.relationship("Course", back_populates="sessions")
    group = _orm.relationship("GroupSession", back_populates="session")
    user = _orm.relationship("User", back_populates="session")
    hometasks = _orm.relationship("Hometask", back_populates="session")


class GroupSessions(_db.Base):

    __tablename__ = "group_sessions"

    session_id = _sql.Column(_sql.Integer, _sql.ForeignKey("session.id"), primary_key=True)
    group_id = _sql.Column(_sql.Integer,  _sql.ForeignKey("group.id"), primary_key=True)

    session = _orm.relationship("Session", back_populates="group")
    group = _orm.relationship("Group", back_populates="sessions")


class IndividualSessions(_db.Base):

    __tablename__ = "individual_sessions"

    session_id = _sql.Column(_sql.Integer, _sql.ForeignKey("session.id"), primary_key=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"), primary_key=True)

    session = _orm.relationship("Session", back_populates="user")
    user = _orm.relationship("User", back_populates="sessions")


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

    session = _orm.relationship("Session", back_populates="hometasks")
    student = _orm.relationship("User", back_populates="hometasks")


class Progress(_db.Base):

    __tablename__ = "progress"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    student_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"))
    course_id = _sql.Column(_sql.Integer, _sql.ForeignKey("course.id"))
    lesson = _sql.Column(_sql.Integer, nullable=False)
    step = _sql.Column(_sql.Integer, nullable=False)

    student = _orm.relationship("User", back_populates="progresses")
    course = _orm.relationship("Course", back_populates="progresses")


class Chat(_db.Base):

    __tablename__ = "chat"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, nullable=True)
    date_created = _sql.Column(_sql.DateTime)

    members = _orm.relationship("ChatMembers", back_populates="chat")


class ChatMembers(_db.Base):

    __tablename__ = "chat_members"

    chat_id = _sql.Column(_sql.Integer, _sql.ForeignKey("chat.id"), primary_key=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("user.id"), primary_key=True)
    admin = _sql.Column(_sql.Boolean)

    chat = _orm.relationship("Chat", back_populates="members")
    member = _orm.relationship("User", back_populates="chats")


class Admin(_db.Base):

    __tablename__ = "admin"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    login = _sql.Column(_sql.String, primary_key=True, index=True)
    password = _sql.Column(_sql.String, nullable=False)
    sign = _sql.Column(_sql.String)


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

    user = _orm.relationship("User", back_populates="notifications")
