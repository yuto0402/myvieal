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
})

const textarea = document.getElementById('id_content');

textarea.addEventListener('input', function () {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
});
