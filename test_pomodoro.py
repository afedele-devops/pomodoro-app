import pytest
import subprocess
import time
import signal
import os
import json
from playwright.sync_api import sync_playwright

import config  # usamos las duraciones configuradas

def format_time(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"

@pytest.fixture(scope="session", autouse=True)
def run_server():
    server = subprocess.Popen(
        ["python", "pomodoro.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    time.sleep(3)  # esperar a que arranque
    yield
    os.killpg(server.pid, signal.SIGTERM)

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

def test_backend_timer_flow(browser):
    page = browser.new_page()
    page.goto("http://127.0.0.1:8000")

    expected_start = format_time(config.WORK_DURATION)
    assert page.inner_text("#timer") == expected_start
    assert page.inner_text("#mode") == "Trabajo"

    page.click("button.start")
    page.wait_for_timeout(3000)
    assert page.inner_text("#timer") != expected_start

    # Pausar temporizador
    page.click("button.pause")
    current_value = page.inner_text("#timer")
    page.wait_for_timeout(2000)
    new_value = page.inner_text("#timer")
    assert new_value == current_value or abs(
        int(new_value.split(":")[1]) - int(current_value.split(":")[1])
    ) <= 1

    page.click("button.reset")
    page.wait_for_timeout(1000)
    assert page.inner_text("#timer") == expected_start
    assert page.inner_text("#mode") == "Trabajo"


def test_mode_changes_with_mock(browser):
    page = browser.new_page()

    mock_states = [
        {"running": False, "time_left": 25*60, "mode": "work", "cycle": 0},
        {"running": False, "time_left": 5*60, "mode": "short_break", "cycle": 1},
        {"running": False, "time_left": 15*60, "mode": "long_break", "cycle": 4},
    ]
    state_index = {"value": 0}

    def mock_status(route, request):
        if "status" in request.url:
            response = mock_states[state_index["value"]]
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(response)
            )
        else:
            route.continue_()

    page.route("**/status", mock_status)
    page.goto("http://127.0.0.1:8000")

    # Primer mock: modo trabajo
    state_index["value"] = 0
    page.evaluate("updateDisplay()")
    page.wait_for_timeout(500)
    assert page.inner_text("#mode") == "Trabajo"

    # Segundo mock: descanso corto
    state_index["value"] = 1
    page.evaluate("updateDisplay()")
    page.wait_for_timeout(500)
    assert page.inner_text("#mode") == "Descanso corto"

    # Tercer mock: descanso largo
    state_index["value"] = 2
    page.evaluate("updateDisplay()")
    page.wait_for_timeout(500)
    assert page.inner_text("#mode") == "Descanso largo"
