# Django-GraphQL

Using GraphQL in Django. Big Thanks to [Very Academy YouTube Channel](https://www.youtube.com/playlist?list=PLOLrQ9Pn6caxz00JcLeOR-Rtq0Yi01oBH)

[Graphene-Django Official Documentation](https://docs.graphene-python.org/projects/django/en/latest/installation/)

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

```json
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

```http
http://127.0.0.1:8000/books/?query=query{allBooks{id,title}}
```

Here the prefix is the same URL as previous

```http
http://127.0.0.1:8000/books/
```

We just passed query as

```http
query{allBooks{id,title}}
```

Response is also same

```json
{"data":{"allBooks":[{"id":"1","title":"7 Habit of Highly Non Effective People"},{"id":"2","title":"Django Mens"},{"id":"3","title":"React Boys"}]}}
```

### Making even more comples queries

#### Make models

[models.py](src/Quiz/models.py)

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

[schema.py](src/Quiz/schema.py)

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

```json
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
