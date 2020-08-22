from datetime import timedelta
from flask_cors import CORS
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import Enum, ForeignKey, String, Time
from datetime import time
import enum
import datetime
from Models import Teacher

from sqlalchemy.orm import relationship

app = Flask('scheduler')
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:masterpsw@scheduler.ctxuo4jlqpyv.eu-central-1.rds.amazonaws.com:3369/scheduler'
CORS(app)
db = SQLAlchemy(app)



# _______Enums_______
class ActivityType(enum.Enum):
    not_available = "NOT_AVAILABLE"
    course = "COURSE"
    seminar = "SEMINAR"
    laboratory = "LABORATORY"


class Specialization(enum.Enum):
    series_A = "SERIES_A"
    series_B = "SERIES_B"
    EA = "EA"
    TST = "TST"


# _______Association_Tables_______
event_group_association_table = db.Table('events_groups', db.Model.metadata,
                                         db.Column('event_id', db.Integer, ForeignKey('events.id')),
                                         db.Column('group_id', db.Integer, ForeignKey('groups.id'))
                                         )


# _______Models_______
class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    events = relationship("Event")

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '' % self.id


class Classroom(db.Model):
    __tablename__ = "classrooms"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    events = relationship("Event")

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '' % self.id


class AcademicActivity(db.Model):
    __tablename__ = "activities"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    activity_type = db.Column(db.String(20))
    length = db.Column(db.Time)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, activity_type, length):
        self.name = name
        self.activity_type = activity_type
        self.length = length

    def __repr__(self):
        return '' % self.id


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specialization = db.Column(Enum(Specialization))
    year = db.Column(db.Integer)
    group = db.Column(db.Integer)
    subgroup = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, specialization, year, group, subgroup):
        self.specialization = specialization
        self.year = year
        self.group = group
        self.subgroup = subgroup

    def __repr__(self):
        return '' % self.id


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day = db.Column(db.Integer)
    length = db.Column(db.Time)
    start = db.Column(db.Time)
    activity_id = db.Column(db.Integer, ForeignKey('activities.id'))
    classroom_id = db.Column(db.Integer, ForeignKey('classrooms.id'))
    teacher_id = db.Column(db.Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher")
    classroom = relationship("Classroom")
    activity = relationship("AcademicActivity")
    groups = relationship(
        "Group",
        secondary=event_group_association_table)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, day, start, length, activity_id, classroom_id, teacher_id):
        self.day = day
        self.start = start
        self.activity_id = activity_id
        self.classroom_id = classroom_id
        self.teacher_id = teacher_id
        self.length = length

    def __repr__(self):
        return '' % self.id


class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specialization = db.Column(db.String(20))
    year = db.Column(db.Integer)
    group = db.Column(db.Integer)
    subgroup = db.Column(db.Integer)
    events = relationship(
        "Event",
        secondary=event_group_association_table)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, specialization, year, group, subgroup):
        self.specialization = specialization
        self.year = year
        self.group = group
        self.subgroup = subgroup

    def __repr__(self):
        return '' % self.id


# _______Schema_______
class TeacherSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Teacher
        sql_session = db.session

    name = fields.String(required=True)


class ClassroomSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Classroom
        sql_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    type = fields.String()
    capacity = fields.Number()


class AcademicActivitySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = AcademicActivity
        sql_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    length = fields.Time()


class StudentSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Student
        sql_session = db.session

    id = fields.Number(dump_only=True)
    specialization = fields.String()
    year = fields.Number()
    group = fields.Number()
    subgroup = fields.Number()


class EventSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Event
        sql_session = db.session

    id = fields.Number(dump_only=True)
    day = fields.Number()
    start = fields.Time()
    activity_id = fields.Number()
    classroom_id = fields.Number()
    teacher_id = fields.Number()
    length = fields.Time()


class GroupSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Group
        sql_session = db.session

    id = fields.Number(dump_only=True)
    specialization = fields.String()
    year = fields.Number()
    group = fields.Number()
    subgroup = fields.Number()


