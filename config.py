
# Cambiar a True para pruebas rápidas
DEMO_MODE = False

if DEMO_MODE:
    WORK_DURATION = 6
    SHORT_BREAK  = 6
    LONG_BREAK   = 6
else:
    WORK_DURATION = 25 * 60
    SHORT_BREAK  = 5 * 60
    LONG_BREAK   = 15 * 60
