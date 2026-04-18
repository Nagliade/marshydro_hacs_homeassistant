import ssl
import json
import os
import paho.mqtt.client as mqtt

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import MARS_HOST, MARS_PORT


class MarsCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, mac, username, password):
        super().__init__(hass, None, name="MarsPro")

        self.mac = mac
        self.data = {}

        # =========================
        # MQTT CLIENT
        # =========================
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)

        # =========================
        # TLS SETUP
        # =========================
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # 👉 Zertifikate aus dem gleichen Ordner laden
        base_path = os.path.dirname(__file__)

        cert_file = os.path.join(base_path, "emqx-marspro.pem")
        key_file = os.path.join(base_path, "emqx-marspro.key")

        if not os.path.exists(cert_file) or not os.path.exists(key_file):
            print("❌ MarsPro Zertifikate NICHT gefunden!")
            print("Pfad:", base_path)
        else:
            try:
                ctx.load_cert_chain(certfile=cert_file, keyfile=key_file)
                print("✅ Zertifikate erfolgreich geladen")
            except Exception as e:
                print("❌ Fehler beim Laden der Zertifikate:", e)

        self.client.tls_set_context(ctx)

        # =========================
        # CALLBACKS
        # =========================
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

        # =========================
        # CONNECT
        # =========================
        self.client.connect(MARS_HOST, MARS_PORT)
        self.client.loop_start()

    # =========================
    # MQTT EVENTS
    # =========================
    def _on_connect(self, client, userdata, flags, rc, properties=None):
        print("✅ Mars MQTT connected:", rc)

        topic = f"MHPRO/CB43/API/UP/{self.mac}"
        client.subscribe(topic)
        print("📡 Subscribed to:", topic)

    def _on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            data = json.loads(payload)

            if "data" not in data:
                return

            self.data = data["data"]

            # 👉 Home Assistant updaten
            self.async_set_updated_data(self.data)

        except Exception as e:
            print("❌ Mars MQTT Error:", e)

    def _on_disconnect(self, client, userdata, rc, properties=None):
        print("⚠️ Mars MQTT disconnected:", rc)

        while True:
            try:
                print("🔄 Reconnecting...")
                client.reconnect()
                break
            except Exception:
                import time
                time.sleep(5)