[Gehe zurück](../README.md)<br/>

<hr>

<h1>CyberTelly Qt - Benutzerhandbuch</h1>

<hr>

<h2>Inhalt:</h2>
<ol>
  <li>Tastenkürzel</li>
  <li>Mausbedienung des Programms</li>
  <li>Tipps zur Einrichtung der TV-Umgebung</li>
  <li>Tipps zur Fehlerbehebung</li>
  <li>Systemvoraussetzungen</li>
  <li>Hinweise für Entwickler</li>
  <li>Copyright und Lizenzierung</li>
</ol>

<h2>Tastenkürzel:</h2>

  | Taste | Aktion |
  |:------|:-------|
  | Strg-P | Programmliste öffnen<br/> Programm streamen mit Doppelklick oder Return |
  | P | Streaming starten |
  | S | Streaming stoppen |
  | Strg-V | Vollbild ein |
  | ESC | Vollbild aus |
  | Strg-T | Toolbar anzeigen/verstecken |
  | Strg-9 | Bildformat 16:9 einstellen |
  | Strg-L | Lautstärke einstellen |
  | Leertaste | Audio aus/ein |
  | Pfeil nach oben | Audio lauter |
  | Pfeil nach unten | Audio leiser |
  | Strg-E | Einstellungen-Dialog öffnen |
  | F1 | Programmhilfe öffnen |
  | Strg-I | Programminfo anzeigen |

<h2>Mausbedienung des Programms:</h2>

  | Was ist zu tun? | Wie macht man es? |
  |:-------|:--------------|
  | Kontextmenü öffnen | Cursorposition im Programmfenster<br/>Rechte Maustaste |
  | Fenster verschieben | Cursorposition im Programmfenster <br/> Linke Maustaste + Drag & Drop |
  | Fenstergröße ändern | Cursorposition Fensterecke rechts unten<br/> Linke Maustaste + Drag & Drop |
  | Vollbild ein-/ausschalten | Cursorposition im Programmfenster<br/> Doppelklick |
  | Lautstärke regeln | Cursorposition im Programmfenster<br/> Mausrad drehen |
  | EPG anzeigen (nur TVHeadend) | Programmliste öffnen<br/> Cursor zu Sender bewegen<br/> Kurze Pause: Tooltip wird angezeigt<br/> Tooltip enthält 4 Einträge |

<h2>Tipps zur Einrichtung der TV-Umgebung:</h2>

<h3>Download fertiger IPTV-M3u-Playlists</h3>
Links zu IPTV-M3u-Listen:<br/>
https://github.com/jnk22/kodinerds-iptv<br/>
https://github.com/iptv-org/iptv (PLAYLISTS.md)<br/>
Speicherort: Ordner <b>CyberTelly/m3u</b> im Linux Homeverzeichnis bzw. C:\Benutzer\[Benutzername]

<h3>Zusammenstellen einer eigenen M3u-Playlist:</h3>
Voraussetzung: Internet-Download Playlists<br/>
Vorgehensweise:<br/>

<ol>
<li>M3u-Playlists im Dateimanager öffnen</li>
<li>VLC-Player öffnen</li>
<li>Menü: Ansicht-Wiedergabeliste</li>
<li>M3u-Dateien nach playlist[00:00] ziehen</li>
<li>Nicht benötigte Sender löschen (Entf)</li>
<li>Gewünschte Sender umsortieren (Drag & Drop)</li>
<li>Rechtsklick: Playlist abspeichern<br/> Speicherort: Ordner <b>CyberTelly/m3u</b> im Linux Homeverzeichnis bzw. C:\Benutzer\[Benutzername]</li>
</ol>

<h3>Fritzbox-Cable - M3u-Liste erzeugen:</h3>
<ol>
<li>VLC-Player öffnen</li>
<li>Menü Ansicht-Wiedergabeliste-Universal Plug & Play<br/> Medienserver werden angezeigt<br/> Doppelklick öffnet Programmliste</li>
<li>Drag & Drop: Sender > Playlist[00:00]</li>
<li>Playlist[00:00]-Fenster öffnen</li>
<li>Drag & Drop: Sender umsortieren</li>
<li>Rechtsklick: Playlist abspeichern<br/> Speicherort: Ordner <b>CyberTelly/m3u</b> im Linux Homeverzeichnis bzw. C:\Benutzer\[Benutzername]</li>
</ol>

<h3>Sat>IP Server - M3u-Liste erzeugen:</h3>
Bei Sat>IP Servern können Sender - ähnlich
wie bei einer FritzBox-Cable - per m3u-Liste
abgespielt werden.<br/>
Fertige M3u-Listen siehe: https://github.com/dersnyke/satipplaylists<br/>
Nach dem Download muss in der Playlist mit 
einem Texteditor 'sat.ip' noch ersetzt werden
durch die IP-Adresse des Sat>IP Servers.<br/>
Beispiel: sat.ip > 192.168.178.230<br/>
Anschließend kann die Liste angepasst und
gespeichert werden wie oben beschieben.<br/>
Das Verfahren wurde mit einem Sat>IP Server
der Firma Megasat erfolgreich getestet.
    
<h3>Infos zum TVHeadend-Server:</h3>
Ein TVHeadend-Server läuft im lokalen Netzwerk und dient als Quelle zum Streamen und Aufnehmen von Live-TV.<br/>
Mögliche Hardware: Raspi 4 mit TV HAT und Raspi OS lite<br/>
Weitere Infos siehe: https://tvheadend.org<br/>

<h4>Zugriff auf TVHeadend-Server:</h4>

