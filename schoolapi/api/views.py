from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from base.models import Student,subject,Grades,Classroom,Teacher,User
from .serializers import StudentSerializer,TeacherSerializer,ClassroomSerializer,GradesSerializer,SubjectSerializer

from rest_framework import status
from rest_framework.decorators import api_view,permission_classes


@api_view(['GET','POST','DELETE'])
def students(request):	
	if request.method=="GET":
			if request.user.role==1 or request.user.role==2:
				first_name = request.query_params.get("first_name",None)
				student_id=request.query_params.get("student_id",None)
				last_name=request.query_params.get("last_name",None)
				classroom=request.query_params.get("classroom",None)
				
				if student_id  :
					students=Student.objects.filter(student_id=student_id)
				elif first_name and last_name and classroom:
					students=Student.objects.filter(first_name=first_name,last_name=last_name,taxh=classroom)		 
				elif first_name and last_name:
					students=Student.objects.filter(first_name=first_name,last_name=last_name)
				elif classroom:
					students=Student.objects.filter(taxh=classroom)
				elif last_name:
					students=Student.objects.filter(last_name=last_name)
				elif first_name:
					students=Student.objects.filter(first_name=first_name)
				else:
					students=Student.objects.all()
					print(request.user.username)
				
				serializer=StudentSerializer(students,many=True)
				return Response(serializer.data)
			else: 
				return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)
	elif request.method=="POST":
			if request.user.role==1 :
				data=request.data
				try:
					new_user=User.objects.create(username=data["user"]["username"],password=data["user"]["password"],role=3)
				except:
					return JsonResponse({'message':"You need to add user in ur json form"},status=status.HTTP_400_BAD_REQUEST)			
				
				try:
					new_student=Student.objects.create(user=new_user,first_name=data["first_name"],last_name=data["last_name"],taxh=data["classroom"],phone=data["phone"],email=data["email"],apousies=0)
				except:
					return JsonResponse({'message':"You need to fix the student information"},status=status.HTTP_400_BAD_REQUEST)	
				
				classroom=Classroom.objects.get(id=request.data["taxh"])
				classroom.students_in=Student.objects.filter(taxh=request.data["taxh"]).count()
				if classroom.students_in <= classroom.maximum :
						
						classroom.save()
						serializer=StudentSerializer(new_student)
						return Response(serializer.data)
				else: 
						student=Student.objects.get(student_id=serializer.data["student_id"])
						student.delete()
						return JsonResponse({'message':"You can't add more students in this classroom"},status=status.HTTP_400_BAD_REQUEST)
			else:
				return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)
	
	elif request.method=="DELETE":
		if request.user.role==1 :
			student_id=request.query_params.get("student_id",None)
			try:
				student=Student.objects.get(student_id=student_id)
				classroom=Classroom.objects.get(id=student.taxh.id)
				classroom.students_in=Student.objects.filter(taxh=student.taxh.id).count()
				classroom.save()
				student.delete()
				return JsonResponse({'message': ' Student  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
	
			except:
					return JsonResponse({'message': ' Student not found'}, status=status.HTTP_404_NOT_FOUND)		
		else:
			return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def student_update(request,id=''):
	if request.user.role!=2:
		if request.user.role==1:	
			try:
				student=Student.objects.get(student_id=id)
				classs=student.taxh.id
			
			except :
				return JsonResponse({'message': ' Student not found'}, status=status.HTTP_404_NOT_FOUND)
		elif request.user.role==3:
			student=Student.objects.get(student_id=request.user.id)	
			classs=student.taxh.id	
		
		data=JSONParser().parse(request)
		serializer=StudentSerializer(student,data=data)
		if serializer.is_valid():
			serializer.save()
			if classs!=serializer.data['taxh']:
				taxh=Classroom.objects.get(id=classs)
				taxh2=Classroom.objects.get(id=serializer.data['taxh'])
				taxh.students_in-=1
				taxh2.students_in=Student.objects.filter(taxh=serializer.data['taxh']).count()
				if taxh2.maximum < taxh2.students_in:
					student.taxh=taxh
					student.save()
				else:
					taxh.save()
					taxh2.save()
			return JsonResponse({'message': ' Student  UPDATED successfully!'}, status=status.HTTP_204_NO_CONTENT)
	
		
			
		return JsonResponse({'message': ' Bad request'}, status=status.HTTP_400_BAD_REQUEST)
	else:
		return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','DELETE'])
def classroom(request):
	if request.user.role==1:
		if request.method=="GET":
				id = request.query_params.get("id",None)
				classname=request.query_params.get("classname",None)
				class_number=request.query_params.get("class_number",None)
				
				if id  :
					classroom = Classroom.objects.filter(id=id)
				elif classname  and class_number :
					classroom = Classroom.objects.filter(classname=classname)
				elif classname  and class_number :
					classroom = Classroom.objects.filter(classname=classname,class_number=class_number)
				else :
					classroom = Classroom.objects.all()
				
				
				serializer=ClassroomSerializer(classroom,many=True)
				return Response(serializer.data)
		elif request.method=="POST":
				serializer=ClassroomSerializer(data=request.data)
		
				if serializer.is_valid():			
					serializer.save()
				return Response(serializer.data)
	
		elif request.method=="DELETE":
	
				id=request.query_params.get("id",None)
				try:
					classroom =Classroom.objects.get(id=id)
					classroom.delete()
					return JsonResponse({'message': ' Student  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
				except:
					return JsonResponse({'message' : 'Couldnts find classroom with that id'},status=status.HTTP_404_NOT_FOUND)
	else:
		return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)



@api_view(["PUT"])
def classroom_update(request,id):
	if request.user.role==1:
		try:
			classe=Classroom.objects.get(id=id)
		except:
			return JsonResponse({'message' : 'Couldnt find a class with that id'},status=status.HTTP_404_NOT_FOUND)
	
		data=JSONParser.parse(request.data)
		serializer=ClassroomSerializer(classe,data=data)
	
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
	
		return JsonResponse({'message':'Bad request'},status=status.HTTP_400_BAD_REQUEST)
	else:	
		return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET","POST","DELETE"])
def grade(request):
	if request.method=="GET":
		if request.user.role==1:			
			grade_id=request.query_params.get("id",None)
			student=request.query_params.get("student",None)
			Subject=request.query_params.get("subject",None)
			classroom=request.query_params.get("classroom",None)
			
			if classroom:
				grades=Grades.objects.filter(classroom=classroom)
	
			elif student and Subject :
				grades = Grades.objects.filter(student=student,subject_name=Subject)			
			elif Subject:
				grades = Grades.objects.filter(subject=Subject)
			elif student  :
				grades = Grades.objects.filter(student=student)
					
			elif grade_id:
				grades=Grades.objects.filter(id=grade_id)
			
			else :
				grades = Grades.objects.all()
			
		elif request.user.role==2:
			teacher=Teacher.objects.get(user=request.user)
			student=request.query_params.get("student",None)
			Subject=request.query_params.get("subject_name",None)
			classroom=request.query_params.get("classroom",None)
			if student and Subject:
				grades=Grades.objects.filter(teacher=teacher.teacher_id,student=student.student_id,subject_name=Subject)
			elif student:
				grades=Grades.objects.filter(teacher=teacher.teacher_id,student=student.student_id)
					
			elif classroom and Subject :
				grades=Grades.objects.filter(teacher=teacher.teacher_id,classroom=classroom,subject_name=Subject)

			elif Subject :
				grades=Grades.objects.filter(teacher=teacher.teacher_id,subject_name=Subject)
			elif classroom :
				grades=Grades.objects.filter(teacher=teacher.teacher_id,classroom=classroom)	
			else:
				grades=Grades.objects.filter(teacher=teacher.teacher_id)

		else:
			student=Student.objects.get(user=request.user)
			
			Subject=request.query_params.get("subject_name",None)
			classroom=request.query_params.get("classroom",None)
			if Subject :
				grades=Grades.objects.filter(student=student,subject_name=Subject)
			elif classroom:
				grades=Grades.objects.filter(student=student,classroom=classroom)
			else:
				grades=Grades.objects.filter(student=student)
		serializer=GradesSerializer(grades,many=True)
				
		return Response(serializer.data)	

	elif request.method=="POST":
			if request.user.role==1:
				serializer=GradesSerializer(data=request.data)
				if serializer.is_valid():			
					
					student=Student.objects.get(student_id=request.data["student"])
					sub=subject.objects.get(subject_id=request.data["subject_name"])
					if student.taxh==sub.taxh:
							serializer.data["classroom"]=student.taxh
							serializer.save()
							return Response(serializer.data)
					else:
							return JsonResponse({"message":"This subject is not in student classroom"},status=status.HTTP_400_BAD_REQUEST)
				return JsonResponse({"message":"This grade already exists"},status=status.HTTP_400_BAD_REQUEST)
			elif request.user.role==2:
					subject=request.data['subject_name']
					student=request.data['student']
					teacher=Teacher.objects.get(user=request.user)
					Subject=subject.objects.get(subject_id=request.data["subject"])
					Student=Student.objects.get(student_id=request.data['id'])
					try:
						if Subject.taxh ==student.taxh and subject.teacher == teacher.teacher_id :
							grades=Grades.objects.create(student=student.student_id,subject_name=Subject.subject_id,teacher=teacher.id,classroom=Subject.taxh,grade=request.data["grade"])
						else :
							return JsonResponse({"message":"No permissions"},status=status.HTTP_400_BAD_REQUEST)
					except:
							return JsonResponse({"message":"Bad request"},status=status.HTTP_400_BAD_REQUEST)



	elif request.method=="DELETE":
			if request.user.role==1:
				id=request.query_params.get("id",None)
				try:
					grades =Grades.objects.get(id=id)
					grades.delete()
					return JsonResponse({'message': ' Grades  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
				except:
					return JsonResponse({'message' : 'Couldnts find Grades with that id'},status=status.HTTP_404_NOT_FOUND)	
			else:
				return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def grade_update(request,id):
	if request.user.role==1:
		try:
			grade=Grades.objects.get(id=id)
		except:
			return JsonResponse({'message' : 'Couldnt find a Grade with that id'},status=status.HTTP_404_NOT_FOUND)
	
		data=JSONParser.parse(request.data)	
		serializer=GradesSerializer.parse(grade,data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
	
		return JsonResponse({'message':'Bad request'},status=status.HTTP_400_BAD_REQUEST)

	

@api_view(["GET","POST","DELETE"])
def SSubject(request):
	
		if request.method=="GET":
				
				teacher=request.query_params.get("teacher",None)
				onoma=request.query_params.get("onoma",None)
				taxh=request.query_params.get("taxh",None)
				subject_id=request.query_params.get("subject_id",None)
				if teacher  :
					Subject = subject.objects.filter(teacher=teacher)
					
				elif onoma  and taxh :
					Subject = subject.objects.filter(onoma=onoma,taxh=taxh)	
			
				elif onoma  :
					Subject = subject.objects.filter(onoma=onoma)	
				
				elif subject_id :
					Subject = subject.objects.filter(subject_id=subject_id)					
				else :
					Subject = subject.objects.all()
	
				serializer=SubjectSerializer(grades,many=True)
				return Response(serializer.data)
			
		
		elif request.user.role==1 and request.method != "GET":
			if request.method=="POST":
					serializer=SubjectSerializer(data=request.data)
					
					if serializer.is_valid():			
						serializer.save()
					return Response(serializer.data)
		
		
			elif request.method=="DELETE":
					subject_id=request.query_params.get("subject_id",None)
					try:
						Subject =subject.objects.get(subject_id=subject_id)
						Subject.delete()
						return JsonResponse({'message': ' Subject  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
					except:
						return JsonResponse({'message' : 'Couldnts find Subject with that id'},status=status.HTTP_404_NOT_FOUND)
		else:

			return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def subject_update(request,id):
	if request.user.role==1:
		try:
			subj=subject.objects.get(subject_id=id)
		except:
			return JsonResponse({'message':'Subject not found'},status=status.HTTP_404_NOT_FOUND)
	
		data=JSONParser.parsers(request.data)
		serializer=SubjectSerializer(subj,data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
	
		return JsonResponse({'message':'Bad request'},status=status.HTTP_400_BAD_REQUEST)
	else:
		return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)





@api_view(["GET","POST","DELETE"])
def teacher(request):
	if request.method=="GET":
			first_name=request.query_params.get("first_name",None)
			last_name=request.query_params.get("last_name",None)
			teacher_id=request.query_params.get("teacher_id",None)
			if first_name and last_name:
				teacher = Teacher.objects.filter(first_name=first_name,last_name=last_name)
				
			elif teacher_id :
						teacher = Teacher.objects.filter(teacher_id=teacher_id,last_name=last_name)
			else :
				teacher=teacher.objects.all()
		
	
			serializer=SubjectSerializer(teacher,many=True)
			return Response(serializer.data)		


	elif request.method=="POST":
			data=request.data
			if request.user.role==2:
				new_user=request.user
			elif request.user.role==1:
				new_user=data["user"]
			else:
				return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)


			new_Teacher=Teacher.objects.create(user=new_user,first_name=data["first_name"],last_name=data["last_name"],phone=data["phone"],email=data["email"])		
			

			if new_Teacher:
				new_Teacher.save()
		
			serializer=TeacherSerializer(new_Teacher)
			return Response(serializer.data)
	
	elif request.method=="DELETE":
			if request.user.role==2:
				teacher_id=Teacher.objects.get(user=request.user)
			elif request.user.role==1:
				teacher_id=request.query_params.get("teacher_id",None)
			else:
				return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)

			try:
				teacher =Teacher.objects.get(teacher_id=teacher_id)
				teacher.delete()
				return JsonResponse({'message': ' teacher  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
			except:
				return JsonResponse({'message' : 'Couldnts find teacher with that id'},status=status.HTTP_404_NOT_FOUND)




@api_view(["PUT"])
def teacher_update(request,id):
	if request.user.role==1:
		try:
			teacher=Teacher.objects.get(teacher_id=id)
		except:
			return JsonResponse({'message':'Teacher not found'},status=status.HTTP_404_NOT_FOUND)
	elif request.uer.role==2:
		teacher=Teacher.objects.get(user=request.user)
	else:
		return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)

	data=JSONParser.parsers(request.data)
	serializer=TeacherSerializer(teacher,data=data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)

	return JsonResponse({'message':'Bad request'},status=status.HTTP_400_BAD_REQUEST)