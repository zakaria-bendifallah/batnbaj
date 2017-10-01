from django.db import models
from datetime import date

# Create your models here.



class Category(models.Model):
    name_ar = models.CharField(max_length = 30)
   # sub_category_ar = models.CharField(max_length = 30, blank=True)

    def __str__(self):
        return self.name_ar



class Character(models.Model):

    name_ar = models.CharField(max_length = 30)
    name_fr = models.CharField(max_length = 30)
    short_bio_ar  = models.CharField(max_length = 500)
    short_bio_fr  = models.CharField(max_length = 500)
    
    def __str__(self):
        return self.name_ar



class Story(models.Model):

   title_ar = models.CharField(max_length = 100 )
   synopsis_ar = models.CharField(max_length = 500, blank=True)
   pub_date = models.DateField()
   draft    = models.IntegerField(default = 1)
   category = models.ForeignKey(Category,on_delete=models.CASCADE, default = 1)   
   def __str__(self):
       return self.title_ar
   # add a new story
   def add_entry(data):
        
       data["pub_date"] = date.today() 
       conform = True
       query_response = { 'status' : "success", 
                          'message': "حكايتك تسجلت فالمذكرة يا السي"}

       if(data['title_ar'] == ''):
           conform = False
           query_response["message"] = "لازم إسم للحكاية"
           query_response["status"] = "failure"
       if conform: 
           mystory = Story(title_ar = data['title_ar'], 
                           synopsis_ar = data['synopsis_ar'],
                           draft = data['draft'],
                           category = Category.objects.get(pk=data['category']),
                           pub_date = data['pub_date'])    
           mystory.save()     
           Response.add_entry(data, mystory)
       return query_response

   # update an existing story
   def update_entry(data):
       query_response = {}
       mystory = Story.objects.filter(pk = data['story_id']).first()

       if mystory is None:
          query_response["status"] = "failure"
          query_response["message"] = "ما لقيناش لحكاية !"  
          return query_response
      
       if(data['title_ar'] == ''):
           conform = False
           query_response["message"] = "لازم إسم للحكاية"
           query_response["status"] = "failure"
           return query_response    

       mystory.title_ar = data['title_ar'] 
       mystory.synopsis_ar = data['synopsis_ar']
       mystory.draft = data['draft']
       mystory.category = Category.objects.get(pk=data['category'])
       mystory.pub_date = date.today() 
       mystory.save()

       Response.delete_entry(mystory)
       Response.add_entry(data, mystory)

       query_response['status'] = "success"
       query_response['message'] = "لحكاية تعدلت بنجاح"  
       return query_response     

   # delete an existing story
   def delete_entry(story_id):
       story = Story.objects.filter(pk = story_id).first()      
       if story is None:
           return False
       story.delete()
       story = None
       story = Story.objects.filter(pk = story_id).first() 
       if story is None:
           return True
       else:
           return False 


class Response(models.Model):
  
   text_ar = models.CharField(max_length = 1000, blank=True) 
   pub_date = models.DateField(blank=True)
   character = models.ForeignKey(Character, on_delete=models.CASCADE)
   story = models.ForeignKey(Story, on_delete=models.CASCADE)


   # add a new conversation
   def add_entry(data, curr_story):
       for key in range(len(data['responses'])):
           myresponse = Response(text_ar   = data['responses'][key],
                           character = Character.objects.get(pk=data['characters'][key]),
                           pub_date = date.today(),
                           story = curr_story)
           myresponse.save() 

   # delete an existing conversation
   def delete_entry(curr_story):
       queryset = Response.objects.filter(story = curr_story)
       if queryset is not None:
           queryset.delete()          
    


