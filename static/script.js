const progressCircle = document.querySelector(".progress");
const radius = 110;
const circumference = 2 * Math.PI * radius;
progressCircle.style.strokeDasharray = circumference;
progressCircle.style.strokeDashoffset = circumference; // empieza vacío

let totalTime = 0;
let lastMode = null;

function setProgress(timeLeft) {
    if (totalTime <= 0) return;

    const elapsed = totalTime - timeLeft;
    let percent = totalTime > 0 ? elapsed / totalTime : 0;
    percent = Math.max(0, Math.min(1, percent)); // clamp 0..1

    let offset;
    if (timeLeft <= 0) {
        // al terminar el bloque, mostrar lleno
        offset = 0;
    } else {
        // empieza vacío (offset = circumference) y se llena hasta 0
        offset = circumference * (1 - percent);
    }

    progressCircle.style.strokeDashoffset = offset;
}

async function updateDisplay() {
    const response = await fetch("/status");
    const data = await response.json();

    const minutes = Math.floor(data.time_left / 60);
    const seconds = data.time_left % 60;
    document.getElementById("timer").innerText =
        String(minutes).padStart(2, '0') + ":" + String(seconds).padStart(2, '0');

    // Cambiar fondo y texto según modo
    let modeText = "";
    if (data.mode === "work") {
        modeText = "Trabajo";
        document.body.style.background = "#f44336";
    } else if (data.mode === "long_break") {
        modeText = "Descanso largo";
        document.body.style.background = "#2196F3";
    } else {
        modeText = "Descanso corto";
        document.body.style.background = "#4CAF50";
    }
    document.getElementById("mode").innerText = modeText;

    // Reiniciar totalTime cuando cambia el modo
    if (lastMode !== data.mode) {
        totalTime = data.time_left;
        lastMode = data.mode;

        // estado visual inicial: vacío al comenzar el bloque
        progressCircle.style.strokeDashoffset = circumference;
    }

    setProgress(data.time_left);
}

// Actualizar cada segundo
setInterval(updateDisplay, 1000);
updateDisplay();

async function startTimer() {
    await fetch("/start", { method: "POST" });
}

async function pauseTimer() {
    await fetch("/pause", { method: "POST" }); 
}

async function resetTimer() {
    await fetch("/reset", { method: "POST" });
}
