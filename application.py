from datetime import timedelta
from flask_cors import CORS
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import ForeignKey
import datetime
from json import dumps


app = Flask('scheduler')
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:masterpsw@scheduler.ctxuo4jlqpyv.eu-central-1.rds.amazonaws' \
                                 '.com:3369/scheduler'
CORS(app)
db = SQLAlchemy(app)


# _______Models_______
class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    token = db.Column(db.String(100))
    rights = db.Column(db.String(20))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, token, rights):
        self.name = name
        self.token = token
        self.rights = rights

    def __repr__(self):
        return '' % self.id


class Classroom(db.Model):
    __tablename__ = "classrooms"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    location = db.Column(db.String(20))
    classroom_type = db.Column(db.String(20))
    capacity = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, location, classroom_type, capacity):
        self.name = name
        self.location = location
        self.classroom_type = classroom_type
        self.capacity = capacity

    def __repr__(self):
        return '' % self.id


class Lesson(db.Model):
    __tablename__ = "lessons"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    year = db.Column(db.Integer)
    specialization = db.Column(db.String(20))
    lesson_type = db.Column(db.String(20))
    length = db.Column(db.Time)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, year, specialization, lesson_type, length):
        self.name = name
        self.year = year
        self.specialization = specialization
        self.lesson_type = lesson_type
        self.length = length

    def __repr__(self):
        return '' % self.id


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, ForeignKey('groups.id'))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, group_id):
        self.group_id = group_id

    def __repr__(self):
        return '' % self.id


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    day = db.Column(db.String(20))
    length = db.Column(db.Time)
    start = db.Column(db.Time)
    lesson_id = db.Column(db.Integer, ForeignKey('lessons.id'))
    classroom_id = db.Column(db.Integer, ForeignKey('classrooms.id'))
    teacher_id = db.Column(db.Integer, ForeignKey('teachers.id'))
    group_id = db.Column(db.Integer, ForeignKey('groups.id'))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, teacher_id, classroom_id, group_id, lesson_id, day, start, length):
        self.name = name
        self.day = day
        self.start = start
        self.length = length
        self.lesson_id = lesson_id
        self.classroom_id = classroom_id
        self.teacher_id = teacher_id
        self.group_id = group_id

    def __repr__(self):
        return '' % self.id


class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specialization = db.Column(db.String(20))
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


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    specialization = db.Column(db.String(20))
    year = db.Column(db.Integer)
    courses = db.Column(db.Integer)
    course_length = db.Column(db.Time)
    seminaries = db.Column(db.Integer)
    seminary_length = db.Column(db.Time)
    laboratories = db.Column(db.Integer)
    laboratory_length = db.Column(db.Time)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, specialization, year, courses, course_length, seminaries, seminary_length, laboratories, laboratory_length):
        self.name = name
        self.specialization = specialization
        self.year = year
        self.courses = courses
        self.course_length = course_length
        self.seminaries = seminaries
        self.seminary_length = seminary_length
        self.laboratories = laboratories
        self.laboratory_length = laboratory_length

    def __repr__(self):
        return '' % self.id


# _______Schema_______
class TeacherSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Teacher
        sql_session = db.session

    name = fields.String(required=True)
    token = fields.String(required=True)
    rights = fields.String(required=True)


class ClassroomSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Classroom
        sql_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    location = fields.String()
    classroom_type = fields.String()
    capacity = fields.Number()


class LessonSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Lesson
        sql_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    year = fields.Number()
    specialization = fields.String()
    lesson_type = fields.String()
    length = fields.Time()


class StudentSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Student
        sql_session = db.session

    id = fields.Number(dump_only=True)
    group_id = fields.Number()


class EventSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Event
        sql_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String()
    day = fields.Number()
    start = fields.Time()
    lesson_id = fields.Number()
    classroom_id = fields.Number()
    teacher_id = fields.Number()
    group_id = fields.Number()
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


class CourseSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Course
        sql_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String()
    specialization = fields.String()
    year = fields.Number()
    courses = fields.Number()
    course_length = fields.Time()
    seminaries = fields.Number()
    seminary_length = fields.Time()
    laboratories = fields.Number()
    laboratory_length = fields.Time()


db.create_all()


# _______Routes_______
@app.route('/teachers', methods=['GET'])
def get_all_teachers():
    get_teachers = Teacher.query.all()
    teacher_schema = TeacherSchema(many=True)
    teachers = teacher_schema.dump(get_teachers)
    return make_response(jsonify({"teachers": teachers}))


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
    if data.get('id'):
        get_teacher.id = data['id']
    db.session.add(get_teacher)
    db.session.commit()
    teacher_schema = TeacherSchema(only=['id', 'name', 'token'])
    teacher = teacher_schema.dump(get_teacher)
    return make_response(jsonify({"teacher": teacher}))


@app.route('/teachers/<id>', methods=['DELETE'])
def delete_teacher_by_id(id):
    get_teacher = Teacher.query.get(id)
    db.session.delete(get_teacher)
    db.session.commit()
    return make_response("", 204)


