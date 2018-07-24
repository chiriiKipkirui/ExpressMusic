$(document).ready(function(){
    $('#search_text').keyup(function(){
        var search_text= $(this).val();
        if($('#album-slug')){
        var album_slug = $('#album-slug').val();
    }
    else{
        var album_slug = '';
    }

        $.ajax({
            type:'POST',
            url:'search',
            data:{
                'search_text':search_text,
                'album':album_slug,
                'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(res) {
          var searchResults = $('#playlist_video');
          searchResults.html(res);

      },
      dataType:'html'

        })

      // $.get('search', {search_text: search_text}, function(data){
      //   $('#playlist_video').html(data);
      //  });
});




})
