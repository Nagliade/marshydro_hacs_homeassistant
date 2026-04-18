import ssl
import json
import os
import time
import threading
import paho.mqtt.client as mqtt

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import MARS_HOST, MARS_PORT


class MarsCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, mac, username, password):
        super().__init__(hass, None, name="MarsPro")

        self.mac = mac
        self.data = {}
        self._connected = False

        # =========================
        # MQTT CLIENT
        # =========================
        self.client = mqtt.Client(client_id=f"mars_{mac}", clean_session=True)
        self.client.username_pw_set(username, password)

        # Auto-Reconnect Settings
        self.client.reconnect_delay_set(min_delay=5, max_delay=60)

        # =========================
        # TLS SETUP
        # =========================
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        base_path = os.path.dirname(__file__)
        cert_file = os.path.join(base_path, "emqx-marspro.pem")
        key_file = os.path.join(base_path, "emqx-marspro.key")

        ctx.load_cert_chain(cert_file, keyfile=key_file)

        self.client.tls_set_context(ctx)

        # =========================
        # CALLBACKS
        # =========================
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

        # =========================
        # START THREAD
        # =========================
        self._start_mqtt()

    # =========================
    # START MQTT LOOP
    # =========================
    def _start_mqtt(self):
        def run():
            while True:
                try:
                    print("🔌 Connecting to Mars MQTT...")
                    self.client.connect(MARS_HOST, MARS_PORT, keepalive=60)
                    self.client.loop_forever()
                except Exception as e:
                    print("❌ MQTT Fehler:", e)
                    time.sleep(5)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

    # =========================
    # EVENTS
    # =========================
    def _on_connect(self, client, userdata, flags, rc, properties=None):
        print("✅ Mars MQTT connected:", rc)
        self._connected = True

        topic = f"MHPRO/CB43/API/UP/{self.mac}"
        client.subscribe(topic)
        print("📡 Subscribed to:", topic)

    def _on_disconnect(self, client, userdata, rc, properties=None):
        self._connected = False
        print("⚠️ Mars MQTT disconnected:", rc)

    def _on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            data = json.loads(payload)

            if "data" not in data:
                return

            self.data = data["data"]
            self.async_set_updated_data(self.data)

        except Exception as e:
            print("❌ Mars MQTT Error:", e)