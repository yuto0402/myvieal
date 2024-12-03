import Cookies from "/js-cookie";

document.querySelector(".follow-btn").onclick = function (event) {
  event.preventDefault();
  console.log("動いたよ");
  fetch(window.location.pathname, {
    method: "POST",
    body: "",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      "X-CSRFToken": Cookies.get("csrftoken"),
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
        followBtn.classList.add("follow-btn--unfollow");
        followBtn.textContent = "フォロー中";
      } else {
        followBtn.classList.remove("follow-btn--unfollow");
        followBtn.textContent = "フォロー";
      }
    })
    .catch((error) => {
      console.log(error);
    });
};
