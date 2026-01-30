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
Strg-Taste entspricht Cmd-Taste bei MacOS

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
Speicherort: Ordner <b>CyberTelly/m3u</b> im Linux Homeverzeichnis bzw. C:\Benutzer\[Benutzername]<br/><br/>
Bitte beachten:<br/>
Downloads von den oben genannten Websites könnten nicht lizensierte Streaming-Quellen enthalten. Für deren Nutzung ist ausschließlich der Anwender dieses Programms verantwortlich.

<h3>Zusammenstellen einer eigenen IPTV-Playlist:</h3>
Voraussetzung: Internet-Download Playlists<br/>
Vorgehensweise:<br/>

<ol>
<li>M3u-Playlist im Dateimanager / Finder suchen</li>
<li>VLC-Player öffnen</li>
<li>Windows/Linux: Menü Ansicht-Wiedergabeliste</li>
<li>Playlist in die Medienbibliothek ziehen</li>
<li>M3u-Dateien in die Wiedergabeliste ziehen</li>
<li>Wiedergabeliste öffnen</li>
<li>Nicht benötigte Sender löschen (Entf)</li>
<li>Gewünschte Sender umsortieren (Drag & Drop)</li>
<li>Windows/Linux: Rechtsklick Playlist abspeichern<br/>MacOS: Menü Ablage - Wiedergabeliste speichern<br/> Speicherort: Ordner <b>CyberTelly/m3u</b> im Linux/MacOS Homeverzeichnis bzw. C:\Benutzer\[Benutzername]</li>
</ol>

<h3>Fritzbox-Cable - M3u-Liste erzeugen:</h3>
<ol>
<li>VLC-Player öffnen</li>
<li>Windows/Linux: Ansicht-Wiedergabeliste</li>
<li>Klick auf Universal Plug & Play<br/> Medienserver werden angezeigt<br/> Doppelklick öffnet Programmliste</li>
<li>Drag & Drop: Sender > Wiedergabeliste</li>
<li>Wiedergabeliste öffnen</li>
<li>Drag & Drop: Sender umsortieren</li>
<li>Windows/Linux: Rechtsklick Playlist abspeichern<br/>MacOS: Ablage - Wiedergabeliste speichern<br/> Speicherort: Ordner <b>CyberTelly/m3u</b> im Linux/MacOS Homeverzeichnis bzw. C:\Benutzer\[Benutzername]</li>
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

Bekannte Probleme sind:<br/>
<ul>
  <li>Firewall blockiert Videostream</li>
  <li>VLC blockert Videostream wegen ungültigem Zertifikat</li>
  <li>Windows 11: VLC stürzt ab wegen Konflikt mit NVIDIA Audiotreiber</li>
  <li>Fedora 43:  VLC stürzt ab wegen Konflikt mit Audiotreiber</li>
  <li>Linux: Gelegentliche Bildfehler bei proprietärem NVIDIA Bildschirmtreiber</li>
</ul>

Detaillierte Anweisungen zur Fehlerbehebung siehe [Troubleshooting.txt](https://github.com/rkm-r/CyberTelly/releases)<br/>

<h2>Systemvoraussetzungen:</h2>
<h3>Betriebssystem:</h3>
<h4>Windows 10 / 11: getestet, ok</h4>
<h4>Linux x64 (wayland und x11): ok</h4>
Um das Programm ausführen zu können benötigen verschiedene Distributionstypen bestimmte Minimalversionen der GNU C Library (glibc):<br/>
<ul>
<li>glibc >= 2.39 für Debian-basierte Distros (Debian, Ubuntu, Mint, ...)</li>
<li>glibc >= 2.39 für RPM-basierte Distros (Fedora, Rocky Linux, AlmaLinux, OpenSuSE, ...)</li>
<li>glibc >= 2.42 für Arch-basierte Distros (Arch, cachyOS, Manjaro, ...)</li>
</ul>
So kann bestimmt werden, welche glibc-Version installiert ist:<br/>
<ol>
<li>Konsolenfenster öffnen</li>
<li>Kommando: <code>ldd --version</code></li>
</ol>
Falls die aktuelle Distribution eine zu niedrige glibc-Version hat, kann das Programm installiert, aber nicht gestartet werden.<br/>

Nähere Informationen siehe [Installationsanleitung.txt](https://github.com/rkm-r/CyberTelly/releases)<br/>
<h4>Raspberry Pi OS 64Bit (wayland und x11): ok</h4>
<ul>
<li>Minimum Version 13 (Trixie)</li>
<li>Beste Performance mit Raspberry Pi 5 und X11</li>
</ul>
<h4>MacOS: ok</h4>
<ul>
<li>Minimum Version 26.2 (Tahoe)</li>
<li>Erforderliche Hardware: Apple Silicon (Intel-Macs werden nicht unterstützt)</li>
</ul>
<h3>VLC-Mediaplayer Version 3</h3>
<h4>Windows: Version >= 3.0.21</h4>
<h4>Linux:   Version >= 3.0.20</h4>
<h4>MacOS:   Version >= 3.0.22</h4>
<h4>Hinweis zu verfügbaren Installationspaketen:</h4>
Alle außer dem Arch-Linux-Installer kommen mit eingebetteter VLC-Bibliothek. Sie benötigen keinen separat installierten VLC-Player und erfüllen diese Systemvoraussetzung 'out of the box'.
<h4>Hinweis für Entwickler und Linux-Arch-Installationen:</h4>
VLC muss aus dem Repository installiert sein. Snap- oder Flathub-Apps laufen in einer Sandbox, die keinen Zugriff auf die VLC-Bibliothek libvlc zulässt.<br/>

<h2>Hinweise für Entwickler</h2>
Der Quellcode des Programms ist im Ordner source beigefügt. Für eigene Versuche wird empfohlen, ein virtuelles Python Environment zu erzeugen und die erforderlichen Module mithilfe der Datei requirements.txt dort zu installieren.<br/><br/>
Die Bereitstellung des Programms ist nicht Bestandteil dieser Veröffentlichung. In diesem Zusammenhang wird auf folgende Quellen verwiesen:
<ul>
<li>Fitzpatrick Martin, Create GUI Applications with Python & Qt6 (5th Edition, PyQt6), S. 651ff.</li>
<li>https://docs.flatpak.org/de/latest/</li>
</ul>
<h2>Copyright und Lizensierung:</h2>
<h4>Copyright (C) 2025, 2026 Rudolf Ringel</h4>
Dieses Programm ist  freie Software und ist
lizensiert  unter den  Bedingungen der  GNU
General Public License 3 (GPLv3).  Die 
Veröffentlichung erfolgt in der Hoffnung, dass
es dem Anwender von Nutzen sein wird,  aber
OHNE  IRGENDEINE  GARANTIE,  sogar ohne die
implizite Garantie der MARKTREIFE oder  der
VERWENDBARKEIT FÜR EINEN BESTIMMTEN ZWECK.<br/>
Weitere Informationen dazu siehe: https://www.gnu.org/licenses/
<h4>Hinweis auf vom Programm genutzte Open Source Libraries:</h4>

| Open Source Library | Lizenz |
|:------|:-------|
| PySide6 (Qt for Python)| LGPLv3.0 |
| libVLC (via python-vlc)| LGPLv2.1+ |
| requests| Apache 2.0 |
| screeninfo| MIT |
| pyobjc-framework-Quartz| MIT |

Alle Bibliotheken wurden ohne Änderungen verwendet wie auf  pypi.org veröffentlicht.<br/>
Weitere Informationen siehe https://pypi.org
