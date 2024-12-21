Hier ist die README-Datei für GitHub, die beschreibt, wie der Discord-Bot auf einem Server eingerichtet wird und wie er bedient werden kann:

---

# **Discord Squadleader Bot**

Ein Discord-Bot zur Verwaltung von Squadleadern und Squads, inklusive Map-Informationen. Der Bot ist flexibel einsetzbar und lässt sich einfach auf jedem Server einrichten.

---

## **Einladung und Einrichtung**

### **1. Bot einladen**
Lade den Bot mit dem folgenden Link auf deinen Discord-Server ein:

🔗 [Discord-Bot einladen](https://discord.com/oauth2/authorize?client_id=1320093639074119721&permissions=1141760&integration_type=0&scope=bot+applications.commands)

### **2. Benötigte Berechtigungen**
Der Bot benötigt folgende Berechtigungen, um vollständig zu funktionieren:
- `Send Messages`
- `Embed Links`
- `Read Message History`
- `Connect`
- `View Channels`

---

## **Bot-Befehle**

Der Bot wird vollständig über **Slash-Befehle** (`/`) und Textbefehle (`!`) gesteuert.

### **Slash-Befehle**
Diese Befehle dienen der Konfiguration des Bots auf deinem Server:

1. `/set_text_channel`  
   **Beschreibung:** Setze den Textkanal für die Squad-Bot-Befehle.  
   **Beispiel:** `/set_text_channel #general`  

2. `/set_api_domain`  
   **Beschreibung:** Setze die API-Domain, um Map-Informationen abzurufen.  
   **Beispiel:** `/set_api_domain https://rcon.1bv.eu`  

3. `/add_channel`  
   **Beschreibung:** Füge einen Voice-Kanal als Squad-Kanal hinzu.  
   **Beispiel:** `/add_channel Squad I`  

4. `/remove_channel`  
   **Beschreibung:** Entferne einen Voice-Kanal aus den Squad-Kanälen.  
   **Beispiel:** `/remove_channel Squad I`  

5. `/list_channels`  
   **Beschreibung:** Zeige alle registrierten Voice-Kanäle und deren Konfiguration an.  
   **Beispiel:** `/list_channels`  

---

### **Textbefehle**
Der Bot reagiert auf folgende Textbefehle im definierten Textkanal:

1. **`!squadlead`**  
   **Beschreibung:** Startet die Auswahl eines Squadleaders und erstellt Squads.  
   **Ergebnis:** Der Bot wählt automatisch Squadleader für die registrierten Voice-Kanäle aus und teilt die Spieler in Squads auf.

---

## **Funktionsweise**

1. **Squadleader-Auswahl:**  
   - Spieler aus dem registrierten Voice-Kanal werden zufällig als Squadleader ausgewählt.
   - Spieler, die keine Bots sind, werden automatisch in Squads (maximal 6 Mitglieder) aufgeteilt.

2. **Map-Informationen:**  
   - Falls eine API-Domain eingerichtet wurde, zeigt der Bot die aktuelle Map an.

3. **Flexibilität:**  
   - Der Bot kann auf mehreren Servern gleichzeitig verwendet werden. Jede Serverkonfiguration ist unabhängig.

---

## **Beispielausgabe**

### **Discord-Nachricht**
```
Squadleader und Squads

Es wurden 1 Squad(s) erstellt für den Kanal 🎧│Seeding!

**Aktuelle Map**
Omaha Beach

**Squad 1 (Leader: ⭐ [1.BV] Biene)**
⭐ **[1.BV] Biene**

🪖 [1.BV] GermanMeatLoaf  
🪖 [1.BV] bumbumkill  
🪖 [1.BV] Harrald von Holz  
```

---

## **Häufige Probleme**

### **1. Der Bot antwortet nicht auf Befehle**
- Stelle sicher, dass der Textkanal mit `/set_text_channel` festgelegt wurde.
- Überprüfe die Berechtigungen des Bots, insbesondere:
  - `Send Messages`
  - `Embed Links`

### **2. Die Map-Informationen werden nicht angezeigt**
- Prüfe, ob die API-Domain mit `/set_api_domain` korrekt eingerichtet wurde.
- Stelle sicher, dass die API erreichbar ist.

---

## **Mitwirken**

Beiträge und Verbesserungsvorschläge sind willkommen!  
Erstelle einen **Issue** oder reiche einen **Pull Request** ein.

---

Falls du Fragen oder Probleme hast, melde dich gern! 😊
