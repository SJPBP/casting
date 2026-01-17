document.addEventListener("DOMContentLoaded", function () {
  function callApi(api) {
    fetch(api)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return True;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  function play() {
    const playApi = "http://127.0.0.1:8080/play";
    callApi(playApi);
  }

  function pause() {
    const playApi = "http://127.0.0.1:8080/pause";
    callApi(playApi);
  }

  document.getElementById("play").addEventListener("click", play);
  document.getElementById("pause").addEventListener("click", pause);
});
