function toggleFollow(){
      $.ajax({
        url: window.USER_FOLLOW_URL,
        success: function(data) {
          $("#followCount").html('Подписчиков: ' + data.follower_count);
          $('#followElement').html(data.button);
        }
      });
};


function toggleLike(post_id){
      $.ajax({
        url: "/post/" + post_id + "/like_api",
        success: function(data) {
          $("#likeCount" + post_id).html('Лайки: ' + data.like_count);
          $("#imageElement" + post_id).html(data.img);
        }
      });
};
