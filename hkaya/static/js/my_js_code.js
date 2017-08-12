//{% load static %}

$(document).ready(function() {

   //add a new response window
   $("#new-response").click(function(e){
     e.preventDefault();
     var new_elem = {
         id          : form_data.number_responses,
         div_id      : "zidhky_div_" + form_data.number_responses,
         textarea_id: "zidhky_textarea_" + form_data.number_responses,
         character_id: "zidhky_character_" + form_data.number_responses
     };
     form_data.responses_array.push(new_elem);
     form_data.number_responses += 1;


     var main_div = $('<div></div>');
     main_div.addClass("zidhky resp-container");
     main_div.attr("id",new_elem.div_id);

     var header_div = $("<div></div>")
     header_div.addClass("zidhky resp-header");

     var close_tag = $('<p></p>');
     close_tag.addClass("fa fa-window-close");

     var minus_tag = $('<p></p>');
     minus_tag.addClass("fa fa-minus-square");

     var down_tag = $('<p></p>');
     down_tag.addClass("fa fa-arrow-circle-down");

     var up_tag = $('<p></p>');
     up_tag.addClass("fa fa-arrow-circle-up");

     var newline_tag = $('<br>');

   

     var character_tag = $('<select></select>')
     character_tag.attr("name","character-select");
     character_tag.attr("id",new_elem.character_id);
     for (character in character_list){
        var option_tag = $('<option></option>');
        option_tag.attr("value",character_list[character].id);
        option_tag.text(character_list[character].name);
        character_tag.append(option_tag); 
     } 
      
     var textarea_tag = $('<textarea></textarea>');
     textarea_tag.attr("rows","5");
     textarea_tag.attr("cols","50");
     textarea_tag.attr("id", new_elem.textarea_id);
      
     header_div.append(close_tag).append(
                     minus_tag).append(
                     down_tag).append(
                     up_tag);
     main_div.append(header_div).append(
                     character_tag).append(
                     textarea_tag);

     $("#new-response").before(main_div);
     main_div.hide().fadeIn("slow");
   });


   //reduce a conversation window
   $("#zidhky-form").on("click",".fa.fa-minus-square", (function(){
      $(this).parent().parent().find("textarea").slideUp();
      $(this).toggleClass("fa-minus-square fa-plus-square"); 
      console.log("minus pressed");
   }));
   
   //expand a conversation window
   $("#zidhky-form").on("click",".fa.fa-plus-square", (function(){
      $(this).parent().parent().find("textarea").slideDown();
      $(this).toggleClass("fa-plus-square fa-minus-square"); 
   }));

   //close a conversation window
   $("#zidhky-form").on("click",".fa.fa-window-close", (function(){
      var main_div = $(this).parent().parent();
      main_div.fadeOut("fast");

      var main_div_id = main_div.attr("id"); 
      var index = form_data.get_index_by_div(main_div_id);
      if(index == -1)
      {
          console.log("form element "+ main_div_id +" not found");
      }else{
          form_data.responses_array.splice(index,1); 
          main_div.delay(100).remove();
      }
       
   }));

   //switch between self and next response
   $("#zidhky-form").on("click",".fa-arrow-circle-down", (function(){
      self_parent = $(this).parent().parent();
      next_parent = self_parent.next();
      if(next_parent.hasClass("zidhky resp-container")){
          self_parent.slideUp("fast");
          self_parent.delay(100).detach(); 
          next_parent.after(self_parent);
          self_parent.delay(100).slideDown();

          var self_div_id = self_parent.attr("id"); 
          var next_div_id = next_parent.attr("id"); 
          var self_index = form_data.get_index_by_div(self_div_id);
          var next_index = form_data.get_index_by_div(next_div_id);  
          var self_response = form_data.responses_array[self_index];
          form_data.responses_array[self_index] = form_data.responses_array[next_index] 
          form_data.responses_array[next_index] = self_response;
      }
   }));
    
   
   //switch between self and previous response
   $("#zidhky-form").on("click",".fa-arrow-circle-up", (function(){
      self_parent = $(this).parent().parent();
      prev_parent = self_parent.prev();
      if(prev_parent.hasClass("zidhky resp-container")){
        self_parent.slideUp("fast");
        self_parent.delay(100).detach(); 
        prev_parent.before(self_parent);
        self_parent.delay(100).slideDown();

        var self_div_id = self_parent.attr("id"); 
        var prev_div_id = prev_parent.attr("id"); 
        var self_index = form_data.get_index_by_div(self_div_id);
        var prev_index = form_data.get_index_by_div(prev_div_id);  
        var self_response = form_data.responses_array[self_index];
        form_data.responses_array[self_index] = form_data.responses_array[prev_index] 
        form_data.responses_array[prev_index] = self_response;
      }
   }));


   $("#data-submit").click(function(e){
         e.preventDefault();
         console.log($(".zidhky.story_name").val());
         console.log($(".zidhky.category_name").val());
         console.log($(".zidhky.draft").is(":checked"));
         
         var darray_length = form_data.responses_array.length;

         for(i=0; i < darray_length; i++)
         {
             console.log($('#'+form_data.responses_array[i].textarea_id).val());
             console.log($('#'+form_data.responses_array[i].character_id).val());
         }

         var post_data = {
              title_ar : $(".zidhky.story_name").val(),
              category : $(".zidhky.category_name").val(),
              draft : $(".zidhky.draft").is(":checked"),
              synopsis_ar : $(".zidhky.synopsis").val(),
              responses : [],
              characters : []  
         }
         for(i=0; i < darray_length; i++)
         {
            post_data.responses.push(
                          $('#'+form_data.responses_array[i].textarea_id).val());
            post_data.characters.push(
                          $('#'+form_data.responses_array[i].character_id).val());
         }
         
         var json_post_data = JSON.stringify(post_data);
         console.log(json_post_data); 

         $.ajax({url: "/hkaya/zidhky/ajax/validate_story/",
                headers: {'X-CSRFToken': csrf_token},
                data: json_post_data,  
                dataType: "json",
                contentType: "application/json;charset=utf-8",
                type: 'POST', 
                success: function(data){     
                    if(data.status == "success"){
                       add_story_success(data);
                    }else{
                       add_story_failure(data);
                    }
                },
                error: function(xhr){
                    alert("An error occured: " + xhr.status + " " + xhr.statusText); 
                },
         });


   });


});


var form_data = {
    number_responses : 0,
    responses_array : [], 
    /* object elements have the following structure
        {
          id : ,
          div_id : "",
          textarea_id : "",
          character_id : ""
        }
    */
    get_index_by_div : function(id){

        var length = form_data.responses_array.length;
        var index = -1;
        for(i=0; i< length; i++)
        {
            if(id == form_data.responses_array[i].div_id){
                index = i;
            }     

        }
        return index;
    }
};



function add_story_success(data)
{

    $("#zidhky-form").hide();
    var success_msg_tag = $("<p> "+ data.message +" &nbsp</p>");
    success_msg_tag.addClass("success_msg");
    var check_font_tag = $('<i class="fa fa-check " aria-hidden="true"></i>');
    success_msg_tag.append(check_font_tag);
    var new_story_link = $("<a href='" + add_story_link + "'>زيد حكاية أخرى</a>");     
    new_story_link.attr("id","link-button");
    $("#zidhky-form").before(success_msg_tag).before(new_story_link);
}

function add_story_failure(data)
{



}