db.create_all()


# _______Routes_______
@app.route('/teachers', methods=['GET'])
def get_all_teachers():
    get_teachers = Teacher.query.all()
    teacher_schema = TeacherSchema(many=True)
    teachers = teacher_schema.dump(get_teachers)
    return make_response(jsonify({"teacher": teachers}))


@app.route('/teachers/<id>', methods=['GET'])
def get_teacher_by_id(id):
    get_teacher = Teacher.query.get(id)
    teacher_schema = TeacherSchema()
    teacher = teacher_schema.dump(get_teacher)
    return make_response(jsonify({"teacher": teacher}))


@app.route('/teachers/<id>', methods=['PUT'])
def update_teachers_by_id(id):
    data = request.get_json()
    get_teacher = Teacher.query.get(id)
    if data.get('name'):
        get_teacher.name = data['name']
    db.session.add(get_teacher)
    db.session.commit()
    teacher_schema = TeacherSchema(only=['id', 'name'])
    teacher = teacher_schema.dump(get_teacher)
    return make_response(jsonify({"teacher": teacher}))


@app.route('/teachers/<id>', methods=['DELETE'])
def delete_teacher_by_id(id):
    get_teacher = Teacher.query.get(id)
    db.session.delete(get_teacher)
    db.session.commit()
    return make_response("", 204)


@app.route('/teachers', methods=['POST'])
def create_teacher():
    data = request.get_json(force=True)
    teacher_schema = TeacherSchema()
    teacher = Teacher(data.get("name"))
    result = teacher_schema.dump(teacher.create())
    return make_response(jsonify({"teacher": result}), 200)


@app.route('/classrooms', methods=['GET'])
def get_all_classrooms():
    get_classrooms = Classroom.query.all()
    classroom_schema = ClassroomSchema(many=True)
    classrooms = classroom_schema.dump(get_classrooms)
    return make_response(jsonify({"classroom": classrooms}))


@app.route('/classrooms/<id>', methods=['GET'])
def get_classroom_by_id(id):
    get_classroom = Classroom.query.get(id)
    classroom_schema = ClassroomSchema()
    classroom = classroom_schema.dump(get_classroom)
    return make_response(jsonify({"classroom": classroom}))


@app.route('/classrooms/<id>', methods=['PUT'])
def update_classroom_by_id(id):
    data = request.get_json()
    get_classroom = Classroom.query.get(id)
    if data.get('name'):
        get_classroom.name = data['name']
    db.session.add(get_classroom)
    db.session.commit()
    classroom_schema = ClassroomSchema(only=['id', 'name', 'type'])
    classroom = classroom_schema.dump(get_classroom)
    return make_response(jsonify({"classroom": classroom}))


@app.route('/classrooms/<id>', methods=['DELETE'])
def delete_classrooms_by_id(id):
    get_classroom = Classroom.query.get(id)
    db.session.delete(get_classroom)
    db.session.commit()
    return make_response("", 204)


@app.route('/classrooms', methods=['POST'])
def create_classrooms():
    data = request.get_json(force=True)
    classroom_schema = ClassroomSchema()
    classroom = Classroom(data.get("name"))
    result = classroom_schema.dump(classroom.create())
    return make_response(jsonify({"classroom": result}), 200)


@app.route('/activities', methods=['GET'])
def get_all_activities():
    get_activities = AcademicActivity.query.all()
    activities_schema = AcademicActivitySchema(many=True)
    academicActivities = activities_schema.dump(get_activities)
    return make_response(jsonify({"academicActivities": academicActivities}))


@app.route('/activities/<id>', methods=['GET'])
def get_activities_by_id(id):
    get_activities = AcademicActivity.query.get(id)
    academic_activity_schema = AcademicActivitySchema()
    academic_activity = academic_activity_schema.dump(get_activities)
    return make_response(jsonify({"academicActivity": academic_activity}))


