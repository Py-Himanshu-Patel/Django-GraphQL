from django.urls import path
from graphene_django.views import GraphQLView
from Quiz.schema import schema

urlpatterns = [
	path("quiz/", GraphQLView.as_view(graphiql=True, schema=schema))
]
