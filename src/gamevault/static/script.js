function toggleMenu() {
  const menu = document.getElementById("side-menu");
  menu.classList.toggle("open");
}

// Close menu when clicking outside
document.addEventListener("click", function (event) {
  const menu = document.getElementById("side-menu");
  const button = document.querySelector(".menu-button");

  const clickedInsideMenu = menu.contains(event.target);
  const clickedButton = button.contains(event.target);

  if (!clickedInsideMenu && !clickedButton) {
    menu.classList.remove("open");
  }
});