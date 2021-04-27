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
