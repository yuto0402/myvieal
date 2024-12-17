const detail = document.querySelector(".detail");
const description = document.querySelector(".description");

document.querySelector(".detail").addEventListener("click", function () {
  description.classList.toggle("expanded");
  if (description.classList.contains("expanded")) {
    detail.textContent = "...閉じる";
  } else {
    detail.textContent = "...もっと見る";
  }
});

//もし動画の説明文があまり長くない(3行以下)なら「もっと見る」を表示しない
if (description.scrollHeight <= description.offsetHeight) {
  detail.style.display = "none";
}

// profile_other_jsからコピペ（動作確認して後でまとめる）

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

document.querySelector(".follow-btn").addEventListener("click", function (event) {
  event.preventDefault();
  console.log("ここは実行されている");
  fetch(url, {
    method: "POST",
    body: "target_user_pk=" + target_user_pk,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    // ステータスがokかチェックする処理
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      } else {
        return response.json();
      }
    })
    .then((response) => {
      // ボタンの状態を変更する
      const followBtn = document.querySelector(".follow-btn");
      if (response.method == "follow") {
        followBtn.classList.add("follow-btn--following");
        followBtn.textContent = "フォロー中";
      } else if (response.method == "unfollow") {
        followBtn.classList.remove("follow-btn--following");
        followBtn.textContent = "フォロー";
      }
    })
    .catch((error) => {
      console.log(error);
    });
});
