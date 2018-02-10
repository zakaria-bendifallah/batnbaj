from django.conf.urls import include,url

from . import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^chkoun/', views.viewChkoun, name='index'),
    url(r'^hky/(\d+)/',  views.viewStory , name='hky'),
    url(r'^cat/(\d+)/',  views.viewCategory , name='cat'),

    url(r'^zidhky/add_story/',  views.viewAddStory , name='addstory'),
    url(r'^zidhky/search_story/',  views.viewSearchStory , name='searchstory'),
    url(r'^zidhky/ajax/validate_story/',  views.ajaxValidateStory , name='validatestory'),
    url(r'^zidhky/ajax/delete_story/',  views.ajaxDeleteStory , name='deletestory'),
    url(r'^zidhky/modify_story/(\d+)/',  views.viewModifyStory , name='modifystory'),

    url(r'^zidhky/add_character/',  views.viewAddCharacter , name='addcharacter'),
    url(r'^zidhky/search_character/',  views.viewSearchCharacter , name='searchcharacter'),
    url(r'^zidhky/ajax/delete_character/',  views.ajaxDeleteCharacter , name='deletecharacter'),
    url(r'^zidhky/modify_character/(\d+)/',  views.viewModifyCharacter , name='modifycharacter'),

]
