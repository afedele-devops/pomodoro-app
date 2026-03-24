from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import time
import threading

import config  # importamos las duraciones

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Variables de temporizador y ciclos
timer_running = False
end_time = None
paused_time_left = config.WORK_DURATION
mode = "work"  # "work" | "short_break" | "long_break"
cycle_count = 0
lock = threading.Lock()

@app.get("/")
def read_root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.post("/start")
def start_timer():
    global timer_running, end_time, paused_time_left
    with lock:
        if not timer_running:
            end_time = time.time() + paused_time_left
            timer_running = True
    return {"status": "started", "mode": mode}

@app.post("/pause")
def pause_timer():
    global timer_running, end_time, paused_time_left
    with lock:
        if timer_running and end_time:
            paused_time_left = max(0, int(end_time - time.time()))
        timer_running = False
    return {"status": "paused", "time_left": paused_time_left, "mode": mode}

@app.post("/reset")
def reset_timer():
    global timer_running, end_time, paused_time_left, mode, cycle_count
    with lock:
        timer_running = False
        mode = "work"
        cycle_count = 0
        paused_time_left = config.WORK_DURATION
        end_time = None
    return {"status": "reset", "mode": mode, "time_left": paused_time_left}

@app.get("/status")
def get_status():
    global timer_running, end_time, paused_time_left, mode, cycle_count
    with lock:
        if not timer_running or end_time is None:
            return {
                "running": False,
                "time_left": paused_time_left,
                "mode": mode,
                "cycle": cycle_count
            }

        time_left = int(end_time - time.time())
        if time_left <= 0:
            # Cambiar de modo
            if mode == "work":
                cycle_count += 1
                if cycle_count % 4 == 0:
                    mode = "long_break"
                    paused_time_left = config.LONG_BREAK
                else:
                    mode = "short_break"
                    paused_time_left = config.SHORT_BREAK
            else:
                mode = "work"
                paused_time_left = config.WORK_DURATION

            # Auto‑start del nuevo bloque
            end_time = time.time() + paused_time_left
            timer_running = True

            return {
                "running": True,
                "time_left": paused_time_left,
                "mode": mode,
                "cycle": cycle_count
            }

        return {
            "running": True,
            "time_left": time_left,
            "mode": mode,
            "cycle": cycle_count
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
