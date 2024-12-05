const detail = document.querySelector('.detail');
const description = document.querySelector('.description');
document.querySelector('.detail').addEventListener('click', () => {

  description.classList.toggle('expanded');
  if (description.classList.contains('expanded')) {
    detail.textContent = '...閉じる';
  } else {
    detail.textContent = '...もっと見る';
  }
})

//もし動画の説明文があまり長くない(3行以下)なら「もっと見る」を表示しない
if (description.scrollHeight <= description.offsetHeight) {
  detail.style.display = 'none'
}
