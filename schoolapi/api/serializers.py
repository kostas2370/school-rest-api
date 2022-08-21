from rest_framework import serializers
from base.models import Student,Teacher,Classroom,subject,Grades
from django.contrib.auth.models import User


class StudentSerializer(serializers.ModelSerializer):
	class Meta:
		model=Student
		fields="__all__"

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields="__all__"

class TeacherSerializer(serializers.ModelSerializer):
	class Meta:
		model=Teacher
		fields="__all__"

class ClassroomSerializer(serializers.ModelSerializer):
	class Meta:
		model=Classroom
		fields="__all__"

class SubjectSerializer(serializers.ModelSerializer):
	class Meta:
		model=subject
		fields="__all__"

class GradesSerializer(serializers.ModelSerializer):
	class Meta:
		model=Grades
		fields="__all__"