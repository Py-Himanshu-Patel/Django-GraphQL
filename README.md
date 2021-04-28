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

```json
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

 ```json
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

```json
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

```json
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

```json
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

```json
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
