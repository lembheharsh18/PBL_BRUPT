document.addEventListener("DOMContentLoaded", function () {
  const hamburgerMenu = document.querySelector(".hamburger-menu");
  const container = document.querySelector(".container");

  hamburgerMenu.addEventListener("click", function () {
    container.classList.toggle("active");
  });
});
