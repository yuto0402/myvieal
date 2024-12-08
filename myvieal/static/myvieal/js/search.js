const search_text = document.querySelector("#search-var");
search_text.addEventListener("click", (e) => {
  e.preventDefault;
  // const url = {% url "search" %};
  const showUsers = async () => {
    try {
      // const response = await fetch({% url "search-history" %})
      const jsonresponse = await response.json();
      console.log(jsonresponse);
    } catch (err) {
      console.log("Error log: " + err);
    }
  };
});

const cancel = document.querySelector(".cancel-button");
const search = document.querySelector("#search-bar");

cancel.setAttribute();

search.addEventListener("input", () => {
  cancel.setAttribute("display", "none");
});
