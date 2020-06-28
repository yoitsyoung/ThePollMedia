
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe   
from django.apps import apps
from .models import *
import logging
# Register your models here.
UserModel = get_user_model()
admin.site.unregister(UserModel)



# in line for user class
class QuestionInline(admin.StackedInline):
    model = Question
    
class ProfileInline(admin.StackedInline):
    model = Profile

class OptionInQuestion(admin.StackedInline):
    model = Option

class OptionInline(admin.TabularInline):
    model = User.answers.through


#not sure what this does
class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.get_fields(include_hidden=True)]
        super(ListAdminMixin, self).__init__(model, admin_site)
##
@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    
    inlines = [QuestionInline, OptionInline, ProfileInline]
    
    
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'answers', 'questions'
    )

    def questions(self, obj):
        #object here is user model passed in
        qs = obj.questions.filter(owner = obj.id)
        content = ''
        for i in range(0,len(qs)):
            url = '/admin/polling/question/{}/change/'.format(qs[i].id)
            html =  '<a href=' + url + '> View question ' + str(qs[i].id) + '</a><br>'
            content += html
        return mark_safe(content)

    
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        OptionInQuestion,
    ]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)