@app.route('/teachers/<adminpsw>', methods=['POST'])
def create_teacher(adminpsw):
    data = request.get_json(force=True)
    teacher_schema = TeacherSchema()
    rights = "User"
    if adminpsw == "makemeadmin":
        rights = "Admin"
    teacher = Teacher(data.get("name"), data.get("token"), rights)
    result = teacher_schema.dump(teacher.create())
    return make_response(jsonify({"teacher": result}), 200)


@app.route('/classrooms', methods=['GET'])
def get_all_classrooms():
    get_classrooms = Classroom.query.all()
    classroom_schema = ClassroomSchema(many=True)
    classrooms = classroom_schema.dump(get_classrooms)
    return make_response(jsonify({"classrooms": classrooms}))


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
    if data.get('id'):
        get_classroom.id = data['id']
    db.session.add(get_classroom)
    db.session.commit()
    classroom_schema = ClassroomSchema(only=['id', 'name', 'location', 'classroom_type', 'capacity'])
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
    classroom = Classroom(data.get("name"), data.get("location"), data.get("classroom_type"), data.get("capacity"))
    result = classroom_schema.dump(classroom.create())
    return make_response(jsonify({"classroom": result}), 200)


@app.route('/lessons', methods=['GET'])
def get_all_lessons():
    get_lessons = Lesson.query.all()
    lesson_schema = LessonSchema(many=True)
    lessons = lesson_schema.dump(get_lessons)
    return make_response(jsonify({"lessons": lessons}))


@app.route('/lessons/<id>', methods=['GET'])
def get_lesson_by_id(id):
    get_lesson = Lesson.query.get(id)
    lesson_schema = LessonSchema()
    lesson = lesson_schema.dump(get_lesson)
    return make_response(jsonify({"lesson": lesson}))


@app.route('/lessons/<id>', methods=['PUT'])
def update_lesson_by_id(id):
    data = request.get_json()
    get_lesson = Lesson.query.get(id)
    if data.get('id'):
        get_lesson.id = data['id']
    db.session.add(get_lesson)
    db.session.commit()
    lesson_schema = LessonSchema(only=['id', 'name', 'lesson_type', 'specialization', 'year'])
    lesson = lesson_schema.dump(get_lesson)
    return make_response(jsonify({"lesson": lesson}))


@app.route('/lessons/<id>', methods=['DELETE'])
def delete_lesson_by_id(id):
    get_lesson = Lesson.query.get(id)
    db.session.delete(get_lesson)
    db.session.commit()
    return make_response("", 204)


@app.route('/lessons', methods=['POST'])
def create_lesson():
    data = request.get_json(force=True)
    lesson_schema = LessonSchema()
    lesson = Lesson(data.get("name"), data.get("year"), data.get("specialization"), data.get("lesson_type"), data.get("length"))
    result = lesson_schema.dump(lesson.create())
    return make_response(jsonify({"lesson": result}), 200)


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
    student_schema = StudentSchema(only=['id', 'group_id'])
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
    student = Student(data.get('group_id'))
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


@app.route('/courses', methods=['GET'])
def get_all_courses():
    get_courses = Course.query.all()
    course_schema = CourseSchema(many=True)
    courses = course_schema.dump(get_courses)
    return make_response(jsonify({"courses": courses}))


@app.route('/courses/<id>', methods=['GET'])
def get_course_by_id(id):
    get_course = Course.query.get(id)
    course_schema = CourseSchema()
    course = course_schema.dump(get_course)
    return make_response(jsonify({"course": course}))


@app.route('/courses/<id>', methods=['PUT'])
def update_course_by_id(id):
    data = request.get_json()
    get_course = Course.query.get(id)
    course_schema = CourseSchema(
        only=['id', 'name', 'year', 'specialization', 'courses', 'course_length', 'seminaries', 'seminary_length',
              'laboratories', 'laboratory_length'])
    course = course_schema.dump(get_course)
    if data.get('id'):
        if get_course.id == int(data['id']):
            get_course.name = data['name']
            get_course.name = data['year']
            get_course.name = data['specialization']
            get_course.name = data['courses']
            get_course.name = data['course_length']
            get_course.name = data['seminaries']
            get_course.name = data['seminary_length']
            get_course.name = data['laboratories']
            get_course.name = data['laboratory_length']
            db.session.add(get_course)
            db.session.commit()
    return make_response(jsonify({"course": course}))


@app.route('/courses/<id>', methods=['DELETE'])
def delete_course_by_id(id):
    get_course = Course.query.get(id)
    db.session.delete(get_course)
    db.session.commit()
    return make_response("", 204)


@app.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json(force=True)
    course_schema = CourseSchema()
    course = Course(data.get("name"), data.get("specialization"), data.get("year"), data.get('courses'),
                    data.get("course_length"), data.get("seminaries"), data.get("seminary_length"),
                    data.get("laboratories"), data.get("laboratory_length"))
    result = course_schema.dump(course.create())
    return make_response(jsonify({"course": result}), 200)


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
        only=['id', 'name', 'teacher_id', 'classroom_id', 'group_id', 'lesson_id', 'day', 'start', 'length'])
    event = event_schema.dump(get_event)
    if data.get('id'):
        if get_event.id == int(data['id']):
            get_event.name = data['name']
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
    event = Event(data.get("name"), data.get("teacher_id"), data.get("classroom_id"),
                  data.get('group_id'), data.get("lesson_id"), data.get("day"), data.get("start"), data.get("length"))
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
