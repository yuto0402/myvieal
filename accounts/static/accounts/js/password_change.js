// 表示・非表示の切り替え
const show = document.querySelectorAll(".eye");
show.forEach((button) => {
  button.addEventListener("click", function () {
    const input = this.previousElementSibling;
    const type = input.getAttribute("type");
    if (type === "password") {
      input.setAttribute("type", "text");
      this.setAttribute("src", this.dataset.show);
    } else {
      input.setAttribute("type", "password");
      this.setAttribute("src", this.dataset.hide);
    }
  });
});

// フォーム送信時にパスワードフィールドをすべてtype="password"に戻す
document.querySelector("form").addEventListener("submit", function () {
  document.querySelectorAll('input[type="text"]').forEach((input) => {
    input.setAttribute("type", "password");
  });
});
