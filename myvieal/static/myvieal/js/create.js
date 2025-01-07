document.getElementById("image-input").addEventListener("change", function (event) {
  var file = event.target.files[0];
  var thumbnailPreview = document.querySelector(".thumbnail-preview");

  var reader = new FileReader();

  reader.onload = function (e) {
    thumbnailPreview.src = reader.result;
    thumbnailPreview.style.display = "block";
  };
  reader.readAsDataURL(file);
});

document.getElementById("file-input").addEventListener("change", function (event) {
  var file = event.target.files[0];
  var videoPreview = document.querySelector(".video-preview");

  // FileReaderで動画のURLを作成
  var reader = new FileReader();

  reader.onload = function () {
    videoPreview.src = reader.result; // 動画のプレビューを表示
    videoPreview.style.display = "block"; // プレビューを表示
  };

  // 動画ファイルを読み込む
  reader.readAsDataURL(file);
});

const titleForm = document.querySelector('textarea[name="title"]');
const titleLength = document.querySelector(".title-length");
titleForm.addEventListener("input", function () {
  titleLength.textContent = `${titleForm.value.length}/50`;
});

const explanationForm = document.querySelector('textarea[name="explanation"]');
const explanationLength = document.querySelector(".explanation-length");
explanationForm.addEventListener("input", function () {
  explanationLength.textContent = `${explanationForm.value.length}/500`;
});

// タグ機能 ここから

const tag_section = document.querySelector(".tag");
const tag_contents = document.querySelectorAll("div.tag_input *");
const tag_select_wrapper = document.querySelector(".tag_select_wrapper");
const tag_input_text = document.querySelector(".tag_input_text");
const genre_list = document.querySelector(".genre_list");
const genre_label = document.querySelectorAll(".genre_list p");
const tag_list = document.querySelector(".tag_list");
let tag_label = document.querySelectorAll(".tag_list p");

tag_select_wrapper.addEventListener("click", () => {
  genre_list.classList.add("active");
});

document.addEventListener("click", (event) => {
  // クリックした要素が除外リストに含まれるかチェック
  const isExcluded = Array.from(tag_contents).some((div) => div.contains(event.target));
  if (!isExcluded) {
    genre_list.classList.remove("active");
    tag_list.classList.remove("active");
  }
});

//一覧表示されたジャンル名に対してクリックイベントを付与する
genre_label.forEach((element) => {
  element.addEventListener("click", () => {
    genre_label.forEach((e) => e.classList.remove("active"));
    tag_list.innerHTML = ""; //appendChild()が重複しないように空にする
    element.classList.add("active");
    const showGenreContent = async () => {
      try {
        const response = await fetch(`/get_tags/${element.getAttribute("id")}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-CSRFToken": "{{ csrf_token }}",
          },
        });
        const jsonresponse = await response.json();
        if (jsonresponse.tag_list.length > 0) {
          jsonresponse.tag_list.forEach((tag) => {
            const tag_element = document.createElement("p");
            tag_element.setAttribute("name", tag.id);
            tag_element.textContent = tag.name;
            tag_list.appendChild(tag_element);
            tag_list.classList.add("active");
          });
          tag_label = document.querySelectorAll(".tag_list p");
          set_tag_click(); //一覧表示されるタグそれぞれにクリックイベントを追加する
        } else {
          const tag_element = document.createElement("p");
          tag_element.textContent = "該当するタグがありません";
          tag_list.appendChild(tag_element);
          tag_list.classList.add("active");
        }
      } catch (err) {
        console.log("Error log: " + err);
      }
    };
    showGenreContent();
  });
});

// タグそれぞれに対して、クリックした際の動作を設定する関数
function set_tag_click() {
  tag_label.forEach((element) => {
    element.addEventListener("click", () => {
      genre_list.classList.remove("active");
      tag_list.classList.remove("active");

      //選択されたタグを表示するdivを”タグを入力”の上に追加する
      const tag_hidden_value = document.createElement("input");
      const new_tag_input = document.createElement("p");
      const tag_cancel_btn = document.createAttribute("div");
      const img = document.createElement("img");
      const new_tag_div = document.createElement("div");

      tag_hidden_value.type = "text";
      tag_hidden_value.name = "tag_list";
      tag_hidden_value.value = element.getAttribute("name");

      new_tag_div.classList.add("tag_container");

      new_tag_input.textContent = `#${element.textContent}`;
      new_tag_input.classList.add("tag_input_text");
      new_tag_input.classList.add("added");

      img.src = document.querySelector(".image_url_indicator").getAttribute("url");
      img.classList.add("tag_cancel_btn");
      img.addEventListener("click", (event) => {
        // クリックされたボタンの親要素であるboxクラスのdivを削除
        const box = event.target.closest(".tag_container"); // 一番近いdivを探す
        if (box) {
          box.remove(); // 削除
        }
      });

      new_tag_div.appendChild(new_tag_input);
      // new_tag_div.appendChild(tag_cancel_btn)
      new_tag_div.appendChild(img);

      const tag_input_div = document.querySelector(".tag_input");
      tag_section.insertBefore(new_tag_div, tag_input_div);
      tag_section.insertBefore(new_tag_div, tag_input_div);
      tag_section.insertBefore(tag_hidden_value, tag_input_div);
    });
  });
}

// タグ作成機能
const tag_create_button = document.querySelector(".tag_create_button");
const modalDialog = document.querySelector("#modalDialog");
const cancel_btn = document.querySelector(".cancel_button");
const tag_create_text = document.querySelector("#tag_create_text");

tag_create_button.addEventListener("click", () => {
  modalDialog.showModal();
  // モーダルダイアログを表示する際に背景部分がスクロールしないようにする
  document.documentElement.style.overflow = "hidden";
});

cancel_btn.addEventListener("click", () => {
  modalDialog.close();
  document.documentElement.style.overflow = "scroll";
  tag_create_text.value = "";
});

const tag_create_form = document.querySelector("#tag_create_form");
const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

tag_create_form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(tag_create_form);
  await fetch("/create-tag/", {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": csrfToken,
    },
  });
  modalDialog.close();
  document.documentElement.style.overflow = "scroll";
  tag_create_text.value = "";
});

// タグ機能 ここまで

let autocomplete;
function initMap() {
  const input = document.getElementById("pac-input");
  autocomplete = new google.maps.places.Autocomplete(input, {
    fields: ["place_id", "name", "formatted_address"],
  });

  autocomplete.addListener("place_changed", function () {
    const place = autocomplete.getPlace();

    if (place.place_id) {
      input.value = place.name;
      document.getElementById("place_id").value = place.place_id;
      document.getElementById("address").value = place.formatted_address;
    }
  });
}
