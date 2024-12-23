var navBtnFollowing = document.getElementById("nav__btn--following");
var navBtnFavorite = document.getElementById("nav__btn--favorite");

var followingList = document.getElementById("following-list");
var movieList = document.getElementById("movie-list");

navBtnFavorite.addEventListener("click", function (event) {
  event.preventDefault();
  if (navBtnFavorite != document.getElementsByClassName("nav__btn--selected")) {
    followingList.style.display = "none";
    movieList.style.display = "block";

    navBtnFollowing.classList.remove("nav__btn--selected");
    navBtnFavorite.classList.add("nav__btn--selected");
  }
});

navBtnFollowing.addEventListener("click", function (event) {
  event.preventDefault();
  if (navBtnFollowing != document.getElementsByClassName("nav__btn--selected")) {
    followingList.style.display = "block";
    movieList.style.display = "none";

    navBtnFavorite.classList.remove("nav__btn--selected");
    navBtnFollowing.classList.add("nav__btn--selected");
  }
});
