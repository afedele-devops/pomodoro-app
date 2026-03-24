const progressCircle = document.querySelector(".progress");
const radius = 110;
const circumference = 2 * Math.PI * radius;
progressCircle.style.strokeDasharray = circumference;
progressCircle.style.strokeDashoffset = circumference; // empieza vacío

let totalTime = 0;

function setProgress(timeLeft) {
    const elapsed = totalTime - timeLeft;
    const percent = elapsed / totalTime;
    const offset = circumference * (1 - percent);
    progressCircle.style.strokeDashoffset = offset;
}

async function updateDisplay() {
    const response = await fetch("/status");
    const data = await response.json();

    let minutes = Math.floor(data.time_left / 60);
    let seconds = data.time_left % 60;
    document.getElementById("timer").innerText =
        String(minutes).padStart(2, '0') + ":" + String(seconds).padStart(2, '0');

    // Cambiar fondo y duración según modo
    let modeText = "";
    if (data.mode === "work") {
        modeText = "Trabajo";
        document.body.style.background = "#f44336"; // rojo
    } else if (data.mode === "long_break") {
        modeText = "Descanso largo";
        document.body.style.background = "#2196F3"; // azul
    } else {
        modeText = "Descanso corto";
        document.body.style.background = "#4CAF50"; // verde
    }
    document.getElementById("mode").innerText = modeText;

    // Actualizar totalTime solo cuando arranca un nuevo bloque
    if (!data.running && data.time_left > 0) {
        totalTime = data.time_left;
    } else if (totalTime === 0) {
        totalTime = data.time_left;
    }

    setProgress(data.time_left);
}

async function startTimer() {
    await fetch("/start", { method: "POST" });
}

async function pauseTimer() {
    await fetch("/pause", { method: "POST" }); 
}

async function resetTimer() {
    await fetch("/reset", { method: "POST" });
}

// Actualizar cada segundo
setInterval(updateDisplay, 1000);
updateDisplay();
