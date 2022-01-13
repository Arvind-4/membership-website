var tag = document.createElement("script");
var youtubeVideoDiv = document.getElementById("player");
var host_id = youtubeVideoDiv.getAttribute("data-video-id");

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName("script")[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
var player;
function onYouTubeIframeAPIReady() {
player = new YT.Player("player", {
    height: "390",
    width: "640",
    videoId: host_id,
    playerVars: {
    playsinline: 1,
    },
    events: {
    onReady: onPlayerReady,
    onStateChange: onPlayerStateChange,
    },
});
}

function onPlayerReady(event) {
event.target.playVideo();
}
var done = false;
function onPlayerStateChange(event) {
if (event.data == YT.PlayerState.PLAYING && !done) {
    setTimeout(stopVideo, 6000);
    done = true;
}
}
function stopVideo() {
player.stopVideo();
}