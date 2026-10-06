const tg = window.Telegram.WebApp;

tg.ready();
tg.expand();

const user = tg.initDataUnsafe?.user;

if (user) {
    document.getElementById("userName").textContent =
        `Salom, ${user.first_name}!`;
}

let mining = false;
let seconds = 24 * 60 * 60;

const timer = document.getElementById("timer");
const status = document.getElementById("miningStatus");
const button = document.getElementById("startMining");

function updateTimer() {

    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    timer.textContent =
        `${String(hours).padStart(2, "0")}:` +
        `${String(minutes).padStart(2, "0")}:` +
        `${String(secs).padStart(2, "0")}`;
}

button.addEventListener("click", () => {

    if (mining) return;

    mining = true;

    status.textContent = "🟢 Mining faol";
    button.textContent = "⛏ MINING ISHLAMOQDA";
    button.disabled = true;

    const interval = setInterval(() => {

        seconds--;

        updateTimer();

        if (seconds <= 0) {

            clearInterval(interval);

            mining = false;

            status.textContent = "🔴 Mining tugadi";

            button.textContent = "▶️ START MINING";
            button.disabled = false;

            seconds = 24 * 60 * 60;

            updateTimer();
        }

    }, 1000);
});

updateTimer();