@app.route('/activities/<id>', methods=['PUT'])
def update_activity_by_id(id):
    data = request.get_json()
    get_activity = AcademicActivity.query.get(id)
    if data.get('name'):
        get_activity.name = data['name']
    db.session.add(get_activity)
    db.session.commit()
    activity_schema = AcademicActivitySchema(only=['id', 'name', 'type', 'specialization', 'year'])
    academic_activity = activity_schema.dump(get_activity)
    return make_response(jsonify({"academicActivity": academic_activity}))


@app.route('/activities/<id>', methods=['DELETE'])
def delete_activity_by_id(id):
    get_activity = AcademicActivity.query.get(id)
    db.session.delete(get_activity)
    db.session.commit()
    return make_response("", 204)


@app.route('/activities', methods=['POST'])
def create_activity():
    data = request.get_json(force=True)
    activity_schema = AcademicActivitySchema()
    academic_activity = AcademicActivity(data.get("name"), data.get("activity_type"), data.get("length"))
    result = activity_schema.dump(academic_activity.create())
    return make_response(jsonify({"academicActivity": result}), 200)


@app.route('/students', methods=['GET'])
def get_all_student():
    get_students = Student.query.all()
    student_schema = StudentSchema(many=True)
    students = student_schema.dump(get_students)
    return make_response(jsonify({"students": students}))


@app.route('/students/<id>', methods=['GET'])
def get_student_by_id(id):
    get_student = Student.query.get(id)
    student_schema = StudentSchema()
    student = student_schema.dump(get_student)
    return make_response(jsonify({"student": student}))


@app.route('/students/<id>', methods=['PUT'])
def update_student_by_id(id):
    data = request.get_json()
    get_student = Student.query.get(id)
    if data.get('id'):
        get_student.name = data['id']
    db.session.add(get_student)
    db.session.commit()
    student_schema = StudentSchema(only=['id', 'specialization', 'year', 'group', 'subgroup'])
    student = student_schema.dump(get_student)
    return make_response(jsonify({"student": student}))


@app.route('/students/<id>', methods=['DELETE'])
def delete_student_by_id(id):
    get_student = Student.query.get(id)
    db.session.delete(get_student)
    db.session.commit()
    return make_response("", 204)


@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json(force=True)
    student_schema = StudentSchema()
    student = Student(data.get("specialization"), data.get("year"), data.get("group"), data.get("subgroup"))
    result = student_schema.dump(student.create())
    return make_response(jsonify({"student": result}), 200)


@app.route('/groups', methods=['GET'])
def get_all_groups():
    get_groups = Group.query.all()
    group_schema = GroupSchema(many=True)
    groups = group_schema.dump(get_groups)
    return make_response(jsonify({"groups": groups}))


@app.route('/groups/<id>', methods=['GET'])
def get_group_by_id(id):
    get_group = Group.query.get(id)
    group_schema = GroupSchema()
    group = group_schema.dump(get_group)
    return make_response(jsonify({"group": group}))


@app.route('/groups/<id>', methods=['PUT'])
def update_group_by_id(id):
    data = request.get_json()
    get_group = Group.query.get(id)
    if data.get('id'):
        get_group.name = data['id']
    db.session.add(get_group)
    db.session.commit()
    group_schema = GroupSchema(only=['id', 'specialization', 'year', 'group', 'subgroup'])
    group = group_schema.dump(get_group)
    return make_response(jsonify({"group": group}))


@app.route('/groups/<id>', methods=['DELETE'])
def delete_group_by_id(id):
    get_group = Group.query.get(id)
    db.session.delete(get_group)
    db.session.commit()
    return make_response("", 204)


@app.route('/groups', methods=['POST'])
def create_group():
    data = request.get_json(force=True)
    group_schema = GroupSchema()
    group = Group(data.get("specialization"), data.get("year"), data.get("group"), data.get("subgroup"))
    result = group_schema.dump(group.create())
    return make_response(jsonify({"group": result}), 200)


