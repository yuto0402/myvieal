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
