from django.shortcuts import render
from hkaya.utils import * 
from django.http import HttpResponse,JsonResponse
from hkaya.models import Category, Story, Response, Character   
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
import json
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


def viewAddStory(request):

    root_links = getRootLinks() 
    categories = getCategories()
    characters = getCharacters()

    return render(request, "add_story.html", locals())

           
   

# -- AJAX views ----------------------------

def ajaxValidateStory(request):
    if request.is_ajax() and request.method == 'POST':

        decoded_request_body = request.body.decode('UTF-8')
        json_form = json.loads(decoded_request_body) 
        print(json_form['title_ar'],json_form['category'],json_form['draft']) 

        if json_form['draft'] == 'true':
            json_form['draft'] = True
        else:
            json_form['draft'] = False

        Story.add_entry(json_form)

    json_data = { 'status' : "success", 'message': "حكايتك تسجلت فالمذكرة يا السي"} 
    return JsonResponse(json_data)





