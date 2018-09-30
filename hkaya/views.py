from django.shortcuts import render
from hkaya.utils import * 
from django.http import HttpResponse,JsonResponse
from hkaya.models import Category, Story, Response, Character   
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from django.contrib.auth import logout
from django.shortcuts import redirect
import json
# Create your views here.



# == HTML views ==----------------------

def index(request):
    root_links = getRootLinks(request) 
    categories = getCategories()
    characters = getCharacters()
    story_list = getStories() 
    return render(request, "index.html", locals())


def viewCategory(request, category_id):

    if request.method == "GET":
        page_num = request.GET.get('page','1')
    root_links = getRootLinks(request) 
    categories = getCategories()
    characters = getCharacters()
    stories = getStories(q_category = category_id, 
                            q_page_num = page_num)
    category_item = getCategory(category_id)
    return render(request, "category.html", locals())


def viewStory(request, story_id):

    #update the number of views of the story
    setStoryViews(story_id, request)       
    root_links = getRootLinks(request) 
    categories = getCategories()
    characters = getCharacters()
    story_item = getStory(story_id) 
    conversation_list = getConversation(story_id) 
    enrich_conversation_text(conversation_list)
    return render(request, "story.html", locals())

def viewChkoun(request):
     
    root_links = getRootLinks(request) 
    categories = getCategories()
    characters = getCharacters()
    return render(request, "chkoun.html", locals())


def viewAddStory(request):

    root_links = getRootLinks(request) 
    categories = getCategories()
    characters = getCharacters()

    return render(request, "add_story.html", locals())

def viewSearchStory(request):

    root_links = getRootLinks(request) 
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
        
    root_links = getRootLinks(request) 
    categories = getCategories()
    characters = getCharacters()
    story_item = getStory(story_id)
    conversation_list = getConversation(story_id) 
    
    return render(request, "modify_story.html", locals())


def viewAddCharacter(request):

    root_links = getRootLinks(request) 
    categories = getCategories()
    characters = getCharacters()
    rs = None
    if request.method == 'POST':
      
        character_name   = request.POST.get("character_name")
        character_bio    = request.POST.get("character_bio")
        character_photo  = request.FILES.get("photo") 
        rs = Character.add_entry(c_name = character_name,
                                 c_bio  = character_bio,
                                 c_photo = character_photo)
        
    return render(request, "add_character.html", locals())

def viewSearchCharacter(request):

    root_links = getRootLinks(request) 
    categories = getCategories()
    characters = getCharacters()
 
    if request.method == "POST":
        search_request = True       
        character_name   = request.POST.get("character_name")
        if character_name == "":
            character_name = None
        character_list = getCharacters(c_character_name = character_name)
        found_characters = len(character_list)
    
    return render(request, "search_character.html", locals())


def viewModifyCharacter(request, character_id):
        
    root_links = getRootLinks(request) 
    categories = getCategories()
    characters = getCharacters()
    character_item = getCharacter(character_id)
     
    if request.method == "POST":
       rs = Character.update_entry(request.POST.get("character_id"),
                                   request.POST.get("character_name"),
                                   request.POST.get("character_bio"),
                                   request.FILES.get("photo")
                                  )
                      
       
    return render(request, "modify_character.html", locals())


def viewLogout(request):
    logout(request)
    return redirect("index") 

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


def ajaxDeleteCharacter(request):

    json_data = { 'status' : "failure"}
    if request.is_ajax() and request.method == 'POST':
        decoded_request = request.body.decode('UTF-8')
        json_form = json.loads(decoded_request)
        character_deleted = Character.delete_entry(json_form['character_id'][2:])
        json_data["character_id"] = json_form['character_id']  
        if character_deleted:
            json_data['status'] = "success"
         
    return JsonResponse(json_data)

