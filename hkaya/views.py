from django.shortcuts import render
from hkaya.utils import * 
from django.http import HttpResponse,JsonResponse
from hkaya.models import Category, Story, Response, Character   
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt

# Create your views here.



# == HTML views ==----------------------

def index(request):
    root_links = getRootLinks() 
    categories = getCategories()
    story_list = getStories() 
    return render(request, "index.html", locals())


def viewCategory(request, category_id):

    root_links = getRootLinks() 
    categories = getCategories()
    story_list = getStories(category_id)
    category_item = getCategory(category_id)
    return render(request, "category.html", locals())


def viewStory(request, story_id):

    root_links = getRootLinks() 
    categories = getCategories()
    story_item = getStory(story_id) 
    conversation_list = getConversation(story_id) 
    return render(request, "story.html", locals())

def viewChkoun(request):
     
    root_links = getRootLinks() 
    categories = getCategories()
    return render(request, "chkoun.html", locals())
    pass


@csrf_exempt
def viewAddStory(request):

    root_links = getRootLinks() 
    categories = getCategories()
    characters = getCharacters()

    return render(request, "add_story.html", locals())

           
   

# -- AJAX views ----------------------------

@csrf_exempt
def ajaxValidateStory(request):
    
    json_data = { 'status' : "success"};  
    return JsonResponse(json_data);





