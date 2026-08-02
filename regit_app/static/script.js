const btn = document.getElementById("btn");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");
const input = document.getElementById("value_form");
const decide = document.getElementById("decide");

if (btn && sidebar && overlay) {
    btn.addEventListener("click", () => {
        sidebar.classList.toggle("active");
        overlay.classList.toggle("active");
    });

    overlay.addEventListener("click", () => {
        sidebar.classList.remove("active");
        overlay.classList.remove("active");
    });
}

if (input) {

    // 保存された値を復元
    input.value = localStorage.getItem("dice_value") || "";

    // 入力中に保存
    input.addEventListener("input", () => {
        localStorage.setItem("dice_value", input.value);
    });
}

// 決定ボタンを押したときだけ削除
if (decide) {
    decide.addEventListener("click", () => {
        localStorage.removeItem("dice_value");
    });
}