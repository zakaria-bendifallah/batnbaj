from django.conf.urls import include,url

from . import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^chkoun/', views.viewChkoun, name='index'),
    url(r'^hky/(\d+)/',  views.viewStory , name='hky'),
    url(r'^cat/(\d+)/',  views.viewCategory , name='cat'),
    url(r'^zidhky/',  views.viewAddStory , name='addstory'),
    url(r'^zidhky/ajax/validate_story/',  views.ajaxValidateStory , name='validatestory'),
]
