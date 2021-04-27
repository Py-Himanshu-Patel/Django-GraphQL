from django.db import models
import graphene
from graphene.types.scalars import Int
from graphene_django import DjangoObjectType, DjangoListField
from .models import Category, Question, Answer, Quiz


class CategoryType(DjangoObjectType):
	class Meta:
		model = Category
		fields = ('id', 'name')


class QuizzesType(DjangoObjectType):
	class Meta:
		model = Quiz
		fields = ('id', 'title', 'category')


class QuestionType(DjangoObjectType):
	class Meta:
		model = Question
		fields = ('title', 'quiz')


class AnswerType(DjangoObjectType):
	class Meta:
		model = Answer
		fields = ('question', 'answer_text')


class Query(graphene.ObjectType):
	# get the request question and all it's answers
	get_all_answers = graphene.List(AnswerType, ques_id=graphene.Int())
	get_question = graphene.Field(QuestionType, ques_id=graphene.Int())

	def resolve_get_question(root, info, ques_id): 
		return Question.objects.get(pk=ques_id)

	def resolve_get_all_answers(root, info, ques_id):
		return Answer.objects.filter(question__pk=ques_id)


schema = graphene.Schema(query=Query)
