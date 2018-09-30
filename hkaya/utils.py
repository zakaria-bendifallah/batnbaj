
from hkaya.models import Category, Story, Response, Character  
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hkaya.text_utils import * 

# == helper functions ==

def getRootLinks(request):
   ''' loads the root links of the website main template
   '''
   root_links = {
      'index': "/hkaya/index",
      'chkoun': "/hkaya/chkoun",
      'category' : "/hkaya/cat", 
      'story' : "/hkaya/hky",
   }

   if request.user.is_authenticated:
      root_links.update({
          'add_story' : "/hkaya/zidhky/add_story",
          'search_story' : "/hkaya/zidhky/search_story",
          'modify_story' : "/hkaya/zidhky/modify_story",
          'add_character' : "/hkaya/zidhky/add_character",
          'search_character' : "/hkaya/zidhky/search_character",
          'modify_character' : "/hkaya/zidhky/modify_character",
          'logout' : "/hkaya/zidhky/logout",
          'username': request.user.username,
          'site_admin': True
      }) 
   else:
      root_links.update({
          'site_admin': False
      })
   return root_links


def getCategories():

    queryset = Category.objects.all()
    return queryset 

def getCategory(category_id):
   queryset =  Category.objects.get(pk=category_id)
   return queryset


def getStories(q_story_title = None, q_category = None , q_draft = 0, q_pages = 5, q_page_num = 1):
   
   queryset = Story.objects.all()
   if q_category is not None: 
       queryset = Story.objects.all().filter(
                            category = q_category
                          )
   if q_story_title is not None:
       queryset = queryset.filter(title_ar = q_story_title)

   queryset = queryset.filter(draft = q_draft)
   paginator = Paginator(queryset, q_pages) 
   try:
       stories = paginator.page(q_page_num)
   except PageNotAnInteger:
       stories = paginator.page(1) 
   except EmptyPage:
       stories = Paginator(paginator.num_pages)   

   return stories


def getStory(story_id):
   queryset = Story.objects.get(pk = story_id)
   return queryset 

def setStoryViews(story_id, request):
    viewed = request.session.get('{}'.format(story_id),False)
    if not viewed:
        Story.increment_views(story_id) 
        request.session["{}".format(story_id)] = True
        request.session.modified = True


def getCharacters(c_character_name = None, c_pages = 10, c_page_num = 1):
   queryset = Character.objects.all();
   if c_character_name is not None:
      queryset.filter(name_ar = c_character_name)
   paginator = Paginator(queryset, c_pages)
   try: 
      characters = paginator.page(c_page_num)
   except PageNotAnInteger:
      characters = paginator.page(1)
   except EmptyPage:  
      characters = paginator.page(paginator.num_pages)

   return characters

def getCharacter(character_id):
   queryset = Character.objects.get(pk = character_id)
   return queryset

def getConversation(story_id):
   queryset = Response.objects.all().filter(story = story_id).order_by('id')
   conversation = list(queryset)
   return conversation


#################################################################
## conversation text decoration 
#################################################################
def enrich_conversation_text(conversation_list):
    ''' enriches the conversation texts with the following:
            - links identification and wrapping in <a> tags
    '''
    for response in conversation_list:
        response.text_ar = add_new_line(response.text_ar)
        response.text_ar = add_url_tags(response.text_ar) 
        
        print(response.text_ar) 
