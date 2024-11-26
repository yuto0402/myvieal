document.getElementById("image-input").addEventListener("change", function (event) {
  var file = event.target.files[0];
  var thumbnailPreview = document.querySelector(".thumbnail-preview");

  // FileReaderで動画のURLを作成
  var reader = new FileReader();

  reader.onload = function (e) {
    thumbnailPreview.src = reader.result; // 動画のプレビューを表示
    thumbnailPreview.style.display = "block"; // プレビューを表示
  };

  // 動画ファイルを読み込む
  reader.readAsDataURL(file);
});
