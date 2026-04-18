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

        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)

        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # load certs from /config/marspro/
        base = hass.config.path("marspro")
        cert = os.path.join(base, "emqx-marspro.pem")
        key = os.path.join(base, "emqx-marspro.key")

        if os.path.exists(cert) and os.path.exists(key):
            ctx.load_cert_chain(cert, key)
        else:
            print("⚠️ MarsPro certs not found in /config/marspro/")

        self.client.tls_set_context(ctx)

        self.client.on_message = self._on_message
        self.client.connect(MARS_HOST, MARS_PORT)
        self.client.subscribe(f"MHPRO/CB43/API/UP/{mac}")
        self.client.loop_start()

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            if "data" not in payload:
                return
            self.data = payload["data"]
            self.async_set_updated_data(self.data)
        except Exception as e:
            print("Mars error:", e)
