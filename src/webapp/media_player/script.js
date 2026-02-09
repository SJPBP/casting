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
