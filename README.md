# Django-GraphQL

Using GraphQL in Django. Big Thanks to [Very Academy YouTube Channel](https://www.youtube.com/playlist?list=PLOLrQ9Pn6caxz00JcLeOR-Rtq0Yi01oBH)

[Graphene-Django Official Documentation](https://docs.graphene-python.org/projects/django/en/latest/installation/)

***

## Commands and Scripts

### Setup Virtual Environment

To setup env

```bash
mkdir .venv
pipenv shell
```

To install the Pipfile

```bash
pipenv install
```

***

### Get graphene

[graphene-django](https://pypi.org/project/graphene-django/) - A Django integration for Graphene.  

```bash
pipenv install graphene-django
```

### Make an app and setup schema for graphene

```bash
(Django-GraphQL) himanshu in src: django-admin startapp MyApp
(Django-GraphQL) himanshu in src: cd MyApp
(Django-GraphQL) himanshu in MyApp: touch schema.py
```

### Create a model

***MyApp/models.py***

```python
class Book(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()

    def __str__(self) -> str:
        return self.title
```

### Create a Schema for that model

***MyApp/schema.py***

```python
import graphene
from graphene_django import DjangoObjectType
from .models import Book

# a serializer like django object that specify 
# model and it's fields for query purpose
class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ('id', 'title', 'summary')

# specify query by providing it the django object we made
class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)

    # create a method starting with resolve
    def resolve_all_books(root, info):
        return Book.objects.all()

# specify the query for this schema
schema = graphene.Schema(query=Query)
```

### Use graphene default view to provide GUI to make query

***MyApp/urls.py***

```python
from django.urls import path
from graphene_django.views import GraphQLView
import graphql
from MyApp.schema import schema

urlpatterns = [
    # instead of defining schema here we can define a default schema in settings.py
    path("books/", GraphQLView.as_view(graphiql=True, schema=schema))
]
```

***MyProject/urls.py***

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MyApp.urls')),
]
```

### Make a GraphQL query

Visit: [http://127.0.0.1:8000/books/](http://127.0.0.1:8000/books/) And make a graphQL query

```graphql
query{
  allBooks {
    id
    title
  }
}
```

The Result

```json
{
  "data": {
    "allBooks": [
      {
        "id": "1",
        "title": "7 Habit of Highly Non Effective People"
      },
      {
        "id": "2",
        "title": "Django Mens"
      },
      {
        "id": "3",
        "title": "React Boys"
      }
    ]
  }
}
```

### Passing GraphQL query in URL instead of using GUI for query

Make the `graphiql` to `False` and GUI is gone.

```python
# in App/urls.py
path("books/", GraphQLView.as_view(graphiql=False, schema=schema))
```

Now we query using URL as follow

```url
http://127.0.0.1:8000/books/?query=query{allBooks{id,title}}
```

Here the prefix is the same URL as previous

```url
http://127.0.0.1:8000/books/
```

We just passed query as

```graphql
query{allBooks{id,title}}
```

Response is also same

```json
{"data":{"allBooks":[{"id":"1","title":"7 Habit of Highly Non Effective People"},{"id":"2","title":"Django Mens"},{"id":"3","title":"React Boys"}]}}
```

***

### Making even more comples queries

#### Make models

[Quiz/models.py](src/Quiz/models.py)

```python
# quiz/models.py

class Category(models.Model):
    ...

class Quiz(models.Model):
    ...

class Question(models.Model):
    ...

class Answer(models.Model):
    ...
```

#### Make schema

[Quiz/schema.py](src/Quiz/schema.py)

```python
import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Category, Question, Answer, Quiz


class CategoryType(DjangoObjectType):
    ...

class QuizzesType(DjangoObjectType):
    ...

class QuestionType(DjangoObjectType):
    ...

class AnswerType(DjangoObjectType):
    ...

# define query root which will be searched for each graphQL query
# to make a get query on already existing data in server
class Query(graphene.ObjectType):
    # DjangoListField give list of all objects in model
    all_quizzes = DjangoListField(QuizzesType)
    all_questions = DjangoListField(QuestionType)

    # can be used to further refine DjangoListField output
    def resolve_all_quizzes(root, info):
        return Quiz.objects.all()

    def resolve_all_questions(root, info):
        return Question.objects.all()

schema = graphene.Schema(query=Query)
```

#### Make query and get response

##### Query

```graphql
query{
  allQuizzes {
    title
  }
  
  allQuestions{
    title
  }
}
```

##### Response

```json
{
  "data": {
    "allQuizzes": [
      {
        "title": "First Quiz"
      },
      {
        "title": "Second Quiz"
      },
      {
        "title": "Third Quiz"
      }
    ],
    "allQuestions": [
      {
        "title": "Is Spring the most famous framework?"
      }
    ]
  }
}
```

We can request only those field which are declared in `QuizzesType` and `QuestionType`.

#### Modify schema to get a single object or a list

```python
# Quiz/schema.py

# to make a get query on already existing data in server
class Query(graphene.ObjectType):
    # returns all objects in models
    # all_quizzes = DjangoListField(QuizzesType)

    # get the request quiz or question list
    get_quiz = graphene.Field(QuizzesType, quiz_id=graphene.Int())
    get_questions = graphene.List(QuestionType, ques_id=graphene.Int())

    # get_questions is List so need an iterable
    def resolve_get_questions(root, info, ques_id):
        # all questions with id > ques_id
        return Question.objects.filter(pk__gt=ques_id)

    # get_quiz is Field so need a single instance
    def resolve_get_quiz(root, info, quiz_id):
        return Quiz.objects.get(pk=quiz_id)
```

##### Query

```graphql
query{
  getQuiz(quizId:1){
    title
  }
  getQuestions(quesId:2){
    title
  }
}
```

##### Response

```json
{
  "data": {
    "getQuiz": {
      "title": "First Quiz"
    },
    "getQuestions": [
      {
        "title": "Is Django the best framework for backend"
      }
    ]
  }
}
```

Notice the use of `quizId` and `quesId` in query.

#### Modify schema to get answers related to a particular question

```python
# to make a get query on already existing data in server
class Query(graphene.ObjectType):
    # get the request question and all it's answers
    get_all_answers = graphene.List(AnswerType, ques_id=graphene.Int())
    get_question = graphene.Field(QuestionType, ques_id=graphene.Int())

    def resolve_get_question(root, info, ques_id): 
        return Question.objects.get(pk=ques_id)

    def resolve_get_all_answers(root, info, ques_id):
        return Answer.objects.filter(question__pk=ques_id)
```

##### Query

 ```graphql
 {
  getQuestion(quesId: 1) {
    title
  }
  getAllAnswers(quesId: 1) {
    answerText
  }
}
```

OR using variables

```graphql
 query GetQuesAns($id: Int = 1){
  getQuestion(quesId: $id) {
    title
  }
  getAllAnswers(quesId: $id) {
    answerText
  }
}
 ```

##### Response

Notice the difference in response type. `getQuestion` gives object while `getAllAnswers` gives a list.

```json
{
  "data": {
    "getQuestion": {
      "title": "Is Spring the most famous framework?"
    },
    "getAllAnswers": [
      {
        "answerText": "NO, ofcourse not."
      },
      {
        "answerText": "As usual. It Depends"
      }
    ]
  }
}
```

***

### GraphQL CRUD with Django

#### Create an instance in database

Add this class in schema.py.

```python
...

class CategoryMutation(graphene.Mutation):
    # define the argument type we want to accept and 
    # then pass this arguments in mutate() function
    class Arguments:
        name = graphene.String(required=True)
        # .. add more fields here as arg

    # define the category type
    category = graphene.Field(CategoryType)

    # name argument to accept the name passed by frontend
    # add more arg here which we declared in Arguments
    @classmethod
    def mutate(cls, root, info, name):	
        category = Category(name=name)
        category.save()
        return CategoryMutation(category=category)

# to mutate data in server and also rell 
# frontend that server accept mutation requst
class Mutation(graphene.ObjectType):
    update_category = CategoryMutation.Field()


# mutation parameter let frontend know that mutation query are 
# accepted and how the are connected (via Mutation class)
schema = graphene.Schema(query=Query, mutation=Mutation)
```

#### Create Mutation with Response

Query: Here name we gave to mutation (CategoryMutation) can be anything it's not related to server side coding.

```graphql
mutation CategoryMutation{
  updateCategory(name:"NewCategory"){
    category{
      name
    }
  }
}
```

Response

```json
{
  "data": {
    "updateCategory": {
      "category": {
        "name": "NewCategory"
      }
    }
  }
}
```

#### Update an instance in database

Just change the Mutation class as follows and rest all same as previous Mutation. Don't forget to comment out or delete previous class with same name.

```python
class CategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return CategoryMutation(category=category)
```

#### Update Mutation with response

```graphql
mutation UpdateCategory{
  updateCategory(id:4, name: "UpdatedCategory"){
    category{
      id
      name
    }
  }
}
```

```json
{
  "data": {
    "updateCategory": {
      "category": {
        "id": "4",
        "name": "UpdatedCategory"
      }
    }
  }
}
```

#### Create and Update together

```python
class CategoryCreate(graphene.Mutation):
    # define the argument type we want to accept and 
    # then pass this arguments in mutate() function
    class Arguments:
        name = graphene.String(required=True)
        # .. add more fields here as arg

    # define the category type
    category = graphene.Field(CategoryType)

    # name argument to accept the name passed by frontend
    # add more arg here which we declared in Arguments
    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryCreate(category=category)


class CategoryUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return CategoryUpdate(category=category)

# to mutate data in server and also rell 
# frontend that server accept mutation requst
class Mutation(graphene.ObjectType):
    update_category = CategoryUpdate.Field()
    create_category = CategoryCreate.Field()


# mutation parameter let frontend know that mutation query are 
# accepted and how the are connected (via Mutation class)
schema = graphene.Schema(query=Query, mutation=Mutation)
```

#### Create and Update Mutation with response

```graphql
mutation CreateCategory {
  createCategory(name: "LatestCategory") {
    category {
      id
      name
    }
  }

  updateCategory(id: 5, name: "ModifiedCategory") {
    category {
      id
      name
    }
  }
}
```

```json
{
  "data": {
    "createCategory": {
      "category": {
        "id": "6",
        "name": "LatestCategory"
      }
    },
    "updateCategory": {
      "category": {
        "id": "5",
        "name": "ModifiedCategory"
      }
    }
  }
}
```

#### Delete Mutation

```python
# to delete the object from database
class CategoryDelete(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id)
        category.delete()

class Mutation(graphene.ObjectType):
    update_category = CategoryUpdate.Field()
    create_category = CategoryCreate.Field()
    delete_category = CategoryDelete.Field()
```

#### Delete Mutation with request and response

```graphql
mutation CreateCategory {
  deleteCategory(id: 11){
    category{
      id
    }
  }
}
```

```json
{
  "data": {
    "deleteCategory": null
  }
}
```

***

### User Management with GraphQL

- Login
- Logout
- Authenticate
- Signup Email Confirmation
- Change Password
- Forgot password - via email confirm
- Delete Account
- Update account details

#### Make custom user

Make new `users` app and include it in INSTALLED_APPS.

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # making email field compulsory
    email = models.EmailField(blank=False, max_length=100, verbose_name="email")
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
```

Uncomment the auth model and specify abstract user in settings.

```python
# settings.py

INSTALLED_APPS = [
    # 'django.contrib.admin',
    ...
]

# Cutome User Model
AUTH_USER_MODEL = 'users.CustomUser'

```

Run `python manage.py makemigrations` and `python manage.py migrate`. After this uncomment `django.contrib.admin`

#### Setup GraphQL and JWT

[Install Graphene](https://docs.graphene-python.org/projects/django/en/latest/installation/): `pip install graphene-django`

[Install Django Graphene JWT](https://django-graphql-jwt.domake.io/en/latest/quickstart.html#installation): `pip install django-graphql-jwt`

[Install Django GraphQL Auth](https://pypi.org/project/django-graphql-auth/) `pip install django-graphql-auth`

Modify `settings.py` as

```python
INSTALLED_APPS = [
    ...
    # third party
    'graphene_django',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
    'graphql_auth',
    # local apps
    'users',
]

GRAPHENE = {
    'SCHEMA': 'users.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

AUTHENTICATION_BACKENDS = [
    # 'graphql_jwt.backends.JSONWebTokenBackend',
    "graphql_auth.backends.GraphQLAuthBackend",
    'django.contrib.auth.backends.ModelBackend',
]
```

Run **makemigrations** and **migrate**.

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Setup django for JWT

```python
# users/admin.py

from django.apps import apps
# get some specific app
app = apps.get_app_config('graphql_auth')
for model_name, model in app.models.items():
    admin.site.register(model)
```

```python
# Project/urls.py
...
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    ...
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True)) )
]

```

#### Setup Schema for GraphQL

Create a `schema.py` file in users app.

```python
# users/schema.py
import graphene
from graphene.types import schema
from graphql_auth.schema import UserQuery, MeQuery

class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
```

#### Go and make a query

```graphql
query{
  users{
    edges{
      node{
        username
      }
    }
  } 
}
```

```json
{
  "data": {
    "users": {
      "edges": [
        {
          "node": {
            "username": "hp"
          }
        }
      ]
    }
  }
}
```

Using `me` query

```graphql
query{
  me{
    username
  }
}
```

```json
{
  "data": {
    "me": {
      "username": "hp"
    }
  }
}
```

#### Define email backend and user authentication

Instead of sending email using SMTP we send email to console.

```python
# settings.py
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# JWT config
GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
    ],
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
}
```

```python
# schema.py
import graphene
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()

class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
```

```graphql
mutation{
  register(
    email: "admin@email.com"
    username: "admin"
    password1: "admin@1234"
    password2: "admin@1234"
  ){
    success
    errors
    token
    refreshToken
  }
}
```

```json
{
  "data": {
    "register": {
      "success": true,
      "errors": null,
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjE5ODE5MTg5LCJvcmlnSWF0IjoxNjE5ODE4ODg5fQ.Qvj7GqN5vkkrQLah-g-n06DMZKHg0WkDUCdnx_gxMys",
      "refreshToken": "da3aba7e87c4796b813765a2b13aad3970aff78d"
    }
  }
}
```

The user registered here have received an email. To verifiy user click of the link provided in email. Here we receive it inside console. Or verify the user from admin panel. Goto `User Status` table and check `Verified` status for user.

Also if email is lost or not delivered resend email using this setting

```python
GRAPHQL_JWT = {
    ...
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ResendActivationEmail",
        "graphql_auth.mutations.ObtainJSONWebToken",
        "graphql_auth.mutations.SendPasswordResetEmail",
    ],
    ...
}
```

```python
class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
```

Make a query to resend email.

```graphql
mutation{
  resendActivationEmail(email: "admin@email.com") {
    success
    errors
  }
}
```

```json
{
  "data": {
    "resendActivationEmail": {
      "success": true,
      "errors": null
    }
  }
}
```

Pick up the activation code from email

```html
<h3>127.0.0.1:8000</h3>

<p>Hello admin!</p>

<p>Please activate your account on the link:</p>

<p>http://127.0.0.1:8000/activate/eyJ1c2VybmFtZSI6ImFkbWluIiwiYWN0aW9uIjoiYWN0aXZhdGlvbiJ9:1lchYb:oZPH7xZajyJJ9t2SvIyGTLnzHlxLz70lNnfMUFx-qVc</p>
```

copy code: `eyJ1c2VybmFtZSI6ImFkbWluIiwiYWN0aW9uIjoiYWN0aXZhdGlvbiJ9:1lchYb:oZPH7xZajyJJ9t2SvIyGTLnzHlxLz70lNnfMUFx-qVc`

Now verify account using 

```graphql
mutation{
  verifyAccount(
    token: "eyJ1c2VybmFtZSI6ImFkbWluIiwiYWN0aW9uIjoiYWN0aXZhdGlvbiJ9:1lchYb:oZPH7xZajyJJ9t2SvIyGTLnzHlxLz70lNnfMUFx-qVc"
  ) {
    success
    errors
  }
}
```

```json
{
  "data": {
    "verifyAccount": {
      "success": true,
      "errors": null
    }
  }
}
```

Also try to login using the verified user.

```graphql
mutation{
  tokenAuth(username: "admin", password: "admin@1234"){
    success
    errors
    token
    refreshToken
    user {
      id
      username
      email
    }
  }
}
```

```json
{
  "data": {
    "tokenAuth": {
      "success": true,
      "errors": null,
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjE5ODUzNDA3LCJvcmlnSWF0IjoxNjE5ODUzMTA3fQ.3Iw8iG5bxsNbsFgfKEGIfm81bUZo3OD5AO28XnhVboc",
      "refreshToken": "16962e695560333389441a0fdab49e7d1b9fba36",
      "user": {
        "id": "VXNlck5vZGU6NQ==",
        "username": "admin",
        "email": "admin@email.com"
      }
    }
  }
}
```

This is also use full when we want to request some data as if the user is logged in.
Then pass the user creadentials and `user{}` query with `user details` we required.

#### Modify user and pass JWT token

Using header of GraphQL UI I could not find any way to pass JWT token in POST request. So I used Postman.

Making this request to update `username` of user.

```graphql
mutation{
  updateAccount(firstName: "HP"){
    success
    errors
  }
}
```

This gives a response

```json
{
  "errors": [
    {
      "message": "CustomUser has no status.",
      "locations": [
        {
          "line": 2,
          "column": 3
        }
      ],
      "path": [
        "updateAccount"
      ]
    }
  ],
  "data": {
    "updateAccount": null
  }
}
```

This do not updated the either the loggined user or user whose JWT we are trying to pass anyway.

Make a Post request using Postman without passing `authentication` in header.

```graphql
mutation{
  updateAccount(firstName: "ADMIN"){
    success
    errors
  }
}
```

Response

```json
{
    "data": {
        "updateAccount": {
            "success": false,
            "errors": {
                "nonFieldErrors": [
                    {
                        "message": "Unauthenticated.",
                        "code": "unauthenticated"
                    }
                ]
            }
        }
    }
}
```

Now pass the JWT of `admin` custom user we made.

Authorization: OAuth2.0 with `JWT <jwt-token-here>`

```json
{
    "data": {
        "updateAccount": {
            "success": true,
            "errors": null
        }
    }
}
```

This updated the first name of the user whose JWT we given.

#### Password reset email

```python
# settings.py
GRAPHQL_JWT = {
  ...
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ResendActivationEmail",
        "graphql_auth.mutations.ObtainJSONWebToken",
        "graphql_auth.mutations.SendPasswordResetEmail",
    ],
  ...
}
```

```python
# schema.py
class AuthMutation(graphene.ObjectType):
  register = mutations.Register.Field()
  verify_account = mutations.VerifyAccount.Field()
  resend_activation_email = mutations.ResendActivationEmail.Field()
  token_auth = mutations.ObtainJSONWebToken.Field()
  update_account = mutations.UpdateAccount.Field()
  send_password_reset_email = mutations.SendPasswordResetEmail.Field()
  password_reset = mutations.PasswordReset.Field()
```

```graphql
mutation{
   sendPasswordResetEmail(email: "admin@email.com"){
    success
    errors
  }
}
```

```json
{
  "data": {
    "sendPasswordResetEmail": {
      "success": true,
      "errors": null
    }
  }
}
```

Pick up the password reset link

```html
<h3>127.0.0.1:8000</h3>

<p>Hello admin!</p>

<p>Reset your password on the link:</p>

<p>http://127.0.0.1:8000/password-reset/eyJ1c2VybmFtZSI6ImFkbWluIiwiYWN0aW9uIjoicGFzc3dvcmRfcmVzZXQifQ:1lcmcv:9bYIJAWdTCiXKAWxbNS2lHl9FzIw1PGUq_gpq-__Z-4</p>
```

Reset token `eyJ1c2VybmFtZSI6ImFkbWluIiwiYWN0aW9uIjoicGFzc3dvcmRfcmVzZXQifQ:1lcmcv:9bYIJAWdTCiXKAWxbNS2lHl9FzIw1PGUq_gpq-__Z-4`

```graphql
mutation{
  passwordReset(token: "eyJ1c2VybmFtZSI6ImFkbWluIiwiYWN0aW9uIjoicGFzc3dvcmRfcmVzZXQifQ:1lcmcv:9bYIJAWdTCiXKAWxbNS2lHl9FzIw1PGUq_gpq-__Z-4"
  , newPassword1: "admin@4321"
  , newPassword2: "admin@4321"  
  ){
    success
    errors
  }
} 
```

```python
{
  "data": {
    "passwordReset": {
      "success": true,
      "errors": null
    }
  }
}
```

Password reset successful.
