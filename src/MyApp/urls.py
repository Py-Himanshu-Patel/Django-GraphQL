from typing import Tuple
from django.urls import path
from graphene_django.views import GraphQLView
import graphql
from MyApp.schema import schema

urlpatterns = [
	# instead of defining schema here we can define a default schema in settings.py
	path("books/", GraphQLView.as_view(graphiql=True, schema=schema))
]
