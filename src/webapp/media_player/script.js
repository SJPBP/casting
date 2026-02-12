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

// Click to seek
progressBar = document.getElementById("progress-bar");
progressFilled = document.getElementById("progress-filled");

progressBar.addEventListener("click", async (e) => {
  const rect = progressBar.getBoundingClientRect();
  const clickX = e.clientX - rect.left;
  const percent = clickX / rect.width;
  // const newTime = percent * duration;

  console.log(percent);
  progressFilled.style.width = (percent * 100) + "%";
  // await set_current_time(newTime);
});
