# importing Flask class flask library
from app import dbe

from flask import Flask, jsonify, request
import json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# creation of  an instance of the Flask class and assign to app
# __name__ refers to the default path of the package
modules = Flask(__name__)

modules.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lessons.db' # path to db
modules.config['SQLALCHEMY_ECHO'] = True # echoes SQL for debug
modules.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instantiate db obj using the SQLAlchemy class with the Flask app obj as arg
dbe = SQLAlchemy(modules)

# Marshmallow must be initialised after SQLAlchemy
ma = Marshmallow(modules)
#------------------------------------------------------------------------------
# class def for SQLAlchemy ORM
class Lesson(dbe.Model):
 """Definition of the User Model used by SQLAlchemy"""
 lesson_session = dbe.Column(dbe.String(80), primary_key=True)
 lesson_code = dbe.Column(dbe.String(80), nullable=False)
 lesson_title = dbe.Column(dbe.String(80), nullable=False)
 lesson_department = dbe.Column(dbe.String(80), nullable=False)
 lesson_tutor = dbe.Column(dbe.String(80), nullable=False)
 lesson_program_leader = dbe.Column(dbe.String(80), nullable=False)
 
 def __repr__(self):
    return '<Lesson %r>' % self.lesson_session
 
     # class definition for Marshmallow serialization
class LessonSchema(ma.SQLAlchemyAutoSchema):
        # definition used by serialization library  based on user model
    class Meta:
        fields = ("lesson_session","lesson_code", "lesson_title", "lesson_department", 
                  "lesson_tutor", "lesson_program_leader")

    # instantiate objects based on Marshmallows schemas
lesson_schema = LessonSchema()
lessons_schema = LessonSchema(many=True)


@modules.get("/")
def hello_world():
    return " <div> <h1> My Bolton Team 8!</h1> </div>"

@modules.get('/lessons/get-all-lessons')
def get_all_lessons():
    lessons = Lesson.query.all()
    return lessons_schema.jsonify(lessons)

@modules.post("/lessons/add-lessons-json")
def lessons_add_json():
    json_data = request.get_json()
    print(json_data)
    
    new_lesson = Lesson (
        lesson_session = json_data['lesson_session'],
        lesson_code = json_data['lesson_code'],
        lesson_title = json_data['lesson_title'],
       lesson_department = json_data['lesson_department'],
       lesson_tutor = json_data['lesson_tutor'],
       lesson_program_leader = json_data['lesson_program_leader']
    )

    dbe.session.add(new_lesson)
    dbe.session.commit()
    print ("Record added Successfully")
    print (json.dumps(json_data, indent=4)) # used for debugging purposes
    return lesson_schema.jsonify(new_lesson)

