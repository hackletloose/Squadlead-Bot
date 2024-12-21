# **⭐ Discord Squadleader Bot**

[English](#english) | [Deutsch](#deutsch)

---

## **English**

### **⭐ Discord Squadleader Bot**

A Discord bot for managing squad leaders and squads, including map information. The bot is flexible and easy to set up on any server.

---

## **Invitation and Setup**

### **1. Invite the Bot**
Invite the bot to your Discord server using the following link:

🔗 [Invite Discord Bot](https://discord.com/oauth2/authorize?client_id=1320093639074119721&permissions=1141760&integration_type=0&scope=bot+applications.commands)

### **2. Required Permissions**
The bot requires the following permissions to function fully:
- `Send Messages`
- `Embed Links`
- `Read Message History`
- `Connect`
- `View Channels`

---

## **Bot Commands**

The bot is fully controlled via **Slash Commands** (`/`) and text commands (`!`).

### **Slash Commands**
These commands are used to configure the bot on your server:

1. `/set_text_channel`  
   **Description:** Sets the text channel for Squad-Bot commands.  
   **Example:** `/set_text_channel #general`  

2. `/set_api_domain`  
   **Description:** Sets the API domain to retrieve map information.  
   **Example:** `/set_api_domain https://rcon.domain.eu`  

3. `/add_channel`  
   **Description:** Adds a voice channel as a Squad channel.  
   **Example:** `/add_channel Squad I`  

4. `/remove_channel`  
   **Description:** Removes a voice channel from Squad channels.  
   **Example:** `/remove_channel Squad I`  

5. `/list_channels`  
   **Description:** Displays all registered voice channels and their configurations.  
   **Example:** `/list_channels`  

---

### **Text Commands**
The bot responds to the following text commands in the designated text channel:

1. **`!squadlead`**  
   **Description:** Starts the selection of squad leaders and creates squads.  
   **Result:** The bot automatically selects squad leaders for the registered voice channels and divides players into squads.

---

## **Functionality**

1. **Squad Leader Selection:**  
   - Players from the registered voice channel are randomly selected as squad leaders.
   - Players who are not bots are automatically divided into squads (maximum 6 members).

2. **Map Information:**  
   - If an API domain is set up, the bot displays the current map.

3. **Flexibility:**  
   - The bot can be used on multiple servers simultaneously. Each server's configuration is independent.

---

## **Example Output**

### **Discord Message**

```
Squadleader and Squads

1 Squad(s) have been created for the channel 🎧│Seeding!

**Current Map**
Omaha Beach

**Squad 1 (Leader: ⭐ [1.BV] Biene)**
⭐ **[1.BV] Biene**

🪖 [1.BV] GermanMeatLoaf  
🪖 [1.BV] bumbumkill  
🪖 [1.BV] Harrald von Holz  
```

---

## **Common Issues**

### **1. The bot does not respond to commands**
- Ensure that the text channel has been set using `/set_text_channel`.
- Check the bot's permissions, especially:
  - `Send Messages`
  - `Embed Links`

### **2. Map information is not displayed**
- Verify that the API domain has been correctly set using `/set_api_domain`.
- Ensure that the API is reachable.

---

## **Language Switching**

The Discord Squadleader Bot supports both English and German languages. You can switch the bot's language using the following commands:

**English:**
- `/set_language english`  
  **Description:** Sets the bot's language to English.

**Deutsch:**
- `/set_language deutsch`  
  **Beschreibung:** Setzt die Sprache des Bots auf Deutsch.

---

## **Contributing**

Contributions and suggestions for improvements are welcome!  
Create an **Issue** or submit a **Pull Request**.

---

If you have any questions or issues, feel free to reach out! 😊

---

## **Deutsch**

### **⭐ Discord Squadleader Bot**

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
   **Beispiel:** `/set_api_domain https://rcon.domain.eu`  

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

## **Sprachauswahl**

Der Discord Squadleader Bot unterstützt sowohl Englisch als auch Deutsch. Du kannst die Sprache des Bots mit den folgenden Befehlen wechseln:

**English:**
- `/set_language english`  
  **Description:** Sets the bot's language to English.

**Deutsch:**
- `/set_language deutsch`  
  **Beschreibung:** Setzt die Sprache des Bots auf Deutsch.

---

## **Mitwirken**

Beiträge und Verbesserungsvorschläge sind willkommen!  
Erstelle einen **Issue** oder reiche einen **Pull Request** ein.

---

Falls du Fragen oder Probleme hast, melde dich gern! 😊
