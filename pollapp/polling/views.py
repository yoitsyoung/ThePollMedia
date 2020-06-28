from django.shortcuts import render, redirect 
from django.http import HttpResponse, HttpRequest, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from . import views
from .models import *
from .forms import *
import logging
import random
logger = logging.getLogger(__name__)
# Create your views here.
# using kwargs is a powerful way to customise your url links... but note they only change the url links
def home_view(request, *args, **kwargs):

    try:
        if not message:
            pass
    except:
        message = 'Hi'
        pass
    context = {
        "user":request.user,
        "message":message,
    }
    return render(request, 'polling/base.html', context)


def random_question_view(request, *args, **kwargs):
    
    user_id = request.user.id
    max_number = Question.objects.count()
    question_id = random.randint(3, max_number + 1)
    logger.info('accessing random qn view... qn id is ' + str(question_id))
    '''
    while True:
        question_id = random.randint(1, max_number)
        res_question = Question.objects.get(id=question_id)
        if not res_question.find_user_answer(user_id=user_id):
            break
        else:
            continue 
    
    '''
    
    res_question = Question.objects.get(id=question_id)
    data = {
        'title' : res_question.title,
        'content' : res_question.content,
        'options' : []
    }  

    #append json data for each option

    for option in res_question.options.all():
        logger.info(option)
        option_dict = {
            'id' : option.id,
            'content' : option.content,
            #'image' : option.image,
            'score' : option.score,
        }
        data['options'].append(option_dict)

    status = 200
    logger.info(data)
    return JsonResponse(data, status=status)

#for a particular fixed question
def question_view(request, question_id, *args, **kwargs):
    res_question = Question.objects.get(id=question_id)
    data = {
        'title' : res_question.title,
        'content' : res_question.content,
        'options' : []
    }  

    #append json data for each option

    for option in res_question.options.all():
        logger.info(option)
        option_dict = {
            'id' : option.id,
            'content' : option.content,
            #'image' : option.image,
            'score' : option.score,
        }
        data['options'].append(option_dict)

    status = 200
    logger.info(data)
    return JsonResponse(data, status=status)

def api_question_view(request, question_id, *args, **kwargs):
    '''
    REST API VIEW
    for COnsume by Js or React or Java/Swift
    Json data
    '''
    data ={

    }
    try:
        question = Question.objects.get(id=question_id)
    except:
        data['message'] = 'Not Found'
        status = 404
    return JsonResponse(data, status=status)

def signup_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpForm(data=request.POST)
            if form.is_valid():
                #not all of this is needed
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                email = form.cleaned_data["email"]
                location = form.cleaned_data["location"]
                bio = form.cleaned_data["bio"]
                #save a commit, an automatic method of form class. Returns user
                user = form.save()
                #Profile models added manually
                #You are loading the instance again so that you can access profile attributes
                user.refresh_from_db()
                user.information.location = location
                user.information.bio = bio
                #always remember to save db changes
                user.save()
                
                user = authenticate(username = user.username, password = password) #looks like you can't access password from obj manager
                login(request, user)
                message = 'You have successfully registered...'
                return HttpResponseRedirect(reverse("home"))
       
            else:
                #now your form has error in each field. re-render to show error message
                context = {'form':form}
                return render(request,'polling/input.html',context)
        else:
            form = SignUpForm()
            context = {'form':form}
            return render(request,'polling/input.html',context)
    else:
        message = 'You are already logged in....'
        return HttpResponseRedirect(reverse("home"))

def login_view(request, *args, **kwargs):

#error message does not show here... need to check

    context ={}
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    message = 'You have successfully logged in'
                    return HttpResponseRedirect(reverse("home"))
            #invalid form
            else:
                context["form"] =  form
                return render(request, 'polling/input.html', context)
        else:
            form = AuthenticationForm()
            context["form"] =  form
            return render(request, 'polling/input.html', context)
    else:
        return HttpResponseRedirect(reverse("home"))

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    message = 'You have successfully logged out'
    return HttpResponseRedirect(reverse("home" ))


def add_question_view(request, *args, **kwargs):
    form = QuestionForm(request.POST or None)
    logger.info(request.POST)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        question = form.save(commit=False)
        question.owner = request.user
        question.save()
        option_one = form.cleaned_data.get('option_one')
        option_two = form.cleaned_data.get('option_two')
        option_three = form.cleaned_data.get('option_three')
        option_four = form.cleaned_data.get('option_four')
        question.add_option(option_one)
        question.add_option(option_two)
        question.add_option(option_three)
        question.add_option(option_four)
        
        form = QuestionForm()
        User = request.user
        logger.info('when' , User.information.score)
        User.information.score += 5.0
        User.save()
        logger.info('added 5 score to user')

    context = {'form':form}
    return HttpResponseRedirect(reverse("home"))

def profile_view(request, *args, **kwargs):
    User = request.user
    asked_questions = User.questions.all()
    question_answers = User.answers.all()
    
    context ={
        'user':User,
        'asked_questions' : asked_questions,
        'question_answers': question_answers,
        'relationship': True
    }
    logger.info(context)
    logger.info('hi')
    return render(request, 'polling/view_profile.html', context)


def answer_question(request, *args, **kwargs):
    logger.info(request.POST)
    User = request.user
    user_option = Option.objects.get(id = request.POST.get('id'))
    if user_option.score is None:
        user_option.score = 1.0
    else:
        user_option.score += 1.0
    user_option.save()
    User.answers.add(user_option)
    logger.info('Added option to user')
    User.information.score += 1.0
    User.save()
    logger.info('added score to user')
    return JsonResponse({'success':True})

def other_profile_view(request, user_id, *args, **kwargs):
    this_user = User.objects.get(id=user_id)
    asked_questions = this_user.questions.all()
    question_answers = this_user.answers.all()
    current_user = request.user
    try:
        if current_user.following.get(user = this_user):
            relationship = True
    except:
        relationship = False
    context ={
        'user':this_user,
        'asked_questions' : asked_questions,
        'question_answers': question_answers,
        'relationship': relationship,
    }
    logger.info(context)
    logger.info('hi')
    return render(request, 'polling/view_profile.html', context)

def search_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('username')
            search_results = User.objects.filter(username__icontains=query)
            context = {
                'search_results':search_results,
            }
            return render(request,'polling/search.html', context)
        else:
            return HttpResponse("invalid form")
    else:
        form = UserSearchForm
        context = {
            'form':form
        }
        return render(request, 'polling/input.html', context)

def follow(request, *args, **kwargs):
    user_id = request.POST.get('user_id')
    following_user = User.objects.get(id=user_id).information
    current_user = request.user
    current_user.following.add(following_user)
    current_user.save()
    logger.info('follower successfully added')
    return HttpResponseRedirect(reverse('home'))
    
