document.querySelector(".detail").addEventListener("click", function () {
  const detail = document.querySelector(".detail");
  const description = document.querySelector(".description");
  description.classList.toggle("expanded");
  if (description.classList.contains("expanded")) {
    detail.textContent = "...閉じる";
  } else {
    detail.textContent = "...もっと見る";
  }
});

// ここは必要なのかわからないので一旦コメントアウトします
// if (description.scrollHeight <= description.offsetHeight) {
//   detail.style.display = 'none'
// }

