function openNav() {
    document.getElementById("mySidenav").classList.remove("-translate-x-full");
    document.getElementById("overlay").classList.remove("opacity-0", "invisible");
  }

function closeNav() {
    document.getElementById("mySidenav").classList.add("-translate-x-full");
    document.getElementById("overlay").classList.add("opacity-0", "invisible");
}