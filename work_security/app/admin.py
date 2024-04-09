from django.contrib import admin

from app.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Gallery)
admin.site.register(Instruction)
admin.site.register(TestToUser)


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [
        AnswerInline,
    ]


class QuestionInline(admin.TabularInline):
    model = Question
    show_change_link = True


class TestAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [
        QuestionInline,
    ]


admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
