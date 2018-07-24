$(function() {
    $("#playlist_video li").eq(0).attr("class","active");
    $("#playlist_video li").on("click", function() {
        $("#videoarea").attr({
            "src": $(this).attr("movieurl"),
            "poster": "",
            "name":$(this).attr("movieurl").slice(7,-4),
            //"autoplay": "autoplay",
        });
        $("#video-description").text($("#videoarea").attr("name"));

    });
    $("#videoarea").attr({
        "src": $("#playlist_video li").eq(0).attr("movieurl"),
        "poster": $("#playlist_video li").eq(0).attr("moviesposter"),
        "name":$("#playlist_video li").eq(0).attr("movieurl").slice(7,-4),

    });
    $("#video-description").text($("#videoarea").attr("name"));

   /* Playlist code move to the next automatically*/
   $("#videoarea").on("ended",function(e){
       $("#playlist_video li.active").next().attr("class","active next");
       $("#playlist_video li.active").removeClass("active");
       $("#playlist_video li").removeClass("active");
       $("#playlist_video li.next ").attr("class","active");
       $("#playlist_video li.active").attr("movieurl");
      $("#videoarea").attr({
       "src": $("#playlist_video li.active").attr("movieurl"),
       "poster": $("#playlist_video li").attr("moviesposter"),
       "name":$("#playlist_video li.active").attr("movieurl").slice(7,-4),

   });
   // console.log($("#videoarea").attr("src"));


   //checking the length of the playlist if it has reached to the end
   if($("#playlist_video li").next().length==0){
       $("#videoarea").attr({
       "src": $("#playlist_video li").eq(0).attr("movieurl"),
       "poster": $("#playlist_video li").eq(0).attr("moviesposter"),
       "name":$("#playlist_video li").eq(0).attr("movieurl").slice(7,-4),
   });
       $("#playlist_video li").eq(0).attr("class","active new");//.attr("class","active new")
       $("#playlist_video li").eq(0).removeClass("new");
       $("#playlist_video li").eq(0).attr("class");


       }



   });

    //end of playback of music\

$('#videoarea').click(function(e){
    if($("#videoarea").attr("class")=="playing"){

        e.target.pause();
        if(e.target.ended){
            console.log("ended");
        }
        $("#videoarea").attr("class","paused");

    }
    else if($("#videoarea").attr("class")=="paused") {
        e.target.play();
        $("#videoarea").attr("class","playing");
    }
});
$("#playlist_video li").click(function(){
    $("#playlist_video li").removeClass("active");
    $(this).attr("class","active");

});
$("playlist_video li").attr("movieurl");
})
/* using click event to pause and play the video*/
