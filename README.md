# 🌱 Mars Hydro Pro MQTT Integration (Home Assistant)

Custom Home Assistant Integration für Mars Hydro Grow Geräte via MQTT.
Diese Integration verbindet dein Mars Hydro Pro Gerät direkt mit Home Assistant – ohne externe Scripts.

---

## ✨ Features

* 🌡 Temperatur
* 💧 Luftfeuchtigkeit
* 🫁 CO₂
* 🌿 VPD
* 🌞 PPFD
* 🌱 Bodenwerte (Temp, Feuchte, EC)
* 💡 Lichtstatus (AN/AUS)

---


## 🔧 Installation

### Methode 1: HACS (empfohlen)

1. Öffne HACS
2. Gehe zu **Integrationen**
3. Klicke auf **⋮ → Benutzerdefiniertes Repository**
4. Füge https://github.com/Nagliade/marshydro_hacs_homeassistant hinzu
5. Kategorie: `Integration`
6. Installiere **MarsPro MQTT**
7. Starte Home Assistant neu

---

## ⚙️ Einrichtung

Nach dem Neustart:

1. Gehe zu
   **Einstellungen → Geräte & Dienste**
2. Klicke auf **Integration hinzufügen**
3. Suche nach **MarsPro MQTT**

---

## 🔑 Benötigte Daten

### 📍 Device MAC

Deine MAC-Adresse findest du:

* in der MarsPro App Geräte-ID


👉 Beispiel:

```
B63A7588946B
```

---

### 👤 Benutzername

👉 Dein Mars Hydro Login E-Mail

---

### 🔐 Passwort

👉 !!Deine Mars Hydro ID!! Es ist nicht dein Passwort zum Login.

---

## 🚀 Ergebnis

Nach erfolgreicher Einrichtung erscheint dein Gerät in Home Assistant mit:

* allen Sensoren
* Lichtstatus
* Live-Daten

---

## 🧪 Troubleshooting

### ❌ Integration startet nicht

* Home Assistant neu starten
* Logs prüfen

---

### ❌ Keine Daten

* MAC korrekt?
* Login korrekt?

---

### ❌ MQTT Verbindung schlägt fehl

* Internetverbindung prüfen
* Mars Server erreichbar?

---



## 🔥 Roadmap

* [ ] Lichtsteuerung (AN/AUS)
* [ ] Dimmer (Helligkeit)
* [ ] Automationen
* [ ] Energy Dashboard

---

## ⚠️ Disclaimer

Dies ist keine offizielle Integration von MarsPro.

