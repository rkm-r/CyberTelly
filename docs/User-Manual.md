[Go back](../README-en.md)<br/>

<hr>

<h1>CyberTelly Qt - User Manual</h1>

<hr>

<h2>Content:</h2>
<ol>
  <li>Keyboard Shortcuts</li>
  <li>Mouse Control</li>
  <li>How to set up your TV environment</li>
  <li>Troubleshooting</li>
  <li>System Requirements</li>
  <li>Information for Developers</li>
  <li>Copyright and Licensing</li>
</ol>

<h2>Keyboard Shortcuts:</h2>

  | Key | Action |
  |:------|:-------|
  | Ctrl-P | Open channel list<br/> Double Click or Enter starts streaming selected channel |
  | P | Start streaming |
  | S | Stop streaming |
  | Ctrl-V | Switch to Fullscreen |
  | ESC | Switch back from Fullscreen |
  | Ctrl-T | Show / hide Toolbar |
  | Ctrl-9 | Set Aspect Ratio to 16:9 |
  | Ctrl-L | Set Volume |
  | Space Bar | Audio muted / unmuted |
  | Arrow up | Volume up |
  | Arrow down | Volume down |
  | Ctrl-E | Open Settings Dialog |
  | F1 | Show Help Dialog |
  | Ctrl-I | Show About Dialog |

<h2>Mouse Control:</h2>

  | How to ... | Steps how to do it |
  |:-------|:--------------|
  | open the context menu | Position cursor inside the window<br/>Click right mouse button |
  | move the window | Position cursor inside the window<br/> Left mouse button + Drag & Drop |
  | resize the window | Move cursor to the right bottom corner<br/> Left mouse button + Drag & Drop |
  | turn fullscreen on or off | Position cursor inside the window<br/> Double click left mouse button |
  | adjust volume quickly | Position cursor inside the window<br/> Turn mouse wheel |
  | display EPG (TVHeadend only) | Open channel list<br/> Move cursor to the desired channel<br/> After a short delay tooltip pops up<br/> Tooltip has four entries |

<h2>How to set up your TV environment:</h2>

<h3>Download urls for IPTV m3u playlists:</h3>
https://github.com/jnk22/kodinerds-iptv<br/>
https://github.com/iptv-org/iptv (PLAYLISTS.md)<br/>
Where to save the playlists: Folder <b>CyberTelly/m3u</b> in Linux Home Dir or C:\Users\[user name]

<h3>How to create your own m3u playlist:</h3>
Make sure you have downloaded m3u lists<br/>
How to build your own list:<br/>
<ol>
<li>Open downloaded lists in file manager</li>
<li>Open VLC Player</li>
<li>Menu: View Playlist</li>
<li>Drag m3u lists into playlist window</li>
<li>Delete channels you don't like (Del)</li>
<li>Rearrange channel order (Drag & Drop)</li>
<li>Right click: Save playlist<br/> Where to save it: Folder <b>CyberTelly/m3u</b> in Linux Home Dir or C:\Users\[user name]</li>
</ol>

<h3>Fritzbox-Cable - How to create m3u list:</h3>
<ol>
<li>Open VLC media player</li>
<li>Menu View-Playlist-Universal Plug'n'Play<br/> Media servers show up<br/> Double click opens channel list</li>
<li>Drag & Drop: Channels > Playlist</li>
<li>Open Playlist window</li>
<li>Drag & Drop: Rearrange channels</li>
<li>Right click: Save playlist<br/> Where to save it: Folder <b>CyberTelly/m3u</b> in Linux Home Dir or C:\Users\[user name]</li>
</ol>

<h3>Sat>IP Server - How to create m3u list</h3>
M3u playlists also work with Sat>IP servers,
similar to a FritzBox-Cable. Almost ready
to use m3u playlists can be downloaded from:<br/>
https://github.com/dersnyke/satipplaylists<br/>
After the download open the list with a 
text editor and replace 'sat.ip' with the 
ip address of the server.<br/>
Example: sat.ip > 192.168.178.230<br/>
If you like you can customize and store 
your playlist then as described above.<br/>
This procedure was successfully tested
with a Megasat Sat>IP server.
    
