document.getElementById("image-input").addEventListener("change", function (event) {
  var file = event.target.files[0];
  var thumbnailPreview = document.querySelector(".thumbnail-preview");
  var reader = new FileReader();

  reader.onload = function () {
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

const tag_create_button = document.querySelector(".tag_create_button");
tag_create_button.addEventListener("click", () => {
  console.log("いいね！");
});

// タグ機能 ここまで
