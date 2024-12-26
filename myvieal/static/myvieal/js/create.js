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

const tag_section = document.querySelector("div.tag");
const tag_contents = document.querySelectorAll("div.tag_input *");
const tag_create_button = document.querySelector(".tag_create_button");
const tag_select_wrapper = document.querySelector(".tag_select_wrapper");
const tag_select_button = document.querySelector('input[name="tag_list"]');
const genre_list = document.querySelector(".genre_list");
const genre_label = document.querySelectorAll(".genre_list p");
const tag_list = document.querySelector(".tag_list");
let tag_label = document.querySelectorAll(".tag_list p");

tag_create_button.addEventListener("click", () => {});

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
        const response = await fetch(`/get_tags/${element.id}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-CSRFToken": "{{ csrf_token }}",
          },
        });
        const jsonresponse = await response.json();
        if (jsonresponse.tags.length > 0) {
          jsonresponse.tags.forEach((book) => {
            const tag_element = document.createElement("p");
            tag_element.textContent = book;
            tag_list.appendChild(tag_element);
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

function set_tag_click() {
  tag_label.forEach((element) => {
    element.addEventListener("click", () => {
      tag_select_button.value = `#${element.textContent}`;
      genre_list.classList.remove("active");
      tag_list.classList.remove("active");

      //さらにタグを追加するためのボタンを作成
      const new_tag_input = document.createElement("div");
      new_tag_input.classList.add("tag_select_wrapper");
      new_tag_input.textContent = "新しいよ";
      tag_section.appendChild(new_tag_input);
    });
  });
}
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
