// youtube player
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
var clip_segments = [];
var current_segment_index = 0;

function onPlayerReady(event) {
    player.seekTo(parseFloat(clip_segments[current_segment_index][0],10));
}

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {
        setTimeout(nextSegment, (parseFloat(clip_segments[current_segment_index][1],10)-parseFloat(clip_segments[current_segment_index][0],10))*1000+100);
        console.log(parseFloat(clip_segments[current_segment_index][0],10));
    }
}

function stopVideo() {
    player.stopVideo();
}
function nextSegment() {
    if(current_segment_index==clip_segments.length-1){
        stopVideo();
    }else {
        current_segment_index++;
        player.seekTo(parseFloat(clip_segments[current_segment_index][0],10));
    }
}

$('input#urlPost').on('click', function(){
    var formData = $('#urlPost').serialize();
    console.log("送信:"+formData);
    $.ajax({
        url: '/post_url',
        type: 'post',
        data: formData
    }).done(function(data) {
        var response = JSON.parse(data)[0];
        var video_id = ""
        if(response == "making"){
            document.getElementById('res').innerHTML='要約動画を作成中です。少々お待ちください';
            setTimeout(retry_post,30000,formData);
            return false;
        }else if (response == "crowd") {
            document.getElementById('res').innerHTML='ただいま込み合っています。少々お待ちください';
            setTimeout(retry_post,60000,formData);
            return false;
        }else if (response == "error"){
            document.getElementById('res').innerHTML='要約の作成に失敗しています';
            return false;
        }else{
            video_id=response;
            document.getElementById('res').innerHTML='';
        }
        clip_segments = JSON.parse(data).slice(1);
        player = new YT.Player('player', {
            height: '360',
            width: '640',
            videoId: video_id,
            events: {
                'onReady': onPlayerReady,
                'onStateChange': onPlayerStateChange
            }
        });
        current_segment_index = 0;
        console.log(parseFloat(clip_segments[current_segment_index][0],10));

    });
    return false;
});

function retry_post(formData){
    console.log("送信:"+formData);
    $.ajax({
        url: '/post_url',
        type: 'post',
        data: formData
    }).done(function(data) {
        var response = JSON.parse(data)[0];
        var video_id = ""
        if(response == "making"){
            document.getElementById('res').innerHTML='要約動画を作成中です。少々お待ちください';
            setTimeout(retry_post,30000,formData);
            return false;
        }else if (response == "crowd") {
            document.getElementById('res').innerHTML='ただいま込み合っています。少々お待ちください';
            setTimeout(retry_post,60000,formData);
            return false;
        }else if (response == "error"){
            document.getElementById('res').innerHTML='要約の作成に失敗しています';
            return false;
        }else{
            video_id=response;
        }
        clip_segments = JSON.parse(data).slice(1);
        player = new YT.Player('player', {
            height: '360',
            width: '640',
            videoId: video_id,
            events: {
                'onReady': onPlayerReady,
                'onStateChange': onPlayerStateChange
            }
        });
        current_segment_index = 0;
        console.log(parseFloat(clip_segments[current_segment_index][0],10));

    });
    return false;
}
