document.getElementById("image-input").addEventListener("change", function(event) {
  var file = event.target.files[0];
  var thumbnailPreview = document.querySelector(".thumbnail-preview");

  var reader = new FileReader();

  reader.onload = function(e) {
    thumbnailPreview.src = reader.result;
    thumbnailPreview.style.display = "block";
  }
  reader.readAsDataURL(file);
});

document.getElementById("file-input").addEventListener("change", function(event) {
  var file = event.target.files[0];
  var videoPreview = document.querySelector(".video-preview");

// FileReaderで動画のURLを作成
  var reader = new FileReader();

  reader.onload = function(e) {
    videoPreview.src = reader.result;  // 動画のプレビューを表示
    videoPreview.style.display = "block";  // プレビューを表示
  }

  // 動画ファイルを読み込む
  reader.readAsDataURL(file);
});

