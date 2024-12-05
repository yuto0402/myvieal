document.getElementById("image-input").addEventListener("change", function(event) {
  let file = event.target.files[0];
  let thumbnailPreview = document.querySelector(".thumbnail-preview");



  // FileReaderで動画のURLを作成
  const reader = new FileReader();

  reader.onload = (e) => {
    thumbnailPreview.src = reader.result;  // 動画のプレビューを表示
    thumbnailPreview.style.display = "block";  // プレビューを表示
  }

  // 動画ファイルを読み込む
  reader.readAsDataURL(file);
});

const titleForm = document.querySelector('textarea[name="title"]');
const titleLength = document.querySelector('.title-length');
titleLength.textContent = titleLength.textContent = `${titleForm.value.length}/50`;
titleForm.addEventListener('input', () => {
  titleLength.textContent = `${titleForm.value.length}/50`;
});

const explanationForm = document.querySelector('textarea[name="explanation"]');
const explanationLength = document.querySelector('.explanation-length');
explanationLength.textContent = `${explanationForm.value.length}/50`;
explanationForm.addEventListener('input', () => {
  explanationLength.textContent = `${explanationForm.value.length}/500`;
});

