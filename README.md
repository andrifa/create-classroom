# My Version Google Classroom Server

creating simple version of google classroom server using flask as the framework, JSON as data format, and insomnia as REST Client 

## Preparation :
> ### Install Python
``` 
> > pip install pyhton
```
> ### Install Flask
```
> > pip install flask
```
> ### Install Insomnia 
```
> > Install Insomnia REST Client from https://insomnia.rest/
```

## Features and User Input:
> ### USER REGISTER
Open insomnia create a request POST to `/daftar` with JSON body
```
{
	"username": "adziima",
	"password": "ccc",
	"fullname": "adziima",
	"user id": 3,
	"email": "adziima@gmail.com"
}
```
> ### USER LOGIN / VALIDATION
Open insomnia create a request POST to `/validasi` with JSON body
```
{
	"username":"andrisan",
	"password":"a1a1a1"
}
```
> ### USER UPDATE DATA
Open insomnia create a request PUT to `/daftar/<int:userid>` with JSON body
```
{
    "email": "andrisan@gmail.com",
    "fullname": "andrisan",
    "password": "a1a1a1",
    "username": "andrisan"
}  
```
> ### CREATE CLASS
Open insomnia create a request POST to `/class` with JSON body
```
{
	"classname":"Backend Beneran",
	"classid":1,
	"teachers":[3]
}
```
> ### UPDATE CLASS
Open insomnia create a request PUT to `/class/<int:classid>` with JSON body
```
{
	"classname":"frontend expert"
}
```
> ### USER JOIN CLASS
Open insomnia create a request POST to `/joinClass` with JSON body
```
{
	"user id": 2,
	"classid": 1
}
```
> ### USER LEAVE CLASS
Open insomnia create a request DELETE to `/outclass` with JSON body
```
{
	"user id": 2,
	"classid": 1
}
```
> ### TEACHER ADD CLASSWORK
Open insomnia create a request POST to `/class/<int:classid>` with JSON body
```
{
	"classworkid":2,
	"question":"1+1?"
}
```
> ### TEACHER UPDATE QUESTION IN CLASSWORK
Open insomnia create a request PUT to `/classwork/<int:classworkid>` with JSON body
```
{
	"question":"berapa 4/4?"
}
```
> ### STUDENT ASSIGN CLASSWORK
Open insomnia create a request POST to `/classwork/<int:classworkid>` with JSON body
```
{
	"user id": 1,
	"answer":"1"
}
```
> ### GET USER DATA
Open insomnia create a request GET from `/getUser/<int:n>` or `/getUser/all`
> ### GET CLASS DATA
Open insomnia create a request GET from `/getClass/<int:n>` or `/getClass/all`
> ### GET CLASSWORK DATA
Open insomnia create a request GET from `/getClassWork/<int:n>` or `/getClassWork/all`
> ### REMOVE CLASSWORK by CLASSWORKID
Open insomnia create a request DELETE from `/classwork/<int:classworkid>` without any JSON Data input
> ### REMOVE CLASS by CLASSID
Open insomnia create a request DELETE from `/class/<int:classid>` without any JSON Data input
> 



