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
    story_list = getStories(q_category = category_id)
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

def viewSearchStory(request):

    root_links = getRootLinks() 
    categories = getCategories()
    characters = getCharacters()

    search_request = False
    story_list = {}  
    if request.method == 'POST':
         search_request = True
         story_name = request.POST.get("story_name")
         category    = request.POST.get("category-select")
         draft       = request.POST.get("draft") 
         if story_name == "":
             story_name = None
         if category == "-1":
             category = None
         if draft is not None: 
             draft = 1
         else:
             draft = 0
         story_list = getStories(q_story_title = story_name,
                                  q_category    = category,
                                  q_draft       = draft)  
    found_stories = len(story_list)
    return render(request, "search_story.html", locals())
           

def viewModifyStory(request, story_id):
        
    root_links = getRootLinks() 
    categories = getCategories()
    characters = getCharacters()
    story_item = getStory(story_id)
    #category_item = getCategory(story_item.category) 
    conversation_list = getConversation(story_id) 
    
    return render(request, "modify_story.html", locals())

# -- AJAX views ----------------------------

def ajaxValidateStory(request):
    if request.is_ajax() and request.method == 'POST':

        decoded_request_body = request.body.decode('UTF-8')
        json_form = json.loads(decoded_request_body) 

        if json_form['draft']:
            json_form['draft'] = 1
        else:
            json_form['draft'] = 0
        if 'story_id' in json_form: # update a story
            json_data = Story.update_entry(json_form)
        else: # add new story 
            json_data = Story.add_entry(json_form)

    return JsonResponse(json_data)

def ajaxDeleteStory(request):

    json_data = { 'status' : "failure"}
    if request.is_ajax() and request.method == 'POST':
        decoded_request = request.body.decode('UTF-8')
        json_form = json.loads(decoded_request)
        story_deleted = Story.delete_entry(json_form['story_id'][2:])
        json_data["story_id"] = json_form['story_id']  
        if story_deleted:
            json_data['status'] = "success"
         
    return JsonResponse(json_data)



