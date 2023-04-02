# importing Flask class flask library, jsonify,
# from app import db
from flask import Flask, jsonify, request
import json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# creation of  an instance of the Flask class and assign to app
# __name__ refers to the default path of the packages
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lessons.db' # path to db
app.config['SQLALCHEMY_ECHO'] = True # echoes SQL for debug
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instantiate db obj using the SQLAlchemy class with the Flask app obj as arg
db = SQLAlchemy(app)

# Marshmallow must be initialised after SQLAlchemy
ma = Marshmallow(app)
#------------------------------------------------------------------------------
# class def for SQLAlchemy ORM
class Lesson(db.Model):
 """Definition of the User Model used by SQLAlchemy"""
 lesson_session = db.Column(db.String(80),nullable=False)
 lesson_code = db.Column(db.String(80),primary_key=True)
 lesson_title = db.Column(db.String(80), nullable=False)
 lesson_department = db.Column(db.String(80), nullable=False)
 lesson_tutor = db.Column(db.String(80), nullable=False)
 lesson_program_leader = db.Column(db.String(80), nullable=False)
 lesson_venue = db.Column(db.String(80), nullable=False)
 lesson_time = db.Column(db.String(80), nullable=False)
 
 def __repr__(self):
    return '<Lesson %r>' % self.lesson_code
 
     # class definition for Marshmallow serialization
class LessonSchema(ma.SQLAlchemyAutoSchema):
        # definition used by serialization library  based on user model
    class Meta:
        fields = ("lesson_session","lesson_code", "lesson_title", "lesson_department", 
                  "lesson_tutor", "lesson_program_leader", "lesson_venue", "lesson_time")

    # instantiate objects based on Marshmallows schemas
lesson_schema = LessonSchema()
lessons_schema = LessonSchema(many=True)


@app.get("/")
def hello_world():
    return " <div> <h1> My Bolton Team 8!</h1> </div>"

@app.get('/lessons/get-all-lessons')
def get_all_lessons():
    lessons = Lesson.query.all()
    return lessons_schema.jsonify(lessons)
 
@app.post("/lessons/add-lessons-json")
def lessons_add_json():
    json_data = request.get_json()
    print(json_data)
    
    new_lesson = Lesson (
        lesson_session = json_data['lesson_session'],
        lesson_code = json_data['lesson_code'],
        lesson_title = json_data['lesson_title'],
       lesson_department = json_data['lesson_department'],
       lesson_tutor = json_data['lesson_tutor'],
       lesson_program_leader = json_data['lesson_program_leader'],
       lesson_venue = json_data['lesson_venue'],
       lesson_time = json_data['lesson_time']

    )

    db.session.add(new_lesson)
    db.session.commit()
    print ("Record added Successfully")
    print (json.dumps(json_data, indent=4)) # used for debugging purposes
    return lesson_schema.jsonify(new_lesson)

