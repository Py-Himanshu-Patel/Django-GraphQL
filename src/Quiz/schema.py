import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Category, Question, Answer, Quiz


class CategoryType(DjangoObjectType):
	class Meta:
		model = Category
		fields = ('id', 'name')


class QuizzesType(DjangoObjectType):
	class Meta:
		model = Quiz
		fields = ('id', 'title', 'category', 'quiz')


class QuestionType(DjangoObjectType):
	class Meta:
		model = Question
		fields = ('title', 'quiz')


class AnswerType(DjangoObjectType):
	class Meta:
		model = Answer
		fields = ('question', 'answer_text')

class Query(graphene.ObjectType):
	# quiz = graphene.String()
	# def resolve_quiz(root, info):
	# 	return "Dummy Text"

	all_quizzes = DjangoListField(QuizzesType)
	all_questions = DjangoListField(QuestionType)

	def resolve_all_quizzes(root, info):
		return Quiz.objects.all()

	def resolve_all_questions(root, info):
		return Question.objects.all()


schema = graphene.Schema(query=Query)
