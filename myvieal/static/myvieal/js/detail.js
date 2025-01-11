defaultheight = document.getElementById("id_content").style.height

document.getElementById("form").addEventListener("submit", function (e) {
  const textarea = document.getElementById("id_content");
  const trimmedValue = textarea.value.trim();
  if (trimmedValue === "") {
    e.preventDefault();
    textarea.value = "";
    textarea.style.height = defaultheight;
    textarea.reportValidity();
  }
});

const reply_expanders = document.querySelectorAll(".reply_expander");

reply_expanders.forEach(function (reply_expander) {
  const text = reply_expander.textContent;
  reply_expander.addEventListener("click", function () {
    this.nextElementSibling.classList.toggle("invisible_reply")
    if (this.textContent.includes("件の返信を見る")) {
      this.innerHTML = '<span style="color: #2b8f38;">閉じる</span>';
    } else {
      this.innerHTML = `<span style="color: #2b8f38;">${text}</span>`;
    }
  });
});

const details = document.querySelectorAll(".detail");
const descriptions = document.querySelectorAll(".description");

details.forEach(function (detail, index) {
  detail.addEventListener("click", function () {
    const description = descriptions[index];
    description.classList.toggle("expanded");
    if (description.classList.contains("expanded")) {
      detail.textContent = "...閉じる";
    } else {
      detail.textContent = "...もっと見る";
    }
  });
});

//もし動画の説明文があまり長くない(3行以下)なら「もっと見る」を表示しない
descriptions.forEach(function (description, index) {
  const detail = details[index];
  if (description.scrollHeight <= description.offsetHeight) {
    detail.style.display = "none";
  }
});

const textarea = document.getElementById("id_content");

textarea.addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = this.scrollHeight + "px";
});

// djangoのdocument(https://docs.djangoproject.com/ja/5.1/howto/csrf/)からコピペ、クッキーを取得する関数
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

if (createdSelf == false) {
  document.querySelector(".follow-btn").addEventListener("click", function (event) {
    event.preventDefault();
    fetch(followBtnUrl, {
      method: "POST",
      body: "target_user_pk=" + targetUserPk,
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
}

document.getElementById("favorite-btn").addEventListener("click", function (event) {
  event.preventDefault();
  fetch(favoriteBtnUrl, {
    method: "POST",
    body: "target_movie_pk=" + targetMoviePk,
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
      // フォロワー数を更新
      document.getElementById("favorite_count").textContent = response.like_count;
      // ボタンの状態を変更する
      const favoriteBtnImage = document.getElementById("favorite-btn__image");
      if (response.method == "favorite") {
        favoriteBtnImage.src = favoriteFillSrc;
      } else if (response.method == "unfavorite") {
        favoriteBtnImage.src = favoriteSrc;
      }
    })
    .catch((error) => {
      console.log(error);
    });
});

const form_expanders = document.querySelectorAll(".form_expander");
const reply_textareas = document.querySelectorAll(".reply_textarea");
const reply_forms = document.querySelectorAll(".reply_form_class")
let previous = "";

form_expanders.forEach(function (form_expander) {
  form_expander.addEventListener("click", function () {
    let tfvalue = this.nextElementSibling.classList.contains("invisible_reply");
    form_expanders.forEach(function (other_expander) {
      other_expander.nextElementSibling.classList.add("invisible_reply");
    });
    if (tfvalue) {
      this.nextElementSibling.classList.remove("invisible_reply");
    } else {
      this.nextElementSibling.classList.add("invisible_reply");
    }
    if (this !== previous) {
      this.nextElementSibling.firstElementChild.firstElementChild.nextElementSibling.value = "";
    }
    previous = this
  });
});

reply_textareas.forEach(function (reply_textarea) {
  reply_textarea.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = this.scrollHeight + "px";
  });
})

reply_forms.forEach(function (reply_form) {
  const reply_textarea_base = reply_form.firstElementChild.nextElementSibling
  const reply_defaultheight = reply_textarea_base.style.height
  reply_form.addEventListener("submit", function (e) {
    const reply_trimmedValue = reply_textarea_base.value.trim();
    if (reply_trimmedValue === "") {
      e.preventDefault();
      reply_textarea_base.value = "";
      reply_textarea_base.style.height = reply_defaultheight;
      reply_textarea_base.reportValidity();
    }
  });
})

const stoppers = document.querySelectorAll(".stopper")

stoppers.forEach(function (stopper) {
  stopper.addEventListener("click", function (e) {
    e.stopPropagation();
  });
});
