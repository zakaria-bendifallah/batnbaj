from django.db import models


# Create your models here.



class Category(models.Model):
    name_ar = models.CharField(max_length = 30)
    name_fr = models.CharField(max_length = 30)
    sub_categoryi_ar = models.CharField(max_length = 30, blank=True)
    sub_categoryi_fr = models.CharField(max_length = 30, blank=True)

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
   title_fr = models.CharField(max_length = 100 )
   synopsis_ar = models.CharField(max_length = 500, blank=True)
   synopsis_fr = models.CharField(max_length = 500, blank=True)
   pub_date = models.DateField()
   draft    = models.IntegerField(default = 1)
   category = models.ForeignKey(Category,on_delete=models.CASCADE, default = 1)   
   def __str__(self):
       return self.title_ar

class Response(models.Model):
  
   text_ar = models.CharField(max_length = 1000, blank=True) 
   text_fr = models.CharField(max_length = 1000, blank=True)   
   pub_date = models.DateField(blank=True)
   character = models.ForeignKey(Character, on_delete=models.CASCADE)
   story = models.ForeignKey(Story, on_delete=models.CASCADE)