@app.route('/events', methods=['GET'])
def get_all_events():
    get_events = Event.query.all()
    event_schema = EventSchema(many=True)
    events = event_schema.dump(get_events)
    return make_response(jsonify({"events": events}))


@app.route('/events/<id>', methods=['GET'])
def get_event_by_id(id):
    get_event = Event.query.get(id)
    event_schema = EventSchema()
    event = event_schema.dump(get_event)
    return make_response(jsonify({"event": event}))


@app.route('/events/<id>', methods=['PUT'])
def update_event_by_id(id):
    data = request.get_json()
    get_event = Event.query.get(id)
    event_schema = EventSchema(
        only=['id', 'day', 'start', 'length', 'activity_id', 'classroom_id', 'teacher_id'])
    event = event_schema.dump(get_event)
    if data.get('id'):
        if get_event.id == int(data['id']):
            get_event.start = data['start']
            get_event.day = data['day']
            get_event.length = data['length']
            db.session.add(get_event)
            db.session.commit()
    return make_response(jsonify({"event": event}))


@app.route('/events/<id>', methods=['DELETE'])
def delete_event_by_id(id):
    get_event = Event.query.get(id)
    db.session.delete(get_event)
    db.session.commit()
    return make_response("", 204)


@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json(force=True)
    event_schema = EventSchema()
    event = Event(data.get("day"), data.get("start"), data.get("length"), data.get("activity_id"), data.get("classroom_id"),
                  data.get("teacher_id"))
    result = event_schema.dump(event.create())
    return make_response(jsonify({"event": result}), 200)


@app.route('/events/schedule/<password>', methods=['PUT'])
def schedule_events(password):
    event_schema = EventSchema(many=True)
    complete_events = []
    if password == "adminpsw":
        get_events = Event.query.all()
        for event in get_events:
            if event.teacher:
                complete_events.append(event)
    for event in complete_events:
        event.start = "08:00"
        event.day = 1
        schedule(event)
        db.session.add(event)
        db.session.commit()

    # db.session.add(get_event)
    # db.session.commit()
    # event_schema = EventSchema(only=['id', 'day', 'start', 'activity_id', 'classroom_id', 'teacher_id'])
    # event = event_schema.dump(get_event)
    response = event_schema.dump(complete_events)
    return make_response(jsonify({"response": response}))


def schedule(event: Event):
    global time1, time2, length1, length2
    get_events = Event.query.all()
    for events in get_events:
        if events.day is not None and events.start is not None:
            group_busy = False
            for groups in events.groups:
                for group in event.groups:
                    if group.id == groups.id:
                        group_busy = True
            if isinstance(event.start, str):
                delta1 = datetime.datetime.strptime(event.start, '%H:%M')
                time1 = timedelta(hours=delta1.hour)
            elif isinstance(event.start, datetime.time):
                time1 = timedelta(hours=event.start.hour)
            elif isinstance(event.start, datetime.timedelta):
                time1 = event.start
            length1 = timedelta(hours=event.activity.length.hour)
            if isinstance(events.start, str):
                delta2 = datetime.datetime.strptime(events.start, '%H:%M')
                time2 = timedelta(hours=delta2.hour)
            elif isinstance(events.start, datetime.time):
                time2 = timedelta(hours=events.start.hour)
            length2 = timedelta(hours=events.activity.length.hour)
            if event.id != events.id and (event.teacher_id == events.teacher_id or
                                          event.classroom_id == events.classroom_id or
                                          group_busy) and (event.day == events.day and
                                                           (
                                                                   time1 <= time2 < time1 + length1 or
                                                                   time2 <= time1 < time2 + length2)):
                if time1 + timedelta(hours=1) + length1 > timedelta(hours=20):
                    event.day = event.day + 1
                    event.start = "08:00"
                else:
                    event.start = time1 + timedelta(hours=1)
                return schedule(event)
    return event


if __name__ == "__main__":
    app.run(debug=True)
