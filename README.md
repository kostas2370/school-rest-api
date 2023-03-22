# School system Rest api

**Endpoints :**
*Students :*
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










 
 
        
    




