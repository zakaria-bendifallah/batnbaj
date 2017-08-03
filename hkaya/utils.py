
from hkaya.models import Category, Story, Response, Character  


# == helper functions ==

def getRootLinks():
   root_links = {
      'index': "http://localhost:8000/hkaya/index",
      'chkoun': "http://localhost:8000/hkaya/chkoun",
      'category' : "http://localhost:8000/hkaya/cat", 
      'story' : "http://localhost:8000/hkaya/hky"} 
   return root_links


def getCategories():

    queryset = Category.objects.all()
    return queryset 


def getCategory(category_id):
   queryset =  Category.objects.get(pk=category_id)
   return queryset


def getStories(category_id = None , draft = False ):
   if category_id is None:
       queryset = Story.objects.all()
   else:
       queryset = Story.objects.all().filter(
                            category = category_id
                          )
   queryset = queryset.filter(draft = 0)[:10]
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
