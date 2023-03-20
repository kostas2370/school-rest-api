from base.models import Student, Teacher, Classroom, Subject, Grades, Assignments, StudentAssigments, Announcements
from base.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "id")


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    classroom = ClassroomSerializer()

    class Meta:
        model = Subject
        fields = "__all__"


class GradesSerializer(serializers.ModelSerializer):
    subject_name = SubjectSerializer()
    teacher = TeacherSerializer()
    classroom = ClassroomSerializer()

    class Meta:
        model = Grades
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], password = validated_data['password'], role = 4)
        return user


class AssignmentsSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    classroom = ClassroomSerializer()
    teacher = TeacherSerializer()

    class Meta:
        model = Assignments
        fields = "__all__"


class AnnouncementsSerializer(serializers.ModelSerializer):
    publisher = UserSerializer()

    class Meta:
        model = Announcements
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    classroom = ClassroomSerializer()

    class Meta:
        model = Student
        fields = "__all__"


class StudentAssigmentsSerializer(serializers.ModelSerializer):
    student = StudentSerializer

    class Meta:
        model = StudentAssigments
        fields = "__all__"
