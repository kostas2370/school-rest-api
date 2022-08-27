from rest_framework import serializers
from base.models import Student,Teacher,Classroom,subject,Grades
from base.models import User


class StudentSerializer(serializers.ModelSerializer):
	class Meta:
		model=Student
		fields=("first_name",'last_name','phone','email','photo','apousies','user','taxh')
		read_only_fields=('student_id','created')

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

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],password = validated_data['password'],role=4 )
        return user