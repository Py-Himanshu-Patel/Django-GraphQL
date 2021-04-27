import graphene
from graphene_django import DjangoObjectType
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


# to make a get query on already existing data in server
class Query(graphene.ObjectType):
	# get the request question and all it's answers
	get_all_answers = graphene.List(AnswerType, ques_id=graphene.Int())
	get_question = graphene.Field(QuestionType, ques_id=graphene.Int())

	def resolve_get_question(root, info, ques_id): 
		return Question.objects.get(pk=ques_id)

	def resolve_get_all_answers(root, info, ques_id):
		return Answer.objects.filter(question__pk=ques_id)


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
