from django.db import models
import graphene
from graphene_django import DjangoObjectType
from .models import Book


class BookType(DjangoObjectType):
	class Meta:
		model = Book
		fields = ('id', 'title', 'summary')

class Query(graphene.ObjectType):
	all_books = graphene.List(BookType)

	# create a method starting with resolve_
	def resolve_all_books(root, info):
		return Book.objects.all()

schema = graphene.Schema(query=Query)
