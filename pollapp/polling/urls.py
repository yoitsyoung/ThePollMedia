from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('login', login_view, name='login'),
    path('signup', signup_view, name='signup'),
    path('logout', logout_view, name='logout'),
    path('questions/random', random_question_view, name='random_question'),
    path('questions/<int:question_id>', question_view, name='questions'),
    path('api/questions/<int:question_id>', api_question_view, name='api_question'),
    path('view_profile', profile_view, name='profile'),
    path('add', add_question_view, name='add_question'),
    path('answer_question', answer_question, name='answer_question'),
    path('users/<int:user_id>', other_profile_view, name = 'users'),
    path('search', search_view, name='search'),
    path('follow', follow, name='follow')



]
