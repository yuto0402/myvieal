const detail = document.querySelector('.detail');
const introduction = document.querySelector('.introduction');
document.querySelector('.detail').addEventListener('click', function() {
introduction.classList.toggle('expanded');
  if (introduction.classList.contains('expanded')) {
    detail.textContent = '...閉じる';
  } else {
    detail.textContent = "...もっと見る";
  }
});

if (introduction.scrollHeight <= introduction.offsetHeight) {
  detail.style.display = "none";
}
