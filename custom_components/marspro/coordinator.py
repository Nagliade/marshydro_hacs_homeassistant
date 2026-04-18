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

        self.hass = hass
        self.mac = mac
        self.data = {}
        self._connected = False

        # =========================
        # MQTT CLIENT
        # =========================
        self.client = mqtt.Client(client_id=f"mars_{mac}", clean_session=True)
        self.client.username_pw_set(username, password)
        self.client.reconnect_delay_set(min_delay=5, max_delay=60)

        # =========================
        # TLS SETUP vorbereiten
        # =========================
        self.ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        base_path = os.path.dirname(__file__)
        self.cert_file = os.path.join(base_path, "emqx-marspro.pem")
        self.key_file = os.path.join(base_path, "emqx-marspro.key")

        print("📂 Zertifikat:", self.cert_file)
        print("📂 Key:", self.key_file)

        # 👉 Async Start (HA konform)
        hass.async_create_task(self._async_setup())

    # =========================
    # ASYNC SETUP
    # =========================
    async def _async_setup(self):
        try:
            # Zertifikate NON-BLOCKING laden
            await self.hass.async_add_executor_job(
                self.ctx.load_cert_chain,
                self.cert_file,
                self.key_file
            )

            print("✅ Zertifikate geladen")

            self.client.tls_set_context(self.ctx)

            # Callbacks setzen
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            self.client.on_message = self._on_message

            # MQTT starten
            self._start_mqtt()

        except Exception as e:
            print("❌ TLS Setup Fehler:", e)

    # =========================
    # MQTT START THREAD
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

            # 👉 HA informieren
            self.async_set_updated_data(self.data)

        except Exception as e:
            print("❌ Mars MQTT Error:", e)