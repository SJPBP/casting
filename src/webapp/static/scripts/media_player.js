async function call_server(msg) {
  try {
    const response = await fetch(`http://localhost:5000/${msg}`);
    const data = await response.json(); // or .text()
    console.log(data);
  } catch (error) {
    console.error("Error:", error);
  }
}

button = document.getElementById("pause-play-btn");
icon = document.getElementById("pause-play-btn-content");

button.addEventListener("click", () => {
  console.log("Button clicked");
  const device_name = document.title;
  if (icon.classList.contains("fa-play")) {
    icon.classList.remove("fa-play");
    call_server(`play/${device_name}`);
    icon.classList.add("fa-pause");
  } else {
    icon.classList.remove("fa-pause");
    call_server(`pause/${device_name}`);
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
