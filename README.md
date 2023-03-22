# School system Rest api

**Endpoints :**


**Students :**
>api/student/ Methods = [GET,POST,DELETE]
>
>api/student/<student_id>/ METHODS [PUT]
>
>query_params : student_id,classroom
for delete :by id

json format :
```json
{
        "classroom": 1,
        "first_name": "test",
        "last_name": "test",
        "phone": "6666666",
        "email": "test@gmail.com",
        "photo": "/media/student_pics/default.png",
        "apousies": 1,
        "user": 3
 }  
```
**Classroom**
>api/classroom/  Methods = [GET,POST,DELETE]
>
>api/classroom/<classroom_Id> Methods = [PUT]
>
>query_params = id ,classname,class_number
>
>for delete by id

json format :
```json
    {
        "id": 1,
        "classname": "A",
        "class_number": 1,
        "maximum": 42,
        "students_in": 3
    }
```

**Grades**
>api/grade/ Methods = [GET,POST,DELETE]
> 
>api/grade/update/<int:id>/ Methods = [PUT]
>
>api/grade/csv/ Methods = [POST,PUT]
>
>(the csv file , subject_id)
>
>query_params = student,classroom,subject_name(id)
>
>for delete by id

```json
{
        "id": 1,  
        "grade": 97,
        "student": 1,
        "subject_name" : 1,
        "teacher" : 1,
        "classroom" : 1
  }   
```
##Subjects
>api/subject/ Methods = [GET,POST,DELETE]
>
>api/subject/update/<int:id>/ Methods = [PUT]
>
>query_parms = teacher,classroom(id),onoma,subject_id
>
>for delete by id

Json format :
```json
 {
        "subject_id": 1,
        "teacher": 1,
        "classroom": 1,
        "onoma": "Mathimatika"
 }

```
**Teachers**
>api/teacher/ Methods = [GET,POST,DELETE]
>
>api/teacher/update/<int:id>/ Methods = [PUT]
>
>query_params = first_name , last_name , teacher_id
>
>For delete by id


Json format :
```json
    {
        "first_name": "Kostasa",
        "last_name": "Damianos",
        "phone": "692022012",
        "email": "test@gmail.com",
        "user": 2
    }
```
**Assigments**
>api/assigment/  Methods = [GET,POST,DELETE]
>
>apiassigment/update/<int:id>  Methods = [PUT]
>
>query_params = teacher(id), classroom(id), id , subject(id)
>
>for delete by id

Json format :
```json
{
        "id": 2,
        "subject":1,
        "pdf_question": "/media/assigments/asddasasqqwqwe.pdf",
        "deadline": "2023-03-23",
        "title": "MASTORILIKIA",
        "question": "KANTE KATI RE ALANIA !"
        "teacher": 3,
        "classroom" :3       
}
```
**StudentAssigments**
>api/student/assigment/ Methods = [POST,GET,DELETE]
>
>api/student/assigment/addgrade/<int:id>/ Methods = ["PUT"] (in put data you add the score and in the id the student assigment id)
>
>query_params = id,assigment,student
>
>for delete by id 
    
Json format :
```json    
    {
        "id": 2,
        "file": "/media/student_assigments/ffsddfs%CF%85.pdf",
        "score": 77,
        "student": 3,
        "assignment": 3
    }

``` 
**Announcements**
>api/announcements/ Methods = [GET,POST,DELETE]
>
>api/announcement/update/<int:id> Methods = [PUT]
>
>query_args : id


```json

{
        "id": 1,
        "publisher": 1,
        "title": "qqqq",
        "content": "qqqq",
        "image_post": "/media/post_images/PP.png",
}

```
        
 **Other** 
>api/getrole/ Methods = [GET] It returns the role of the user logined 
>
>api/getusername/ Methods = [GET] It returns the username of the user

    




