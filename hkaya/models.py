from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
# Create your models here.



class Category(models.Model):
    name_ar = models.CharField(max_length = 30)
   # sub_category_ar = models.CharField(max_length = 30, blank=True)

    def __str__(self):
        return self.name_ar



def user_directory_path(instance, filename):
   # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
   return 'user_{0}/{1}'.format(instance.name_ar, filename)

class Character(models.Model):

    name_ar       = models.CharField(max_length = 30)
    short_bio_ar  = models.CharField(max_length = 500)
    photo         = models.ImageField(upload_to = user_directory_path, blank = True)    
 
    def __str__(self):
        return self.name_ar


    def add_entry(c_name = '', c_bio = '', c_photo = None ):
        rs = {"success":True, "message":""}    

        if c_name == '' or c_name == None:
            rs["success"] = False
            rs["message"] = rs['message'] + "<br> الشخصية لازملها اسم"
        else: 
            ins = Character.objects.all().filter(name_ar = c_name)  
            if len(list(ins)) > 0:
                rs['success'] = False
                rs['message'] = rs['message'] + "<br> هذا الاسم مستعمل"
                
        if c_bio == '' or c_bio == None:    
            rs['success'] = False
            rs['message'] = rs["message"] + "<br> الشخصية لازملها تعريف"
        if(rs['success']):
            mycharacter = Character(name_ar = c_name, 
                                    short_bio_ar = c_bio,
                                    )
            mycharacter.save()       
            mycharacter.photo = c_photo
            mycharacter.save()    
        return rs
    

    def delete_entry(character_id):
       character = Character.objects.filter(pk = character_id).first()      
       if character is None:
           return False
       character.delete()
       character = None
       character = Character.objects.filter(pk = character_id).first() 
       if character is None:
           return True
       else:
           return False 

    def update_entry(c_id = None, c_name = None , c_bio = None , c_photo = None):
       query_response = {"success": True,
                         "message": "معلومات الشخصية تعدلت"}
       mycharacter = Character.objects.filter(pk = c_id).first()

       if mycharacter is None:
          query_response["success"] = False
          query_response["message"] = "ما لقيناش لحكاية !"  
          return query_response

       if(c_name == ''):
           conform = False
           query_response["message"] = "لازم يسم للشخصية"
           query_response["success"] = False
           return query_response    

       if(c_bio == ''):
           conform = False
           query_response["message"] = "الشخصية لازملها تعريف"
           query_response["success"] = False
           return query_response     

       mycharacter.name_ar = c_name
       mycharacter.short_bio_ar = c_bio
       if(c_photo is not None):
          mycharacter.photo = c_photo
       mycharacter.save()      

       return query_response

class Story(models.Model):

   title_ar    = models.CharField(max_length = 100 )
   synopsis_ar = models.CharField(max_length = 500, blank=True)
   pub_date    = models.DateField()
   draft       = models.IntegerField(default = 1)
   category    = models.ForeignKey(Category,on_delete=models.CASCADE, default = 1)   
   num_views   = models.IntegerField(default = 0)
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
       my_story = Story.objects.filter(pk = story_id).first()      
       if my_story is None:
           return False
       my_story.delete()
       my_story = None
       my_story = Story.objects.filter(pk = story_id).first() 
       if my_story is None:
           return True
       else:
           return False 
   
   def increment_views(story_id):
       my_story = Story.objects.filter(pk = story_id).first()
       if my_story is None:
           return False
       my_story.num_views = my_story.num_views + 1
       my_story.save() 

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
    


