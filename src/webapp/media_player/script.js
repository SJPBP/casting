console.log("script.js loaded");

button = document.getElementById("pause-play-btn");
icon = document.getElementById("pause-play-btn-content");

button.addEventListener("click", () => {
  console.log("Button clicked");
  if (icon.classList.contains("fa-play")) {
    icon.classList.remove("fa-play");
    icon.classList.add("fa-pause");
  } else {
    icon.classList.remove("fa-pause");
    icon.classList.add("fa-play");
  }
});

// Update the playback line as the video plays
// video.addEventListener("timeupdate", () => {
//   const currentTime = video.currentTime;
//   const duration = video.duration;
//   const percentage = (currentTime / duration) * 100;
//   progressBar.style.width = percentage + "%";
// });
//
// // Reseting the playback line when the video ends
// video.addEventListener("ended", () => {
//   progressBar.style.width = "0%";
//   showThumbnail();
// });

const playbackline = document.querySelector(".playback-line");
playbackline.addEventListener("click", () => {
  const timelineWidth = playbackline.clientWidth;
  console.log(timelineWidth);
  // video.currentTime = (e.offsetX / timelineWidth) * video.duration;
});