|  |  |
|:-----|:-----|
| Url | [Protokoll][Server-IP]:[Port] |
| Protokoll | http:// |
| Server-IP | IPv4-Adresse des Servers |
| Port | 9981 (Voreinstellung TVHeadend) |
| Beispiel | http://192.168.178.235:9981 |

Das Beispiel kann als Vorlage zur Eingabe in den Programm-Einstellungen dienen.

<h4>User-Einstellungen TVHeadend:</h4>
Menüpunkte: Configuration-Users-Access Entries<br/>
Menüpunkte: Configuration-Users-Passwords

<h4>Authentifizierungs-Einstellungen TVHeadend:</h4>

| | |
|:-----|:-----|
| Menüpunkt | Configuration-General-Base<br/> Http Server Settings |
| Authentication type | Plain (insecure) |
| Digest hash type | MD5 |

Hinweis:<br/>
CyberTelly funktioniert nur mit korrekten User- und Authentifizierungs-Einstellungen!

<h3>Info zum EPG:</h3>
EPG funktioniert nicht mit M3u-Playlists.

<h2>Tipps zur Fehlerbehebung:</h2>

<h3>Problem bei Bild und Ton</h3>
Kein Bild / kein Ton bei Streaming-Gerät (z.B. FritzBox) im lokalen Netzwerk.<br/><br/>
Lösung:<br/>
IP-Adresse des Geräts in der Firewall freischalten (eingehend). 
<h3>Problem mit Sender in M3u-Playlist</h3>
Streaming startet nicht und zeigt sofort einen Streamingfehler an.<br/> Mögliche Ursache: Zertifikatsfehler<br/>
Lösung:<br/>
<ul>
<li>Playlist mit Sender im Dateimanager öffnen</li>
<li>VLC-Player öffnen</li>
<li>Menü: Ansicht-Wiedergabeliste</li>
<li>M3u-Playlist nach playlist[00:00] ziehen</li>
<li>Doppelklick auf fehlerhaften Sender</li>
<li>Wenn ein 'Unsichere Seite'-Dialog erscheint:<br/>Button 'Zertifikat anzeigen' anklicken<br/>Button 'Permanent akzeptieren' anklicken<br/>Sender ist ab sofort dauerhaft verfügbar.</li>
</ul>

<h2>Systemvoraussetzungen:</h2>
<h3>Betriebssystem:</h3>
<h4>Windows 10 / 11: getestet, ok</h4>
<h4>Linux x64 (wayland und x11): ok</h4>
Je nach Distributionstyp ist eine bestimmte Version der GNU C Library (glibc) erforderlich:<br/>
<ul>
<li>glibc >= 2.39 für Debian-basierte Distros (Debian, Ubuntu, Mint)</li>
<li>glibc >= 2.39 für RPM-basierte Distros (Fedora, Rocky Linux, AlmaLinux, OpenSuSE)</li>
<li>glibc >= 2.42 für Arch-basierte Distros (Arch, cachyOS, Manjaro)</li>
</ul>
So kann bestimmt werden, welche glibc-Version installiert ist:<br/>
<ol>
<li>Konsolenfenster öffnen</li>
<li>Kommando: <code>ldd --version</code></li>
</ol>
Falls eine zu niedrige glibc-Version ist, kann das Programm installiert, aber nicht gestartet werden.<br/>

Nähere Informationen siehe [Installationsanleitung.txt](https://github.com/rkm-r/CyberTelly/releases)<br/>
<h4>Raspberry Pi OS 64Bit (wayland und x11): ok</h4>
<ul>
<li>Minimum Version 13 (Trixie)</li>
<li>Raspberry Pi 5 empfohlen</li>
</ul>
<h4>MacOS: prinzipiell möglich, aber nicht implementiert</h4>
Mangels entsprechender Hardware konnte CyberTelly auf Macs nicht getestet und bereitgestellt werden.
<h3>VLC-Mediaplayer Version 3</h3>
<h4>Windows: Version >= 3.0.21</h4>
<h4>Linux:   Version >= 3.0.20</h4>
Hinweis für VLC als Linux Snap-/Flathub-App:<br/>
VLC muss aus dem Repository installiert sein. Snap- oder Flathub-Apps laufen in einer Sandbox, die keinen Zugriff auf die VLC-Bibliothek libvlc zulässt.

<h2>Hinweise für Entwickler</h2>
Das Programm wurde entwickelt mit Python sowie python-vlc und PySide6, den Bindings für VLC und das Qt6-Framework. Der Quellcode ist im Ordner source beigefügt. Für eigene Versuche wird empfohlen, ein virtuelles Python Environment zu erzeugen und die erforderlichen Module mithilfe der Datei requirements.txt dort zu installieren.<br/><br/>
Die Bereitstellung des Programms ist nicht Bestandteil dieser Veröffentlichung. In diesem Zusammenhang wird auf folgende Quelle verwiesen: Fitzpatrick Martin, Create GUI Applications with Python & Qt6 (5th Edition, PyQt6), S. 651ff.

<h2>Copyright und Lizensierung:</h2>
Copyright (C) 2025 Rudolf Ringel<br/>
Dieses Programm ist  freie Software und ist
lizensiert  unter den  Bedingungen der  GNU
General Public License 3 (GPLv3).  Die 
Veröffentlichung erfolgt in der Hoffnung, dass
es dem Anwender von Nutzen sein wird,  aber
OHNE  IRGENDEINE  GARANTIE,  sogar ohne die
implizite Garantie der MARKTREIFE oder  der
VERWENDBARKEIT FÜR EINEN BESTIMMTEN ZWECK.<br>
Weitere Informationen dazu siehe: https://www.gnu.org/licenses/
