const delete_btn = document.querySelector(".account_delete_button");
const cancel_btn = document.querySelector(".cancel_button");
const modalDialog = document.querySelector("#modalDialog");

delete_btn.addEventListener("click", () => {
  modalDialog.showModal();
  // モーダルダイアログを表示する際に背景部分がスクロールしないようにする
  document.documentElement.style.overflow = "hidden";
});

cancel_btn.addEventListener("click", () => {
  modalDialog.close();
});
