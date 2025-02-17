const formJs = document.getElementById("form_js");
const submitJsMultiple = document.querySelectorAll(".submit_js");

formJs.addEventListener("submit", function () {
  submitJsMultiple.forEach(function (submitJs) {
    submitJs.disabled = true;
    submitJs.classList.add("submitting");
  });
});