<h3>TVHeadend Server HowTo:</h3>
A TVHeadend server usually runs in the local network and serves as a source for streaming and recording live TV.<br/>
Possible Hardware: Raspi 4 with TV HAT and Raspi OS lite<br/>
For more Information see: https://tvheadend.org<br/>

<h4>How to access the THV-Server:</h4>

|  |  |
|:-----|:-----|
| Url | [Protocol][Server IP]:[Port] |
| Protocol | http:// |
| Server IP | IPv4-Address of TVH server |
| Port | 9981 (TVHeadend default) |
| Example | http://192.168.178.235:9981 |

The example above can be used as a blue print for the input in the settings dialog.

<h4>User Settings TVHeadend:</h4>
Menu item: Configuration-Users-Access Entries<br/>
Menu item: Configuration-Users-Passwords

<h4>Authentication Settings TVHeadend:</h4>

| | |
|:-----|:-----|
| Menu item | Configuration-General-Base<br/> Http Server Settings |
| Authentication type | Plain (insecure) |
| Digest hash type | MD5 |

Please note:<br/>
CyberTelly only works with correct user and authentication settings!

<h3>EPG:</h3>
EPG doesn't work with m3u playlists.

<h2>Troubleshooting:</h2>

<h3>No picture and sound:</h3>
Streaming device (eg. FritzBox) in your local network has no picture and sound.<br/><br/>
Solution:<br/>
Enable inbound IP Address of the device in your firewall configuration
<h3>Problem with channel in m3u playlist:</h3>
Channel doesn't stream video and immediately shows a streaming error indicator.<br/>
Possible reason: Certificate error<br/>
Solution:<br/>
<ul>
<li>Open playlist in file manager </li>
<li>Open VLC Player</li>
<li>Menu item: View Playlist</li>
<li>Drag m3u list into playlist window</li>
<li>Double click faulty channel</li>
<li>If 'Insecure site' dialog shows up:<br/> Click on button 'View certificate'<br/>Click on button 'Accept permanently'<br/>Channel should be permanently available now.</li>
</ul>

<h2>System Requirements:</h2>
<h3>Operating System:</h3>
<h4>Windows 10 / 11: tested, ok</h4>
<h4>Linux x64 (wayland and x11): ok</h4>
Successfully tested with:<br/>
<ul>
<li>Linux Mint 22.2</li>
<li>Debian 13 (Trixie)</li>
<li>Ubuntu 24.04</li>
<li>Ubuntu 25.04</li>
<li>Lubuntu 24.04</li>
</ul>
<h4>Raspberry Pi OS 64Bit (wayland and x11):</h4>
<ul>
<li>Minimum OS version 13 (Trixie)</li>
<li>Raspberry Pi 5 recommended</li>
</ul>
<h4>MacOS: Should be possible, but isn't implemented</h4>
Due to a lack of Apple hardware, CyberTelly could not be tested and deployed.
<h3>VLC Media Player Version 3</h3>
<h4>Windows: Version >= 3.0.21</h4>
<h4>Linux:   Version >= 3.0.20</h4>
Hint for Linux Snap/Flathub installations:<br/>
VLC must be set up from the distibution repository. Snap or Flathub apps are running in a sandbox where the access to the VLC library (libvlc) is blocked.

<h2>Information for Developers</h2>
CyberTelly was developed using Python along with python-vlc and PySide6, the Python bindings for VLC and the Qt6 framework. Everybody who is interested in getting an idea how it works, can have a look at the source code: Set up a virtual Python environment, install the required modules using requirements.txt and start coding!<br/><br/>
The program deployment is not part of this publication. Information on that can be looked up in the following book: Fitzpatrick Martin, Create GUI Applications with Python & Qt6 (5th Edition, PyQt6), p. 651ff.

<h2>Copyright and Licensing:</h2>
Copyright (C) 2025 Rudolf Ringel<br/>
This program is free software.  It is licensed
under  the  terms  of the  GNU  General Public
License 3 (GPLv3).  It is  distributed in  the
hope that it will be  useful, but  WITHOUT ANY
WARRANTY;  without even  the  implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
PURPOSE.<br/>
For more information see: https://www.gnu.org/licenses/
