from django.contrib import admin

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category']


class AnswerInlineModel(admin.TabularInline):
    model = models.Answer
    fields = ['answer_text', 'is_right']


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ['title', 'quiz', 'is_active']
    list_display = ['title', 'quiz', 'difficulty', 'is_active']
    inlines = [AnswerInlineModel, ]


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_text', 'is_right', 'question']
