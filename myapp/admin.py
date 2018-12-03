from django.contrib import admin
from .models import Question,Choice
class ChoiceinLine(admin.TabularInline):
    model = Choice
    extra = 0
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,{'fields': ['question_text','score']}),
            ('Categoria', {'fields': ['cat']})
                ]
    inlines = [ChoiceinLine]

admin.site.register(Question, QuestionAdmin)