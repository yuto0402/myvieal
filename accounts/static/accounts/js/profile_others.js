// djangoのdocument(https://docs.djangoproject.com/ja/5.1/howto/csrf/)からコピペ
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.querySelector(".follow-btn").onclick = function (event) {
  event.preventDefault();
  console.log("動いたよ");
  fetch(window.location.pathname, {
    method: "POST",
    body: "",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => {
      return response.json();
    })
    .then((response) => {
      // フォロワー数を更新
      document.getElementById("follower_count").textContent =
        response.follower_count + "フォロワー";
      // アイコンの状態を変更する
      const followBtn = document.querySelector(".follow-btn");
      if (response.method == "follow") {
        followBtn.classList.add("follow-btn--following");
        followBtn.textContent = "フォロー中";
      } else {
        followBtn.classList.remove("follow-btn--following");
        followBtn.textContent = "フォロー";
      }
    })
    .catch((error) => {
      console.log(error);
    });
};
