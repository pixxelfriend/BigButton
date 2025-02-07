import usb.core
import usb.util
import time

# Beispiel Vendor und Product ID
VENDOR_ID = 0x045e  # Microsoft Corporation
PRODUCT_ID = 0x02a0  # Beispiel Product ID

# Suchen Sie das USB-Gerät
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
    raise ValueError('Gerät nicht gefunden')

dev.set_configuration()

interface = 0  # Beispielinterface
endpoint = 0x81  # Beispiel für einen In-Endpoint

timeout = 2000  # Timeout auf 2 Sekunden setzen

# Funktion zur Identifizierung der Geräte anhand der empfangenen Daten
def identify_device(data):
    # Basierend auf dem dritten Wert im Array (0-indexiert) das Gerät bestimmen
    if len(data) > 2:
        device_id = data[2]
        if device_id == 1:
            return "Rot"
        elif device_id == 3:
            return "Gelb"
        elif device_id == 0:
            return "Grün"
        elif device_id == 2:
            return "Blau"
        else:
            return "Unbekannt"
    return "Unbekannt"

# Zuordnung der Button-Daten zu den Button-Namen
BUTTONS = {
    8: "Big Button",
    16: "A",
    32: "B",
    64: "X",
    128: "Y",
    4: "XBOX"
}

# Funktion zur Identifikation des gedrückten Buttons
def get_button_name(data):
    """Identifiziere den gedrückten Button basierend auf den letzten beiden Werten."""
    if len(data) < 5:
        return "Unbekannt"

    last_value = data[4]
    second_last_value = data[3]

    # Buttons "Back" und "Start" haben unterschiedliche Codierungen
    if second_last_value == 32 and last_value == 0:
        return "Back"
    elif second_last_value == 16 and last_value == 0:
        return "Start"

    # Überprüfen der üblichen Buttons
    return BUTTONS.get(last_value, "Unbekannt")

try:
    while True:
        # Überprüfen Sie, ob Daten vorhanden sind
        try:
            data = dev.read(endpoint, 64, timeout=timeout)
            device_name = identify_device(data)
            button_name = get_button_name(data)
            print(f"{device_name} - {button_name}: Empfangene Daten: {data}")
        except usb.core.USBTimeoutError:
            print("Warten auf Daten...")
        time.sleep(0.5)  # Regelmäßig prüfen, ohne Blockieren
except KeyboardInterrupt:
    print("Beenden...")
finally:
    usb.util.release_interface(dev, interface)
