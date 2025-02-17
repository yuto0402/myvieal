const form_js = document.getElementById("form_js");
const submit_js = document.getElementById("submit_js");

form_js.addEventListener("submit", function () {
  submit_js.disabled = true;
  submit_js.classList.add("submitting");
})
