from django.contrib import admin
from .models import Blog, Quiz, Question, Option, QuizSubmission

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'created_date', 'is_active']
    list_filter = ['is_active', 'created_date']
    search_fields = ['title', 'description']

admin.site.register(Blog)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizSubmission)

