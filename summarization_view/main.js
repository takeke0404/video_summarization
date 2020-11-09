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
    setTimeout(nextSegment, (parseFloat(clip_segments[current_segment_index][1],10)-parseFloat(clip_segments[current_segment_index][0],10))*1000+100);
    console.log(parseFloat(clip_segments[current_segment_index][0],10));
}

function stopVideo() {
    player.stopVideo();
}
function nextSegment() {
    if(current_segment_index==clip_segments.length-1){
        stopVideo();
    }else {
        current_segment_index++;
        console.log(parseFloat(clip_segments[current_segment_index][0],10));
        player.seekTo(parseFloat(clip_segments[current_segment_index][0],10));
        setTimeout(nextSegment, (parseFloat(clip_segments[current_segment_index][1],10)-parseFloat(clip_segments[current_segment_index][0],10))*1000+100);
    }
}

// drop event
$(function(){
    var droppable = $("#droppable");

    if(!window.FileReader) {
        alert("File API がサポートされていません。");
    }
    var cancelEvent = function(event) {
        event.preventDefault();
        event.stopPropagation();
    }
    droppable.bind("dragenter", cancelEvent);
    droppable.bind("dragover", cancelEvent);

    var handleDroppedFile = function(event) {
        var file = event.originalEvent.dataTransfer.files[0];
        var fileReader = new FileReader();
        fileReader.onload = function(event) {

            console.log(event.target.result);
            var tmp = event.target.result.split("\n");
            var video_id = tmp[0].match(/v=.*/)[0].substring(2);
            for(var i=1;i<tmp.length-1;i++){
                clip_segments[i-1] = tmp[i].split(',');
            }
            player = new YT.Player('player', {
                height: '360',
                width: '640',
                videoId: video_id,
                events: {
                    'onReady': onPlayerReady,
                }
            });
            current_segment_index = 0;
            console.log(parseFloat(clip_segments[current_segment_index][0],10));

        }
        fileReader.readAsText(file);

        cancelEvent(event);
    }

    droppable.bind("drop", handleDroppedFile);
});
