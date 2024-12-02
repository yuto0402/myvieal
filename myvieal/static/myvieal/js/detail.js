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

if (description.scrollHeight <= description.offsetHeight) {
  detail.style.display = "none";
}
