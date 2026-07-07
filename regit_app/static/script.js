const btn = document.getElementById("btn");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");

btn.addEventListener("click", () => {
    sidebar.classList.toggle("active");
    overlay.classList.toggle("active");
});

/* 暗い部分クリックで閉じる */
overlay.addEventListener("click", () => {
    sidebar.classList.remove("active");
    overlay.classList.remove("active");
});