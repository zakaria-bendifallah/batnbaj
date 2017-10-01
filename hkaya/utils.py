
from hkaya.models import Category, Story, Response, Character  


# == helper functions ==

def getRootLinks():
   root_links = {
      'index': "http://localhost:8000/hkaya/index",
      'chkoun': "http://localhost:8000/hkaya/chkoun",
      'category' : "http://localhost:8000/hkaya/cat", 
      'story' : "http://localhost:8000/hkaya/hky",
      'add_story' : "http://localhost:8000/hkaya/zidhky/add_story",
      'search_story' : "http://localhost:8000/hkaya/zidhky/search_story",
      'modify_story' : "http://localhost:8000/hkaya/zidhky/modify_story",
   } 
   return root_links


def getCategories():

    queryset = Category.objects.all()
    return queryset 


def getCategory(category_id):
   queryset =  Category.objects.get(pk=category_id)
   return queryset


def getStories(q_story_title = None, q_category = None , q_draft = False ):
   
   queryset = Story.objects.all()
   if q_category is not None: 
       queryset = Story.objects.all().filter(
                            category = q_category
                          )
   if q_story_title is not None:
       queryset = queryset.filter(title_ar = q_story_title)

   if not q_draft: 
       q_draft = 0
   else:
       q_draft = 1

   queryset = queryset.filter(draft = q_draft)[:10]
   return list(queryset)


def getStory(story_id):
   queryset = Story.objects.get(pk = story_id)
   return queryset 


def getCharacters():
   queryset = Character.objects.all();
   return list(queryset)

def getConversation(story_id):
   queryset = Response.objects.all().filter(story = story_id).order_by('id')
   conversation = list(queryset)
   return conversation
