from django.db import models
from datetime import date

# Create your models here.



class Category(models.Model):
    name_ar = models.CharField(max_length = 30)
    sub_category_ar = models.CharField(max_length = 30, blank=True)

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
  
   def add_entry(data):
       if not data['draft']:
           data["pub_date"] = date.today() 
       else:
           data["pub_date"] = "" 

       mystory = Story(title_ar = data['title_ar'], 
                       synopsis_ar = data['synopsis_ar'],
                       draft = data['draft'],
                       category = Category.objects.get(pk=data['category']),
                       pub_date = data['pub_date'])    
       mystory.save()     
       Response.add_entry(data, mystory)


class Response(models.Model):
  
   text_ar = models.CharField(max_length = 1000, blank=True) 
   pub_date = models.DateField(blank=True)
   character = models.ForeignKey(Character, on_delete=models.CASCADE)
   story = models.ForeignKey(Story, on_delete=models.CASCADE)



   def add_entry(data, curr_story):
       for key in range(len(data['responses'])):
           myresponse = Response(text_ar   = data['responses'][key],
                           character = Character.objects.get(pk=data['characters'][key]),
                           pub_date = data['pub_date'],
                           story = curr_story)
           myresponse.save() 


 
    


