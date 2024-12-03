document.getElementById("image-input").addEventListener("change", function(event) {
  var file = event.target.files[0];
  var iconPreview = document.querySelector(".icon-preview");



  // FileReaderで動画のURLを作成
  var reader = new FileReader();

  reader.onload = function(e) {
    iconPreview.src = reader.result;  // 動画のプレビューを表示
  }

  // 動画ファイルを読み込む
  reader.readAsDataURL(file);
});

const usernameForm = document.querySelector('textarea[name="username"]');
const usernameLength = document.querySelector('.username-length');
usernameLength.textContent = usernameLength.textContent = `${usernameForm.value.length}/50`;
usernameForm.addEventListener('input', function() {
  usernameLength.textContent = `${usernameForm.value.length}/50`;
});

const introductionForm = document.querySelector('textarea[name="introduction"]');
const introductionLength = document.querySelector('.introduction-length');
introductionLength.textContent = introductionLength.textContent = `${introductionForm.value.length}/500`;
introductionForm.addEventListener('input', function() {
  introductionLength.textContent = `${introductionForm.value.length}/500`;
});
