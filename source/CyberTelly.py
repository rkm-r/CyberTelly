# CyberTelly: Mediaplayer for TVHeadend and M3u Playlists
# Copyright (C) 2025  Rudolf Ringel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.

# Contact: info@cybertelly.tv

# Note on the usage of camel case notation:
# Although snake case is the preferred notation type for Python programs,
# this program uses camel case: PySide6 uses camel case and consistency in
# the notation type was preferred over pythonic habits.

import sys, os, platform, shutil
import subprocess
import json
import time
from datetime import datetime, timedelta
import locale
import screeninfo as scInfo
import requests
from functools import partial
from PySide6 import QtCore, QtGui, QtWidgets
import vlc

# Globally accessible vars and objects
cyberTellyApp = None
progName = 'CyberTelly'
progPath = ''
resourcePath = ''
configPath = ''
sysLanguage = 'de'
scalingFactor = 1.0
errorDic = {'de': {}, 'en': {}}
version = '1.0.0'
build = '250923'
versionInfo = 'CyberTelly' + ' ' + version + ' ' + build
bugManager = None

# Setting for MS Windows to show taskbar icon
try:
    from ctypes import windll
    cyberTellyAppId = 'Ringel.CyberTelly.TVOnly.V01-00'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(cyberTellyAppId)
except ImportError:
    pass

# MS Windows: VLC version is determined by examining registry
try:
    import winreg
except ImportError:
    pass

# Main program window
class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWindowOk = False
        self.videoManager = None
        self.soundManager = None
        self.epgManager = None
        self.actionExit = QtGui.QAction(self)
        self.actionExit.triggered.connect(self.close)

        bugManager.push(bugManager.mainProgram, '__init__: Start')

        # Initialize configuration and help text
        self.configManager = ConfigManager()
        self.helpManager = HelpManager()

        try:
            # Setup MainWindow
            bugManager.push(bugManager.mainProgram, '__init__: Setup MainWindow')
            # self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint))
            self.setGeometry(self.configManager.getGeometry())
            self.move(self.geometry().x(), self.geometry().y())
            self.centralwidget = QtWidgets.QWidget(self)
            self.centralwidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
            self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
            self.verticalLayout.setSpacing(0)
            self.verticalLayout.setContentsMargins(6, 6, 6, 6)
            self.videoFrame = QtWidgets.QWidget(self.centralwidget)
            self.videoFrame.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
            self.videoFrame.setAutoFillBackground(False)
            self.videoFrame.setStyleSheet(u"background-color: rgb(119, 118, 123);")
            self.verticalLayout.addWidget(self.videoFrame)
            self.setCentralWidget(self.centralwidget)
            bugManager.pop(bugManager.mainProgram)

            # Setup actions
            bugManager.push(bugManager.mainProgram, '__init__: Setup Actions')
            windowIcon = QtGui.QIcon()
            windowIcon.addFile(os.path.join(resourcePath,"CyberTelly.png"), QtCore.QSize(), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.setWindowIcon(windowIcon)
            self.setStyleSheet(u"background-color: rgb(235, 235, 235); color: rgb(0,0,0)")

            self.actionExit.triggered.disconnect(self.close)
            self.actionExit.triggered.connect(self.closeWindow)
            exitIcon = QtGui.QIcon()
            exitIcon.addFile(os.path.join(resourcePath,"Close.png"), QtCore.QSize(), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.actionExit.setIcon(exitIcon)

            self.actionAbout = QtGui.QAction(self)
            aboutIcon = QtGui.QIcon()
            aboutIcon.addFile(os.path.join(resourcePath,"Info.png"), QtCore.QSize(), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.actionAbout.setIcon(aboutIcon)

            self.actionSelectChannel = QtGui.QAction(self)
            selectChannelIcon = QtGui.QIcon()
            selectChannelIcon.addFile(os.path.join(resourcePath,"Search.png"), QtCore.QSize(), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.actionSelectChannel.setIcon(selectChannelIcon)

            self.actionPlay = QtGui.QAction(self)
            playIcon = QtGui.QIcon()
            playIcon.addFile(os.path.join(resourcePath,"Play.png"), QtCore.QSize(), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.actionPlay.setIcon(playIcon)
            self.actionPlay.setMenuRole(QtGui.QAction.MenuRole.NoRole)

            self.actionVolumeControl = QtGui.QAction(self)
            volumeControlIcon = QtGui.QIcon()
            volumeControlIcon.addFile(os.path.join(resourcePath,"Speaker.png"), QtCore.QSize(), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.actionVolumeControl.setIcon(volumeControlIcon)
            self.actionVolumeControl.setMenuRole(QtGui.QAction.MenuRole.NoRole)

            self.actionToggleVolumeMuted = QtGui.QAction(self)
            self.actionToggleVolumeMuted.setObjectName(u"actionToggleVolumeMuted")
            self.actionToggleVolumeMuted.setCheckable(True)
            self.actionToggleVolumeMuted.setMenuRole(QtGui.QAction.MenuRole.NoRole)
            
            self.actionToolbarOnOff = QtGui.QAction(self)
            self.actionToolbarOnOff.setObjectName(u"actionToolbarOnOff")
            self.actionToolbarOnOff.setCheckable(True)
            self.actionToolbarOnOff.setMenuRole(QtGui.QAction.MenuRole.NoRole)
            
            self.actionSetAspectRatio16x9 = QtGui.QAction(self)
            self.actionSetAspectRatio16x9.setObjectName(u"actionSetAspectRatio16x9")
            self.actionSetAspectRatio16x9.setMenuRole(QtGui.QAction.MenuRole.NoRole)
            
            self.actionFullscreen = QtGui.QAction(self)
            self.actionFullscreen.setObjectName(u"actionFullscreen")
            self.actionFullscreen.setCheckable(True)
            self.actionFullscreen.setMenuRole(QtGui.QAction.MenuRole.NoRole)
            
            self.actionSettings = QtGui.QAction(self)
            self.actionSettings.setObjectName(u"actionSettings")
            settingsIcon = QtGui.QIcon()
            settingsIcon.addFile(os.path.join(resourcePath,"Settings.png"), QtCore.QSize(), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.actionSettings.setIcon(settingsIcon)
            self.actionSettings.setMenuRole(QtGui.QAction.MenuRole.NoRole)

            self.actionStop = QtGui.QAction(self)
            stopIcon = QtGui.QIcon()
            stopIcon.addFile(os.path.join(resourcePath,"Stop.png"), QtCore.QSize(), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.actionStop.setIcon(stopIcon)
            self.actionStop.setMenuRole(QtGui.QAction.MenuRole.NoRole)

            self.actionMinimize = QtGui.QAction(self)
            self.actionMinimize.setMenuRole(QtGui.QAction.MenuRole.NoRole)

            self.actionResetGeometry = QtGui.QAction(self)
            self.actionResetGeometry.setMenuRole(QtGui.QAction.MenuRole.NoRole)

            self.actionHelp = QtGui.QAction(self)
            helpIcon = QtGui.QIcon()
            helpIcon.addFile(os.path.join(resourcePath,"Help.png"), QtCore.QSize(), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.actionHelp.setIcon(helpIcon)
            self.actionHelp.setMenuRole(QtGui.QAction.MenuRole.NoRole)

            self.actionLanguageGerman = QtGui.QAction(self)
            self.actionLanguageGerman.setCheckable(True)
            self.actionLanguageGerman.setMenuRole(QtGui.QAction.MenuRole.NoRole)

            self.actionLanguageEnglish = QtGui.QAction(self)
            self.actionLanguageEnglish.setCheckable(True)
            self.actionLanguageEnglish.setMenuRole(QtGui.QAction.MenuRole.NoRole)
            bugManager.pop(bugManager.mainProgram)

            # Create keyboard shortcuts
            bugManager.push(bugManager.mainProgram, '__init__: Setup Keyboard Shortcuts')
            self.shortcutSelectChannel = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+P'), self)
            self.shortcutVolumeControl = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+L'), self)
            self.shortcutVolumeUp = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Up), self)
            self.shortcutVolumeDown = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Down), self)
            self.shortcutAudioMuted = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Space), self)
            self.shortcutPlay = QtGui.QShortcut(QtGui.QKeySequence('P'), self)
            self.shortcutStop = QtGui.QShortcut(QtGui.QKeySequence('S'), self)
            self.shortcutFullScreenOn = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+V'), self)
            self.shortcutFullScreenOff = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Escape), self)
            self.shortcutSettings = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+E'), self)
            self.shortcutHelp = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_F1), self)
            self.shortcutAbout = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+I'), self)
            self.shortcutToolbarOnOff = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+T'), self)
            self.shortcutAspectRatio16x9 = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+9'), self)
            bugManager.pop(bugManager.mainProgram)

            # Connect signals and slots
            bugManager.push(bugManager.mainProgram, 'connectSignalsSlots')
            # -- Videomanager: Streaming control 
            self.actionSelectChannel.triggered.connect(self.showChannelList)
            self.shortcutSelectChannel.activated.connect(self.showChannelList)        
            self.actionPlay.triggered.connect(self.play)
            self.shortcutPlay.activated.connect(self.play)
            self.actionStop.triggered.connect(self.stop)
            self.shortcutStop.activated.connect(self.stop)
            # -- Soundmanager: Volume control
            self.actionVolumeControl.triggered.connect(self.setVolume)
            self.shortcutVolumeControl.activated.connect(self.setVolume)        
            self.actionToggleVolumeMuted.triggered.connect(self.toggleVolumeMuted)
            self.shortcutVolumeUp.activated.connect(partial(self.setVolumeUpDown,True))        
            self.shortcutVolumeDown.activated.connect(partial(self.setVolumeUpDown,False))        
            self.shortcutAudioMuted.activated.connect(self.toggleVolumeMuted)
            # -- Dialogs
            self.actionSettings.triggered.connect(self.execConfigDialog)
            self.shortcutSettings.activated.connect(self.execConfigDialog)
            self.actionHelp.triggered.connect(self.showProgHelp)
            self.shortcutHelp.activated.connect(self.showProgHelp)
            self.actionAbout.triggered.connect(self.showProgInfo)
            # -- Window control
            self.shortcutAbout.activated.connect(self.showProgInfo)
            self.actionFullscreen.triggered.connect(self.toggleFullScreen)
            self.shortcutFullScreenOn.activated.connect(partial(self.setFullScreen, True))
            self.shortcutFullScreenOff.activated.connect(partial(self.setFullScreen, False))
            self.actionMinimize.triggered.connect(self.showMinimized)
            self.actionResetGeometry.triggered.connect(self.resetGeometry)
            self.actionToolbarOnOff.triggered.connect(self.toolbarOnOff)
            self.shortcutToolbarOnOff.activated.connect(self.toolbarOnOff)
            self.actionSetAspectRatio16x9.triggered.connect(partial(self.setAspectRatio,16,9))
            self.shortcutAspectRatio16x9.activated.connect(partial(self.setAspectRatio,16,9))
            # -- User language
            self.actionLanguageGerman.triggered.connect(partial(self.setUserLanguage,'de'))
            self.actionLanguageEnglish.triggered.connect(partial(self.setUserLanguage,'en'))
            bugManager.pop(bugManager.mainProgram)

            # toolbar.size().height() only returns valid value if window is visible
            # That's why self.toolbarSize is set up in self.timerSetupVars() 
            self.toolBarHeight = 0

            #  Setup toolbar
            bugManager.push(bugManager.mainProgram, '__init__: Setup toolBar')
            self.toolBar = QtWidgets.QToolBar(self)
            self.toolBar.setStyleSheet(u"background-color: rgb(235, 235, 235);")
            self.toolBar.setMovable(False)
            self.toolBar.setFloatable(False)
            self.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
            self.toolBar.addAction(self.actionSelectChannel)
            self.toolBar.addAction(self.actionStop)
            self.toolBar.addAction(self.actionPlay)
            self.toolBar.addAction(self.actionVolumeControl)
            self.toolBar.addAction(self.actionSettings)
            self.toolBar.addAction(self.actionHelp)
            self.toolBar.addAction(self.actionAbout)
            self.toolBar.addAction(self.actionExit)
            self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint) 
            bugManager.pop(bugManager.mainProgram)

            # Setup context menu
            bugManager.push(bugManager.mainProgram, '__init__: Setup Context Menu')
            self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
            self.context = QtWidgets.QMenu(self)
            self.context.setStyleSheet('background-color: lightgrey; color: black; selection-background-color: darkgrey; selection-color: white;')
            self.viewMenu = self.context.addMenu('Ansicht')
            self.viewMenu.addAction(self.actionFullscreen)
            self.viewMenu.addAction(self.actionMinimize)
            self.viewMenu.addAction(self.actionResetGeometry)
            self.viewMenu.addAction(self.actionToolbarOnOff)
            self.viewMenu.addAction(self.actionSetAspectRatio16x9)
            self.userLanguageMenu = self.context.addMenu('Anwendersprache')
            self.userLanguageMenu.addAction(self.actionLanguageGerman)
            self.userLanguageMenu.addAction(self.actionLanguageEnglish)
            self.context.addAction(self.actionSelectChannel)
            self.context.addAction(self.actionPlay)
            self.context.addAction(self.actionStop)
            self.context.addAction(self.actionVolumeControl)
            self.context.addAction(self.actionToggleVolumeMuted)
            self.context.addAction(self.actionSettings)
            self.context.addAction(self.actionHelp)
            self.context.addAction(self.actionAbout)
            self.context.addAction(self.actionExit)
            self.customContextMenuRequested.connect(self.onContextMenu)
            bugManager.pop(bugManager.mainProgram)

            # Create indicators and indicator pixmaps
            bugManager.push(bugManager.mainProgram, '__init__: Setup Indicators')
            self.lbMuted = QtWidgets.QLabel(parent=self.centralwidget)
            self.lbPageLogo = QtWidgets.QLabel(parent=self.centralwidget)
            self.lbPlayError = QtWidgets.QLabel(parent=self.centralwidget)
            self.lbVlcCursorFix = QtWidgets.QLabel(parent=self.centralwidget)
            self.lbVlcBusy = QtWidgets.QLabel(parent=self.centralwidget)
            # -- Configuration VLC Busy Pixmaps
            self.busyImage1 = QtGui.QPixmap(os.path.join(resourcePath,"Busy1.png"))
            self.busyImage2 = QtGui.QPixmap(os.path.join(resourcePath,"Busy2.png"))
            self.busyImage3 = QtGui.QPixmap(os.path.join(resourcePath,"Busy3.png"))
            self.busyImage4 = QtGui.QPixmap(os.path.join(resourcePath,"Busy4.png"))
            # -- Configuration indicator label lbMuted
            self.lbMuted.setText("")
            self.lbMuted.setPixmap(QtGui.QPixmap(os.path.join(resourcePath,"Mute.png")))
            self.lbMuted.setScaledContents(True)
            self.lbMuted.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.lbMuted.setMouseTracking(True)
            self.lbMuted.hide()
            # -- Configuration label lbPageLogo
            self.lbPageLogo.setText("")
            self.lbPageLogo.setPixmap(QtGui.QPixmap(os.path.join(resourcePath,"PageLogo.png")))
            self.lbPageLogo.setScaledContents(True)
            self.lbPageLogo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.lbPageLogo.setMouseTracking(True)
            self.lbPageLogo.hide()
            # -- Configuration indicator label lbPlayError
            self.lbPlayError.setText("")
            self.lbPlayError.setPixmap(QtGui.QPixmap(os.path.join(resourcePath,"PlayError.png")))
            self.lbPlayError.setScaledContents(True)
            self.lbPlayError.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.lbPlayError.setMouseTracking(True)
            self.lbPlayError.hide()
            # -- Configuration indicator label lbVlcBusy
            self.lbVlcBusy.setText("")
            self.lbVlcBusy.setPixmap(self.busyImage1)
            self.lbVlcBusy.setScaledContents(True)
            self.lbVlcBusy.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.lbVlcBusy.setMouseTracking(True)
            self.lbVlcBusy.hide()
            # -- Create indicatorDic
            self.indicatorDic = {'lbMuted': self.lbMuted, 
                                 'lbPageLogo': self.lbPageLogo, 'pageLogoVisible': True, 
                                 'lbPlayError': self.lbPlayError, 
                                 'lbVlcBusy': self.lbVlcBusy, 'busyImages': [self.busyImage1, self.busyImage2, self.busyImage3, self.busyImage4,]}
            
            # Configuration label lbVlcCursorFix
            # lbVlcCursorFix masks videoFrame at cursor position to avoid cursor Windows issues
            self.lbVlcCursorFix.setGeometry(5,5,1,1)
            # self.lbVlcCursorFix.setGeometry(5,5,10,10) # Debug-Setting
            self.lbVlcCursorFix.setMouseTracking(True)
            self.lbVlcCursorFix.setStyleSheet(u"background-color: rgb(119, 118, 123);")
            # self.lbVlcCursorFix.setStyleSheet(u"background-color: red;") # Debug Setting
            self.lbVlcCursorFix.hide()

            bugManager.pop(bugManager.mainProgram)

            # Setup Objects
            bugManager.push(bugManager.mainProgram, '__init__: Setup Video-, Sound-, EpgManager')
            # -- Create and configure VideoManager 
            self.videoManager = VideoManager(self, configManager=self.configManager, videoFrame=self.videoFrame, indicatorDic=self.indicatorDic)
            # -- Create and configure SoundManager
            self.soundManager = SoundManager(self, mediaPlayer=self.videoManager.mediaPlayer, indicatorDic=self.indicatorDic, volume=self.configManager.getVolume())
            self.videoManager.setSoundManager(self.soundManager)
            # -- Create and configure EPGManager
            self.epgManager = EpgManager(configManager=self.configManager, videoManager=self.videoManager)
            bugManager.pop(bugManager.mainProgram)

            # Settings: mousePressevent, mouseMoveEvent, mouseReleaseEvent
            bugManager.push(bugManager.mainProgram, '__init__: Setup mouseEvent vars')
            # -- Settings for moving the window
            self.moveWindow = False
            self.offset = QtCore.QPoint(0,0)
            self.setMouseTracking(True)
            self.centralwidget.setMouseTracking(True)
            self.videoFrame.setMouseTracking(True)
            # -- Settings for resizing the window
            self.resizeWindow = False
            self.mousePos = QtCore.QPoint(0,0)
            self.resizeRect = self.getResizeRect()
            bugManager.pop(bugManager.mainProgram)

            # Setup timers
            bugManager.push(bugManager.mainProgram, '__init__: Setup Timers and corresponding Vars')
            # -- cursorOffTimer: Make cursor invisible after 3 seconds (fullsceen only)
            self.cursorOffTimer = QtCore.QTimer()
            self.cursorOffInterval = 3000
            self.cursorOffTimer.setInterval(self.cursorOffInterval)
            self.cursorOffTimer.timeout.connect(self.timerCursorOff)
            # -- setIndicatorGeometryTimer: Position indicators at screen center
            self.lastGeometry = QtCore.QRect()
            self.setIndicatorGeometryTimer = QtCore.QTimer()
            self.setIndicatorGeometryTimer.setInterval(100)
            self.setIndicatorGeometryTimer.timeout.connect(self.timerSetIndicatorGeometry)
            # -- fixVlcCursorIssueTimer: Fix for MS Windows VLC cursor issue 
            self.activeDialogs = []
            self.fixVlcCursorIssueTimer = QtCore.QTimer()
            self.fixVlcCursorIssueInterval = 100
            self.fixVlcCursorIssueTimer.setInterval(self.fixVlcCursorIssueInterval)
            self.fixVlcCursorIssueTimer.timeout.connect(self.timerfixVlcCursorIssue)
            # -- setupTimer: Processes configuration step tha have to be done after window becomes visible
            self.setupTimer = QtCore.QTimer()
            self.setupTimer.setInterval(100)
            self.setupTimer.timeout.connect(self.timerSetupVars)
            bugManager.pop(bugManager.mainProgram)

            # Miscellaneous settings
            bugManager.push(bugManager.mainProgram, '__init__: Miscellaneous settings')
            # -- Set User Interface language
            self.setMainWindowLanguage(self.configManager.getLanguage())
            # -- Settings for normal window (toolbarVisible, contentmargins)
            self.normalWindowSettings = self.saveNormalWindowSettings(self.configManager.getToolbarSetting())
            # -- Restore toolbar from configuration
            self.toolBar.setVisible(self.configManager.getToolbarSetting())
            bugManager.pop(bugManager.mainProgram)

            bugManager.pop(bugManager.mainProgram)

            self.mainWindowOk = True
            self.setupTimer.start()
        except:
            try:
                self.toolBar.setVisible(True)
            except:
                pass
            bugManager.setError(bugManager.mainProgram)

    # Set user language in main window
    def setMainWindowLanguage(self, language='de'):
            if not language in ['de','en']:
                language = 'de'
            if language == 'de':
                self.viewMenu.setTitle('Ansicht')
                self.userLanguageMenu.setTitle('Anwendersprache')
                self.actionExit.setText(u"Beenden")
                self.actionExit.setToolTip("Programm beenden")
                self.actionAbout.setText(u"Info")
                self.actionAbout.setToolTip(u"Programminfo")
                self.actionSelectChannel.setText(u"Programm auswählen")
                self.actionSelectChannel.setToolTip(u"Programm auswählen")
                self.actionPlay.setText(u"Streaming starten")
                self.actionPlay.setToolTip(u"Streaming starten")
                self.actionVolumeControl.setText(u"Lautstärke einstellen")
                self.actionVolumeControl.setToolTip(u"Lautstärke einstellen")
                self.actionToggleVolumeMuted.setText(u"Audio aus")
                self.actionToolbarOnOff.setText(u"Toolbar sichtbar")
                self.actionSetAspectRatio16x9.setText(u"Bildformat 16:9")
                self.actionFullscreen.setText(u"Vollbild")
                self.actionSettings.setText(u"Einstellungen")
                self.actionSettings.setToolTip(u"Einstellungen")
                self.actionStop.setText(u"Streaming stoppen")
                self.actionStop.setToolTip(u"Streaming stoppen")
                self.actionMinimize.setText(u"Minimieren")
                self.actionResetGeometry.setText(u"Geometrie zurücksetzen")
                self.actionHelp.setText(u"Hilfe")
                self.actionHelp.setToolTip(u"Programmhilfe")
                self.actionLanguageGerman.setText(u"Deutsch")
                self.actionLanguageEnglish.setText(u"Englisch")
            elif language == 'en':
                self.viewMenu.setTitle('View')
                self.userLanguageMenu.setTitle('User Language')
                self.actionExit.setText(u"Quit")
                self.actionExit.setToolTip("Quit Program")
                self.actionAbout.setText(u"About")
                self.actionAbout.setToolTip(u"About")
                self.actionSelectChannel.setText(u"Select Channel")
                self.actionSelectChannel.setToolTip(u"Select Channel")
                self.actionPlay.setText(u"Start Streaming")
                self.actionPlay.setToolTip(u"Start Streaming")
                self.actionVolumeControl.setText(u"Set Volume")
                self.actionVolumeControl.setToolTip(u"Set Volume")
                self.actionToggleVolumeMuted.setText(u"Audio muted")
                self.actionToolbarOnOff.setText(u"Toolbar visible")
                self.actionSetAspectRatio16x9.setText(u"Aspect Ratio 16:9")
                self.actionFullscreen.setText(u"Fullscreen")
                self.actionSettings.setText(u"Settings")
                self.actionSettings.setToolTip(u"Settings")
                self.actionStop.setText(u"Stop Streaming")
                self.actionStop.setToolTip(u"Stop Streaming")
                self.actionMinimize.setText(u"Minimize")
                self.actionResetGeometry.setText(u"Reset Geometry")
                self.actionHelp.setText(u"Help")
                self.actionHelp.setToolTip(u"Help")
                self.actionLanguageGerman.setText(u"German")
                self.actionLanguageEnglish.setText(u"English")

    # Some vars cannot be set in __init__ of main window.
    # This is done by setupTimer after windows has shown up
    def timerSetupVars(self):
        try:
            bugManager.push(bugManager.setupTimer,'timerSetupVars')
            if self.isVisible():
                self.setupTimer.stop()
                if self.toolBar.isVisible():
                    self.toolBarHeight = self.toolBar.size().height()
                self.setIndicatorGeometry(errorType=bugManager.setupTimer)
                if not self.videoManager.vlcSetupOk:
                    if bugManager != None:
                        bugManager.errorOccurred = True
                    windowTitle = 'Programmfehler'
                    if sysLanguage == 'en':
                        windowTitle = 'Program Error'
                    bugManager.push(bugManager.setupTimer,'infoDialog')
                    infoDialog = InfoDialog(self,caption=windowTitle, infoText=getErrorDescription('vlcError', language=sysLanguage, singleString=False))
                    infoDialog.show()
                    bugManager.pop(bugManager.setupTimer)
                    self.activeDialogs.append(infoDialog)
                    self.fixVlcCursorIssueTimer.start()
            bugManager.pop(bugManager.setupTimer)
        except:
            bugManager.setError(bugManager.setupTimer)

    # Position indicators at center of screen
    def setIndicatorGeometry(self, a=40, errorType=None):
        bugManager.push(errorType, 'setIndicatorGeometry')
        try:
            # setGeometry: lbMuted, lbPlayError
            posX = int(self.geometry().width() / 2 - a / 2)
            posY = int(self.geometry().height() / 2 - self.toolBarHeight / 2 - 43)
            self.lbMuted.setGeometry(QtCore.QRect(posX, posY, a, a))
            self.lbVlcBusy.setGeometry(QtCore.QRect(posX, posY+46,a,a))
            self.lbPlayError.setGeometry(QtCore.QRect(posX, posY+46,a,a))
            # setGeometry: lbPageLogo
            width = max(220,min(443,int(self.geometry().width() * 0.4)))
            height = int(width*235/443)
            if height > self.geometry().height() * 0.5625: # 0.5625 = 9/16
                height = int(self.geometry().height() * 0.5625)
                width = int(height*443/235)
            posX = int(self.geometry().width() / 2 - width / 2)
            posY = int(self.geometry().height() / 2 - self.toolBarHeight / 2 - height / 2)
            self.lbPageLogo.setGeometry(posX, posY, width, height)
            bugManager.pop(errorType)
        except:
            bugManager.setError(errorType)

    # VLC in MS Windows doesn't release cursor control if it is positioned over videoFrame.
    # As a consequence CyberTelly can not change the cursor shape. This results in a never changing wait cursor.
    # Workaround:
    # lbVlcCursorFix is a one pixel sized label at the cursor position. It is moved with the cursor.
    # Thus the cursor is never hovering over the videoFrame and CyberTelly regains control.
    def fixVlcCursorIssue(self, cursorPos=None, errorType=None):
        bugManager.push(errorType, 'fixVlcCursorIssue')
        try:
            if cursorPos == None:
                cursorPos = self.cursor().pos()
            if self.geometry().contains(cursorPos):
                newPos = self.centralwidget.mapFromGlobal(cursorPos)
                if self.videoFrame.geometry().contains(newPos):
                    self.lbVlcCursorFix.show()
                    self.lbVlcCursorFix.move(newPos.x(),newPos.y())
                else:
                    self.lbVlcCursorFix.move(5,5)
                    self.lbVlcCursorFix.hide()
            else:
                self.lbVlcCursorFix.move(5,5)
                self.lbVlcCursorFix.hide()
            bugManager.pop(errorType)
        except:
            bugManager.setError(errorType)

    # Settings that have to be saved when switching to fullscreen
    def saveNormalWindowSettings(self, toolBarVisible):
        settings = {
            'toolbarVisible' : toolBarVisible,
            'contentMargins' : self.centralwidget.layout().contentsMargins(),
        }
        return settings
    
    # Settings that have to be restored when switching back from fullscreen
    def restoreNormalWindowSettings(self):
        bugManager.push(bugManager.mainProgram,'restoreNormalWindowSettings')
        self.toolBar.setVisible(self.normalWindowSettings['toolbarVisible'])
        self.centralwidget.layout().setContentsMargins(self.normalWindowSettings['contentMargins'])
        bugManager.pop(bugManager.mainProgram)

    # Toggle fullscreen / normal screen
    def toggleFullScreen(self):
        if self.mainWindowOk:
            bugManager.push(bugManager.mainProgram,'toggleFullScreen')
            if not self.isFullScreen():
                self.setFullScreen(True)
            else:
                self.setFullScreen(False)
            bugManager.pop(bugManager.mainProgram)

    # Set up fullscreen / normal screen
    def setFullScreen(self, fullScreen):
        if self.mainWindowOk and self.isFullScreen() != fullScreen:
            bugManager.push(bugManager.mainProgram,'setFullScreen')
            try:
                self.lastGeometry = QtCore.QRect(self.geometry())
                if fullScreen:
                    self.configManager.setGeometry(self.geometry())
                    self.configManager.setToolbarsetting(self.toolBar.isVisible())
                    self.actionResetGeometry.setEnabled(False)
                    self.actionToolbarOnOff.setEnabled(False)
                    self.actionSetAspectRatio16x9.setEnabled(False)
                    self.normalWindowSettings['toolbarVisible'] = self.toolBar.isVisible()                
                    self.toolBar.setVisible(False)
                    self.centralwidget.layout().setContentsMargins(0,0,0,0)
                    self.showFullScreen()
                    self.cursorOffTimer.start(self.cursorOffInterval)
                else:
                    self.cursorOffTimer.stop()
                    self.actionResetGeometry.setEnabled(True)
                    self.actionToolbarOnOff.setEnabled(True)
                    self.actionSetAspectRatio16x9.setEnabled(True)
                    self.restoreNormalWindowSettings()
                    self.showNormal()
                self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
                bugManager.pop(bugManager.mainProgram)
                self.setIndicatorGeometryTimer.start()
            except:
                bugManager.setError(bugManager.mainProgram)
    
    # Minimize Window
    def showMinimized(self):
        return super().showMinimized()

    # Restore default window geometry
    def resetGeometry(self):
        if self.mainWindowOk:
            bugManager.push(bugManager.mainProgram,'resetGeometry')
            try:
                self.configManager.config['geometry'] = {
                    'x': 100,
                    'y': 100,
                    'width': 806,
                    'height': 497
                }
                self.showNormal()
                self.setGeometry(100,100,806,497)
                self.restoreNormalWindowSettings()
                self.setAspectRatio(aspectRatioX=16, aspectRatioY=9)
                bugManager.pop(bugManager.mainProgram)
                self.setIndicatorGeometryTimer.start()
            except:
                bugManager.setError(bugManager.mainProgram)

    # Timer that positions indicators at center of screen
    # This is done inside a timer method, because sometimes settings are not processed if window hasn't showed up yet
    def timerSetIndicatorGeometry(self):
        try:
            bugManager.push(bugManager.setIndicatorGeometryTimer,'timerSetIndicatorGeometry')
            if self.lastGeometry != self.geometry():
                self.setIndicatorGeometryTimer.stop()
                self.setIndicatorGeometry(errorType=bugManager.setIndicatorGeometryTimer)
                self.fixVlcCursorIssue(self.cursor().pos(), errorType=bugManager.setIndicatorGeometryTimer)
            bugManager.pop(bugManager.setIndicatorGeometryTimer)
        except:
            bugManager.setError(bugManager.setIndicatorGeometryTimer)
    
    # Switch toolbar on/off
    def toolbarOnOff(self):
        if self.mainWindowOk and not self.isFullScreen():
            try:
                bugManager.push(bugManager.mainProgram,'toolbarOnOff')
                th = self.toolBar.size().height()
                pRect = QtCore.QRect(self.geometry())
                if self.toolBar.isVisible():
                    self.toolBar.setVisible(False)
                    pRect.setHeight(pRect.height() - th)
                    self.toolBarHeight = 0
                    self.normalWindowSettings['toolbarVisible'] = False
                else:
                    self.toolBar.setVisible(True)
                    pRect.setHeight(pRect.height() + th)
                    self.toolBarHeight = self.toolBar.size().height()
                    self.normalWindowSettings['toolbarVisible'] = True
                self.setGeometry(pRect)
                self.resizeRect = self.getResizeRect()
                self.setIndicatorGeometry(errorType=bugManager.mainProgram)
                bugManager.pop(bugManager.mainProgram)
            except:
                bugManager.setError(bugManager.mainProgram)

    # Set aspect ratio of window
    def setAspectRatio(self, aspectRatioX=16, aspectRatioY=9):
        if self.mainWindowOk and not self.isFullScreen():
            bugManager.push(bugManager.mainProgram,'setAspectRatio')
            try:
                gX = self.geometry().x()
                gY = self.geometry().y()
                gW = self.geometry().width()
                mL = self.verticalLayout.contentsMargins().left()
                mR = self.verticalLayout.contentsMargins().right()
                mT = self.verticalLayout.contentsMargins().top()
                mB = self.verticalLayout.contentsMargins().bottom()
                tH = 0
                if self.toolBar.isVisible():
                    tH = self.toolBar.size().height()
                d = float((gW - mL - mR) / aspectRatioX)
                gW = int(d * aspectRatioX + mL + mR)
                gH = int(tH + d * aspectRatioY + mT + mB)
                self.setGeometry(gX,gY,gW,gH)
                self.resizeRect = self.getResizeRect()
                self.setIndicatorGeometry(errorType=bugManager.mainProgram)
                bugManager.pop(errorType=bugManager.mainProgram)
            except:
                bugManager.setError(bugManager.mainProgram)
            
    # Set user languange
    def setUserLanguage(self, usrLanguage='de'):
        if self.mainWindowOk and usrLanguage != self.configManager.getLanguage():
            bugManager.push(bugManager.mainProgram,'setUserlanguage')
            try:
                self.configManager.setLanguage(language=usrLanguage)
                self.setMainWindowLanguage(usrLanguage)
                bugManager.pop(bugManager.mainProgram)
            except:
                bugManager.setError(bugManager.mainProgram)
        
    # If cursor is in resizeRect shape changes to CursorShape.SizeFDiagCursor
    def getResizeRect(self):
        localPos = self.mapFromGlobal(self.pos())
        left = localPos.x() + self.geometry().width() - self.verticalLayout.contentsMargins().right()
        top = localPos.y() + self.geometry().height() - self.verticalLayout.contentsMargins().bottom()
        width = self.verticalLayout.contentsMargins().right()
        height = self.verticalLayout.contentsMargins().bottom()
        resizeRect = QtCore.QRect(left,top,width,height)
        return resizeRect

    # Toggle between fullscreen and normal screen
    def mouseDoubleClickEvent(self, a0):
        if self.mainWindowOk:
            self.toggleFullScreen()
            a0.accept()

    # Left mouse button starts moving or resizing window
    def mousePressEvent(self, e):
        if self.mainWindowOk:
            if not self.isFullScreen():
                if e.button() == QtCore.Qt.MouseButton.LeftButton:
                    if self.resizeRect.contains(e.position().toPoint()):
                        self.resizeWindow = True
                        self.mousePos = e.position().toPoint()
                    else:
                        self.moveWindow = True
                        self.offset = self.mapToGlobal(e.position()).toPoint() - self.pos()
                else:
                    self.moveWindow = False
                    self.resizeWindow = False
            else:
                self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
                self.cursorOffTimer.start(self.cursorOffInterval)
            e.accept()
            # return super().mousePressEvent(e)

    # With left mouse button pressed window is moved or resized
    def mouseMoveEvent(self, e):
        if self.mainWindowOk:
            if not (self.moveWindow or self.resizeWindow):
                self.fixVlcCursorIssue(self.cursor().pos())
            if self.cursor().shape() == QtCore.Qt.CursorShape.BlankCursor:
                self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            if not self.isFullScreen():
                if self.moveWindow:
                    aktPos = self.mapToGlobal(e.position()).toPoint()
                    self.move(aktPos - self.offset)
                    self.setIndicatorGeometry()
                else:
                    if self.resizeWindow:
                        diff = e.position().toPoint() - self.mousePos
                        pX = self.geometry().x()
                        pY = self.geometry().y()
                        newWidth = max(self.width()+diff.x(), 288+12)
                        newHeight = max(self.height()+diff.y(),162+12 + self.toolBarHeight)
                        self.setGeometry(pX, pY, newWidth, newHeight)
                        self.setIndicatorGeometry()
                        self.mousePos = e.position().toPoint()
                    else:
                        if self.resizeRect.contains(e.position().toPoint()):
                            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.SizeFDiagCursor))
                        elif self.cursor().shape() != QtCore.Qt.CursorShape.ArrowCursor:
                            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            else:
                self.cursorOffTimer.start(self.cursorOffInterval)
            e.accept()
            # return super().mouseMoveEvent(e)

    # With left mouse button released moving or resizing window is finished
    def mouseReleaseEvent(self, e):
        if self.mainWindowOk:
            if not self.isFullScreen():
                if self.resizeWindow:
                    self.resizeWindow = False
                    self.mousePos = QtCore.QPoint(0,0)
                    self.resizeRect = self.getResizeRect()
                elif self.moveWindow:
                    self.moveWindow = False
                    self.offset = QtCore.QPoint(0,0)
                self.videoFrame.updateGeometry()
                self.setIndicatorGeometry()
            e.accept()
            # return super().mouseReleaseEvent(e)
    
    # Volume control via mouse wheel
    def wheelEvent(self, event):
        if self.mainWindowOk:
            if self.soundManager != None and self.soundManager.soundManagerOk:
                if event.angleDelta().y() > 0:
                    self.soundManager.vslVolume.setValue(min(100,self.soundManager.volume+1))
                elif event.angleDelta().y() < 0:
                    self.soundManager.vslVolume.setValue(max(0,self.soundManager.volume-1))
                self.setVolume()
                self.soundManager.closeWindowTimer.start()
            event.accept()
        # return super().wheelEvent(event)

    # Show context menu
    def onContextMenu(self, pos):
        if self.mainWindowOk:
            bugManager.push(bugManager.mainProgram,'onContextMenu')
            try:
                self.actionToolbarOnOff.setChecked(self.toolBar.isVisible())
                self.actionToggleVolumeMuted.setChecked(self.soundManager.isMuted())
                self.actionFullscreen.setChecked(self.isFullScreen())
                if self.configManager.getLanguage() == 'de':
                    self.actionLanguageGerman.setChecked(True)
                    self.actionLanguageEnglish.setChecked(False)
                else:
                    self.actionLanguageGerman.setChecked(False)
                    self.actionLanguageEnglish.setChecked(True)
                self.context.exec(self.mapToGlobal(pos))
                self.fixVlcCursorIssue(self.cursor().pos(), errorType=bugManager.mainProgram)
                bugManager.pop(bugManager.mainProgram)
            except:
                bugManager.setError(bugManager.mainProgram)
 
    # Set up and show videoManger channel list popup
    def showChannelList(self):
        if self.mainWindowOk:
            bugManager.push(bugManager.mainProgram,'showChannelList')
            try:
                self.epgManager.waitForTimerAndUpdate(errorType=bugManager.mainProgram)
                chPos = self.mapToGlobal(self.centralwidget.pos())
                ph = self.centralwidget.geometry().height()
                vw = self.videoManager.channelListWidth
                if self.isFullScreen():
                    mL = int(self.centralwidget.size().width()*0.01)
                    mT = int(self.centralwidget.size().height()*0.1)
                    mB = mT
                else:
                    mL = self.verticalLayout.contentsMargins().right()
                    mT = self.verticalLayout.contentsMargins().top()
                    mB = self.verticalLayout.contentsMargins().bottom()
                chPos = QtCore.QPoint(chPos.x()+2*mL, chPos.y()+2*mT)
                ph = ph - 2*mT - 2*mB
                self.videoManager.setGeometry(chPos.x(), chPos.y(), vw, ph)
                bugManager.pop(bugManager.mainProgram)
            except:
                bugManager.setError(bugManager.mainProgram)
            if self.videoManager.videoManagerOk:
                self.videoManager.channelList.setFocus()
                self.videoManager.showlbMessage(isVisible=False, errorType=bugManager.videoManager)
                self.videoManager.show()
                if self.videoManager.channelList.rowCount() == 0:
                    self.videoManager.showlbMessage(errorType=bugManager.videoManager)
                self.fixVlcCursorIssueTimer.start()

    # Set up and show soundManager volume control popup
    def setVolume(self):
        if self.mainWindowOk and self.soundManager != None and self.soundManager.soundManagerOk:
            bugManager.push(bugManager.mainProgram,'setVolume')
            try:
                bugManager.push(bugManager.mainProgram,'setVolume: Stop soundManager timer')
                self.soundManager.closeWindowTimer.stop()
                bugManager.pop(bugManager.mainProgram)

                bugManager.push(bugManager.mainProgram,'setVolume: Set soundManager geometry')
                cwPos = self.mapToGlobal(self.centralwidget.pos())
                if self.isFullScreen():
                    mR = int(self.centralwidget.size().width()*0.01)
                    mT = int(self.centralwidget.size().height()*0.1)
                    mB = mT
                else:
                    mR = self.verticalLayout.contentsMargins().right()
                    mT = self.verticalLayout.contentsMargins().top()
                    mB = self.verticalLayout.contentsMargins().bottom()
                ph = self.centralwidget.geometry().height() - mT*2 - mB*2
                dw = self.soundManager.width()
                chPos = QtCore.QPoint(cwPos.x()+self.centralwidget.geometry().width()-dw-mR*2,cwPos.y()+mT*2)
                self.soundManager.setGeometry(chPos.x(), chPos.y(), dw, ph )
                bugManager.pop(bugManager.mainProgram)

                bugManager.push(bugManager.mainProgram,'setVolume: SetFocus soundManager vslVolume')
                self.soundManager.vslVolume.setFocus()
                bugManager.pop(bugManager.mainProgram)

                bugManager.pop(bugManager.mainProgram)
            except:
                bugManager.setError(bugManager.mainProgram)
            self.soundManager.show()
            self.fixVlcCursorIssueTimer.start()

    # Keyboard control to raise / lower volume
    def setVolumeUpDown(self, volumeUp=True):
        if self.mainWindowOk and self.soundManager != None and self.soundManager.soundManagerOk:
            bugManager.push(bugManager.mainProgram,'setVolumeUpDown')
            bugManager.push(bugManager.mainProgram,'setVolumeUpDown: setValue soundManager vslVolume')
            if volumeUp:
                self.soundManager.vslVolume.setValue(min(100,self.soundManager.volume+1))
            else:
                self.soundManager.vslVolume.setValue(max(0,self.soundManager.volume-1))
            bugManager.pop(bugManager.mainProgram)
            self.setVolume()
            bugManager.pop(bugManager.mainProgram)
            self.soundManager.closeWindowTimer.start()

    # Execute modal settings dialog
    def execConfigDialog(self):
        if self.mainWindowOk:
            configDialog = ConfigDialog(parent=self, configManager=self.configManager)
            result = configDialog.exec()
            if result == 0:
                try:
                    bugManager.push(bugManager.mainProgram,'execConfigDialog')

                    stackPos = bugManager.push(bugManager.configManager,'MainWindow.execConfigDialog')
                    self.configManager.saveConfig(errorType=bugManager.configManager)
                    bugManager.pop(bugManager.configManager, stackPos=stackPos)

                    stackPos = bugManager.push(bugManager.videoManager,'MainWindow.execConfigDialog')        
                    self.videoManager.setupVideoConfig(errorType=bugManager.videoManager)
                    bugManager.pop(bugManager.videoManager,stackPos=stackPos)

                    stackPos = bugManager.push(bugManager.epgManager,'MainWindow.execConfigDialog')        
                    self.epgManager.fetchEpgData(errorType=bugManager.epgManager)
                    bugManager.pop(bugManager.epgManager, stackPos=stackPos)

                    self.fixVlcCursorIssue(self.cursor().pos(),errorType=bugManager.mainProgram)
                    bugManager.pop(bugManager.mainProgram)
                except:
                    bugManager.setError(bugManager.mainProgram)

    # Mute / unmute sound
    def toggleVolumeMuted(self):
        if self.mainWindowOk:
            bugManager.push(bugManager.soundManager,'MainWindow.toggleVolumeMuted')
            self.soundManager.toggleVolumeMuted(errorType=bugManager.soundManager)
            bugManager.pop(bugManager.soundManager)

    # Play selected channel without showing videoManger channelList popup
    def play(self):
        if self.mainWindowOk:
            bugManager.push(bugManager.videoManager,'MainWindow.play')
            self.videoManager.play(item=None, errorType=bugManager.videoManager)
            bugManager.pop(bugManager.videoManager)

    # Timer to switch off cursor after 3 seconds (fullscreen only)
    def timerCursorOff(self):
        try:
            bugManager.push(bugManager.cursorOffTimer,'timerCursorOff')
            activeDialogs = []
            for dlg in self.activeDialogs:
                if dlg.isVisible():
                    activeDialogs.append(dlg)
            self.activeDialogs = activeDialogs
            if not (self.videoManager.isVisible() or self.soundManager.isVisible() or len(self.activeDialogs) > 0):
                self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor))
                self.cursorOffTimer.stop()
            else:
                if self.cursor().shape() == QtCore.Qt.CursorShape.BlankCursor:
                    self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
                self.cursorOffTimer.start(self.cursorOffInterval)
            bugManager.pop(bugManager.cursorOffTimer)
        except:
            bugManager.setError(bugManager.cursorOffTimer)
    
    # Timer to fix VLC cursor issue in MS Windows: see fixVlcCursorIssue
    # There is no way to determine in real time if a dialog window has been closed and
    # repositioning lbVlcCursorFix is necessary, so this is done inside a timer method.
    def timerfixVlcCursorIssue(self):
        try:
            bugManager.push(bugManager.fixVlcCursorIssueTimer,'timerfixVlcCursorIssue')
            activeDialogs = []
            for dlg in self.activeDialogs:
                if dlg.isVisible():
                    activeDialogs.append(dlg)
            self.activeDialogs = activeDialogs
            if not (self.videoManager.isVisible() or self.soundManager.isVisible() or len(self.activeDialogs) > 0):
                self.fixVlcCursorIssueTimer.stop()
                self.fixVlcCursorIssue(self.cursor().pos(), errorType=bugManager.fixVlcCursorIssueTimer)
            bugManager.pop(bugManager.fixVlcCursorIssueTimer)
        except:
            bugManager.setError(bugManager.fixVlcCursorIssueTimer)

    # Stop streaming selected channel
    def stop(self):
        if self.mainWindowOk:
            bugManager.push(bugManager.videoManager,'MainWindow.stop')
            self.videoManager.stop(errorType=bugManager.videoManager)
            bugManager.pop(bugManager.videoManager)

    # Show non modal help dialog
    def showProgHelp(self):
        if self.mainWindowOk:
            if self.configManager.getLanguage() == 'en':
                helpDialog = InfoDialog(self,caption='Help', infoText=self.helpManager.getHelpText(language='en'))
            else:
                helpDialog = InfoDialog(self,caption='Programmhilfe', infoText=self.helpManager.getHelpText(language='de'))
            helpDialog.show()
            self.activeDialogs.append(helpDialog)
            self.fixVlcCursorIssueTimer.start()

    # Show non modal about dialog
    def showProgInfo(self):
        if self.mainWindowOk:
            aboutDialog = AboutDialog(self,language=self.configManager.getLanguage())
            aboutDialog.setWindowTitle(versionInfo)
            aboutDialog.show()
            self.activeDialogs.append(aboutDialog)
            self.fixVlcCursorIssueTimer.start()
    
    # Shut down program
    def closeWindow(self):
        # Save settings
        if self.mainWindowOk:
            if not self.isFullScreen():
                self.configManager.setGeometry(self.geometry())
                self.configManager.setToolbarsetting(self.toolBar.isVisible())
            self.configManager.setVolume(self.soundManager.getVolume())
            bugManager.push(bugManager.configManager,'MainWindow.closeWindow')
            self.configManager.saveConfig(errorType=bugManager.configManager)
            bugManager.pop(bugManager.configManager)
        # Show error message if bugManager has errors
        if bugManager.errorOccurred:
            dlg = QtWidgets.QMessageBox()
            dlg.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
            dlg.setWindowTitle(" ")
            dlg.setText(bugManager.errorMessage)
            dlg.move(self.pos().x()+50, self.pos().y()+50)
            dlg.exec()
        self.close()

# Class Configuration manager
class ConfigManager():
    def __init__(self):
        self.configManagerOk = False
        self.configUpdated = False
        try:
            bugManager.push(bugManager.configManager,'__init__: Started')

            # Setup paths
            bugManager.push(bugManager.configManager,'__init__: Setup paths')
            self.progPath = progPath
            self.configPath = configPath
            self.m3uPath = os.path.join(self.configPath, 'm3u')
            bugManager.pop(bugManager.configManager)

            # Read config data from config.json
            self.config = self.readConfig()
            # Init configuration paths and data at first startup or if config is not found
            if not os.path.exists(self.configPath):
                bugManager.push(bugManager.configManager,'__init__: Create new config data')
                os.makedirs(self.configPath)
                if not os.path.isfile(os.path.join(self.configPath,'config.json')):
                    shutil.copy2(os.path.join(progPath,'config.json'), self.configPath)
                    if sysLanguage != self.getLanguage():
                        self.setLanguage(sysLanguage)
                bugManager.pop(bugManager.configManager)
            
            # Init m3u path with m3u sample files at first startup or if path is corrupted
            if not os.path.exists(self.m3uPath):
                bugManager.push(bugManager.configManager,'__init__: Create new m3u data')
                os.makedirs(self.m3uPath)
                m3uSrcPath = os.path.join(self.progPath, 'm3u')
                if os.path.exists(m3uSrcPath):
                    files = os.listdir(m3uSrcPath)
                    for fname in files:
                        shutil.copy2(os.path.join(m3uSrcPath,fname), self.m3uPath)
                bugManager.pop(bugManager.configManager)

            self.configManagerOk = True
            bugManager.pop(bugManager.configManager)
        except:
            bugManager.setError(bugManager.configManager)
    
    # Init program configuration
    def initConfig(self):
        config = {}
        config['language'] = sysLanguage
        config['source'] = 'm3u'
        config['geometry'] = {
            'x': 100,
            'y': 100,
            'width': 806,
            'height': 497
        }
        config['toolBarVisible'] = True
        config['volume'] = 50
        config['tvhServer'] = {
            'url': 'http://192.168.178.201:9981', 
            'username': 'user', 
            'password': 'passw0rd'
        }
        config['m3uFile'] = 'IPTV-de-plus.m3u'
        return config
    
    # Read configuration from config.json with fallback initConfig
    def readConfig(self, errorType=None):
        config = {}
        if errorType == None:
            errorType= bugManager.configManager
        try:
            bugManager.push(errorType,'readConfig')
            configFile = os.path.join(self.configPath,'config.json')
            if os.path.isfile(configFile):
                f = open(configFile, 'r')
                config = json.load(f)
                f.close()
            else:
                config = self.initConfig()
            bugManager.pop(errorType)
        except:
            config = self.initConfig()
            bugManager.setError(errorType)
        return config
    
    # Save configuration to config.json
    def saveConfig(self, errorType=None):
        if errorType == None:
            errorType = bugManager.configManager
        bugManager.push(errorType,'saveConfig')
        try:
            if self.configManagerOk:
                configFile = os.path.join(self.configPath,'config.json')
                f = open(configFile,'w')
                json.dump(self.config, f, indent=2)
                f.close()
                bugManager.pop(errorType)
            else:
                raise
        except:
            bugManager.setError(errorType)
    
    # Update configuration data: Used in configDialog
    def updateConfig(self, newConfig, errorType=None):
        if errorType == None:
            errorType = bugManager.configManager
        bugManager.push(errorType,'updateConfig')
        try:
            if len(newConfig) > 0:
                if self.config['language'] != newConfig['language']:
                    self.config['language'] = newConfig['language']
                    self.configUpdated = True
                if self.config['source'] != newConfig['source']:
                    self.config['source'] = newConfig['source']
                    self.configUpdated = True
                if self.config['tvhServer']['url'] != newConfig['tvhServer']['url']:
                    self.config['tvhServer']['url'] = newConfig['tvhServer']['url']
                    self.configUpdated = True
                if self.config['tvhServer']['username'] != newConfig['tvhServer']['username']:
                    self.config['tvhServer']['username'] = newConfig['tvhServer']['username']
                    self.configUpdated = True
                if self.config['tvhServer']['password'] != newConfig['tvhServer']['password']:
                    self.config['tvhServer']['password'] = newConfig['tvhServer']['password']
                    self.configUpdated = True
                if self.config['m3uFile'] != newConfig['m3uFile']:
                    self.config['m3uFile'] = newConfig['m3uFile']
                    self.configUpdated = True
            bugManager.pop(errorType)
        except:
            bugManager.setError(errorType)
    
    # Determine if config has changed
    def configChanged(self):
        configChanged = self.configUpdated
        self.configUpdated = False
        return configChanged

    # Write language setting to configuration
    def setLanguage(self, language='de'):
        if 'language' in self.config.keys():
            if self.config['language'] != language:
                if language in ['de', 'en']:
                    self.config['language'] = language
                else:
                    self.config['language'] = 'de'
                self.configUpdated = True
        else:
            self.config['language'] = 'de'
            self.configUpdated = True
    
    # Get language from configuration
    def getLanguage(self):
        language = 'de'
        try:
            if self.config['language'] in ['de','en']:
                language = self.config['language']
            else:
                raise
        except:
            language = 'de'
            self.config['language'] = 'de'
            bugManager.push(bugManager.configManager, 'Info: getLanguage Exception caught', setNotification=True)
        return language
    
    # Get streaming source ['tvh', 'm3u']
    def getSource(self):
        source = 'm3u'
        try:
            if self.config['source'] in ['tvh','m3u']:
                source = self.config['source']
            else:
                raise
        except:
            source = 'm3u'
            self.config['source'] = 'm3u'
            bugManager.push(bugManager.configManager, 'Info: getSource Exception caught', setNotification=True)
        return source
    
    # Write geometry setting to configuration
    def setGeometry(self, geometry):
        try:
            geometryDic = {
                'x': geometry.x(),
                'y': geometry.y(),
                'width': geometry.width(),
                'height': geometry.height()
            }
            self.config['geometry'] = geometryDic
        except:
            bugManager.push(bugManager.configManager, 'Info: setGeometry Exception caught', setNotification=True)

    # Get geometry from configuration
    def getGeometry(self):
        geometry = None
        try:
            geometry = QtCore.QRect(self.config['geometry']['x'],
                                    self.config['geometry']['y'],
                                    self.config['geometry']['width'],
                                    self.config['geometry']['height'])
            # Check if Program Window is within screen bounds
            # and reset geometry if necessary.
            isOnScreen = False
            if cyberTellyApp != None:
                screens = cyberTellyApp.screens()
                for screen in screens:
                    if screen.geometry().contains(geometry):
                        isOnScreen = True
                        break
            if not isOnScreen:
                raise
        except:
            bugManager.push(bugManager.configManager, 'Info: getGeometry Exception caught', setNotification=True)
            geometry = QtCore.QRect(100,100,806,497)
            self.config['geometry'] = {
                'x': 100,
                'y': 100,
                'width': 806,
                'height': 497
            }
        return geometry
    
    # Write toolbar setting to configuration
    def setToolbarsetting(self, isVisible):
        try:
            if not isVisible in [True,False]:
                raise
            self.config['toolBarVisible'] = isVisible
        except:
            bugManager.push(bugManager.configManager,'Info: setToolbarSetting Exception caught', setNotification=True)

    # Get toolbar setting from configuration
    def getToolbarSetting(self):
        isVisible = True
        try:
            isVisible =  self.config['toolBarVisible']
        except:
            isVisible = True
            self.config['toolBarVisible'] = True
            bugManager.push(bugManager.configManager, 'Info: getToolbarSetting Exception caught', setNotification=True)
        return isVisible
    
    # Write volume setting to configuration
    def setVolume(self, volume):
        try:
            if not isinstance(volume, int):
                raise
            self.config['volume'] = volume
        except:
            bugManager.push(bugManager.configManager, 'Info: setVolume Exception caught', setNotification=True)

    # Get volume setting from configuration
    def getVolume(self):
        volume = 50
        try:
            volume = self.config['volume']
        except:
            volume = 50
            self.config['volume'] = 50
            bugManager.push(bugManager.configManager, 'Info: getVolume Exception caught', setNotification=True)
        return volume
    
    # Get TVHeadend settings from configuration
    def getTvhServer(self):
        server = {}
        error = False
        try:
            server['url'] = self.config['tvhServer']['url']
        except:
            server['url'] = ''
            error = True
        try:
            server['username'] = self.config['tvhServer']['username']
        except:
            server['username'] = ''
            error = True
        try:
            server['password'] = self.config['tvhServer']['password']
        except:
            server['password'] = ''
            error = True
        if error:
            self.config['tvhServer'] = server
            bugManager.push(bugManager.configManager, 'getTvhServer Exception caught', setNotification=True)
        return server
    
    # Get m3u path from configuration
    def getM3uPath(self):
        m3uPath = ''
        try:
            if os.path.isdir(self.m3uPath):
                m3uPath = self.m3uPath
            else:
                raise
        except:
            m3uPath = ''
            bugManager.push(bugManager.configManager,'getM3uPath (Exception caught)', setNotification=True)
        return m3uPath

    # Get m3u file path from configuration with fallback to first file in m3uFiles
    def getM3uFilePath(self):
        m3uFilePath = ''
        try:
            m3uFilePath = os.path.join(self.m3uPath,self.config['m3uFile'])
            if not os.path.isfile(m3uFilePath):
                m3uFiles = []
                for root, dirs, files in os.walk(self.m3uPath):
                    for name in files:
                        if name.lower().endswith('.m3u') or name.lower().endswith('.m3u8'):
                            m3uFiles.append(name)
                m3uFile = sorted(m3uFiles, key=str.lower)[0]
                m3uFilePath = os.path.join(self.m3uPath,m3uFile)
                if os.path.isfile(m3uFilePath):
                    self.config['m3uFile'] = m3uFile
                    self.configUpdated = True
                else:
                    raise
        except:
            m3uFilePath = ''
            self.config['m3uFile'] = ''
            bugManager.push(bugManager.configManager,'getM3uFilePath (Exception caught)', setNotification=True)
        return m3uFilePath

# Class ConfigDialog
class ConfigDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, configManager=None):
        super().__init__(parent)
        self.configDialogOk = False
        self.configManager = configManager
        bugManager.push(bugManager.configDialog,'__init__: Started')
        try:
            self.language = self.configManager.getLanguage()
            self.setupGui()
            self.setupForm()
            self.setDialogLanguage(language=self.language)
            self.pbOK.clicked.connect(self.exitDialog)
            self.pbCancel.clicked.connect(self.cancelDialog)
            self.configDialogOk = True
            bugManager.pop(bugManager.configDialog)
        except:
            bugManager.setError(bugManager.configDialog)

    # Exec configDialog if __init__ was successful
    def exec(self):
        if self.configDialogOk:
            return super().exec()
        else:
            self.done(2)

    # Setup Gui
    def setupGui(self):
        bugManager.push(bugManager.configDialog,'setupGui')

        # Basic window settings
        bugManager.push(bugManager.configDialog,'setupGui: Window settings')
        self.setWindowFlags(QtCore.Qt.WindowType.Dialog | QtCore.Qt.WindowType.WindowTitleHint | QtCore.Qt.WindowType.CustomizeWindowHint)
        self.resize(360, 387)
        self.setModal(True)
        self.verticalLayout0 = QtWidgets.QVBoxLayout(self)
        bugManager.pop(bugManager.configDialog)

        # QGroupBox: gbStreamingSource
        bugManager.push(bugManager.configDialog,'setupGui: GroupBox gbStreamingSource + vSpacer')
        self.gbStreamingSource = QtWidgets.QGroupBox(self)
        self.verticalLayout1 = QtWidgets.QVBoxLayout(self.gbStreamingSource)
        self.rbSourceTvh = QtWidgets.QRadioButton(self.gbStreamingSource)
        self.verticalLayout1.addWidget(self.rbSourceTvh)
        self.rbSourceM3u = QtWidgets.QRadioButton(self.gbStreamingSource)
        self.verticalLayout1.addWidget(self.rbSourceM3u)
        self.verticalLayout0.addWidget(self.gbStreamingSource)
        self.vSpacer1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout0.addItem(self.vSpacer1)
        bugManager.pop(bugManager.configDialog)

        # QGroupBox: gbTvhServer
        bugManager.push(bugManager.configDialog,'setupGui: GroupBox gbTvhServer + vSpacer')
        self.gbTvhServer = QtWidgets.QGroupBox(self)
        self.verticalLayout2 = QtWidgets.QVBoxLayout(self.gbTvhServer)
        
        # -- Row 1: QLabel / QLineEdit: lbServerUrl / leServerUrl
        bugManager.push(bugManager.configDialog,'setupGui: GroupBox gbTvhServer Row 1')
        self.lbServerUrl = QtWidgets.QLabel(self.gbTvhServer)
        self.lbServerUrl.setAlignment(QtGui.Qt.AlignmentFlag.AlignLeading|QtGui.Qt.AlignmentFlag.AlignLeft|QtGui.Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout2.addWidget(self.lbServerUrl)
        self.leServerUrl = QtWidgets.QLineEdit(self.gbTvhServer)
        self.leServerUrl.setStyleSheet(u"background-color: rgb(255, 255, 255); color: black; font: 700 11pt \"Courier New\";")
        self.verticalLayout2.addWidget(self.leServerUrl)
        bugManager.pop(bugManager.configDialog)
        
        # -- Row 2: two columns layout for lbUsername / leUserName + lbPassword / lePassword
        bugManager.push(bugManager.configDialog,'setupGui: GroupBox gbTvhServer Row 2')
        self.horizontalLayout1 = QtWidgets.QHBoxLayout()
        # -- -- QLabel / QLineEdit: lbUsername / leUserName
        self.verticalLayout3 = QtWidgets.QVBoxLayout()
        self.lbUserName = QtWidgets.QLabel(self.gbTvhServer)
        self.lbUserName.setAlignment(QtGui.Qt.AlignmentFlag.AlignLeading|QtGui.Qt.AlignmentFlag.AlignLeft|QtGui.Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout3.addWidget(self.lbUserName)
        self.leUserName = QtWidgets.QLineEdit(self.gbTvhServer)
        self.leUserName.setStyleSheet(u"background-color: rgb(255, 255, 255); color: black; font: 700 11pt \"Courier New\";")
        self.verticalLayout3.addWidget(self.leUserName)
        self.horizontalLayout1.addLayout(self.verticalLayout3)
        # -- -- QLabel / QLineEdit: lbPassword / lePassword
        self.verticalLayout4 = QtWidgets.QVBoxLayout()
        self.lbPassword = QtWidgets.QLabel(self.gbTvhServer)
        self.lbPassword.setAlignment(QtGui.Qt.AlignmentFlag.AlignLeading|QtGui.Qt.AlignmentFlag.AlignLeft|QtGui.Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout4.addWidget(self.lbPassword)
        self.lePassword = QtWidgets.QLineEdit(self.gbTvhServer)
        self.lePassword.setStyleSheet(u"background-color: rgb(255, 255, 255); color: black; font: 700 11pt \"Courier New\";")
        self.verticalLayout4.addWidget(self.lePassword)
        self.horizontalLayout1.addLayout(self.verticalLayout4)
        self.verticalLayout2.addLayout(self.horizontalLayout1)
        bugManager.pop(bugManager.configDialog)
        self.verticalLayout0.addWidget(self.gbTvhServer)

        self.vSpacer2 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout0.addItem(self.vSpacer2)
        bugManager.pop(bugManager.configDialog)

        # QGroupBox: gbVlcPlayList
        bugManager.push(bugManager.configDialog,'setupGui: GroupBox gbVlcPlayList')
        self.gbVlcPlayList = QtWidgets.QGroupBox(self)
        self.verticalLayout5 = QtWidgets.QVBoxLayout(self.gbVlcPlayList)
        self.cbVlcPLaylist = QtWidgets.QComboBox(self.gbVlcPlayList)
        self.cbVlcPLaylist.setStyleSheet(u"background-color: rgb(255, 255, 255); selection-background-color: rgb(255, 255, 127); selection-color: rgb(0, 85, 255); font: 700 11pt \"Courier New\";")
        self.cbVlcPLaylist.setMaxVisibleItems(5)
        self.cbVlcPLaylist.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        self.verticalLayout5.addWidget(self.cbVlcPLaylist)
        self.verticalLayout0.addWidget(self.gbVlcPlayList)

        self.vSpacer3 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout0.addItem(self.vSpacer3)
        bugManager.pop(bugManager.configDialog)

        # QPushButtons: Cancel, OK
        bugManager.push(bugManager.configDialog,'setupGui: Buttons')
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.hSpacer2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout2.addItem(self.hSpacer2)
        self.pbCancel = QtWidgets.QPushButton(self)
        self.horizontalLayout2.addWidget(self.pbCancel)
        self.hSpacer1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout2.addItem(self.hSpacer1)
        self.pbOK = QtWidgets.QPushButton(self)
        self.horizontalLayout2.addWidget(self.pbOK)
        self.hSpacer3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout2.addItem(self.hSpacer3)
        self.verticalLayout0.addLayout(self.horizontalLayout2)
        bugManager.pop(bugManager.configDialog)

        bugManager.pop(bugManager.configDialog)

    # Set up data in dialog form
    def setupForm(self):
        bugManager.push(bugManager.configDialog,'setupForm')
        if self.configManager.getSource() == 'tvh':
            self.rbSourceTvh.setChecked(True)
        else:
            self.rbSourceM3u.setChecked(True)
        server = self.configManager.getTvhServer()
        self.leServerUrl.setText(server['url'])
        self.leUserName.setText(server['username'])
        self.lePassword.setText(server['password'])
        m3uFiles = []
        for root, dirs, files in os.walk(self.configManager.getM3uPath()):
            for name in files:
                if name.lower().endswith('.m3u') or name.lower().endswith('.m3u8'):
                  m3uFiles.append(name)
        m3uFiles = sorted(m3uFiles, key=str.lower)
        selectedPos = 0
        for index, m3uFile in enumerate(m3uFiles):
            self.cbVlcPLaylist.addItem(m3uFile)
            if self.configManager.getM3uFilePath().endswith(m3uFile):
                selectedPos = index
        self.cbVlcPLaylist.setCurrentIndex(selectedPos)
        bugManager.pop(bugManager.configDialog)

    # Initialize language settings in dialog form
    def setDialogLanguage(self, language='de'):
            if language == 'de':
                self.setWindowTitle(u"Einstellungen")
                self.gbStreamingSource.setTitle(u"Streaming-Quelle")
                self.rbSourceTvh.setText(u"TVHeadend-Server")
                self.rbSourceM3u.setText(u"M3U-Playlist (Sat>IP, IPTV, ..)")
                self.gbTvhServer.setTitle(u"TVHeadend-Server")
                self.lbServerUrl.setToolTip(u"Beispiel: http://192.168.178.201:9981")
                self.lbServerUrl.setText(u"Server-URL:")
                self.lbUserName.setText(u"Benutzername:")
                self.lbPassword.setText(u"Passwort:")
                self.gbVlcPlayList.setTitle(u"VLC-Wiedergabeliste")
                self.pbCancel.setText(u"Abbruch")
                self.pbOK.setText(u"OK")
            elif language == 'en':
                self.setWindowTitle(u"Settings")
                self.gbStreamingSource.setTitle(u"Streaming Source")
                self.rbSourceTvh.setText(u"TVHeadend Server")
                self.rbSourceM3u.setText(u"M3U Playlist (Sat>IP, IPTV, ..)")
                self.gbTvhServer.setTitle(u"TVHeadend Server")
                self.lbServerUrl.setToolTip(u"Example: http://192.168.178.201:9981")
                self.lbServerUrl.setText(u"Server URL:")
                self.lbUserName.setText(u"User Name:")
                self.lbPassword.setText(u"Password:")
                self.gbVlcPlayList.setTitle(u"VLC PlayList")
                self.pbCancel.setText(u"Cancel")
                self.pbOK.setText(u"OK")

    # Set up user feedback if errors in TVHServer settings are detected
    def showTvhStatus(self, language='de', serverOk=False, usrPwOk=False):
        if serverOk and usrPwOk:
            self.gbTvhServer.setTitle(u"TVHeadend-Server")
        else:
            if language == 'de':
                self.gbTvhServer.setTitle(u"TVHeadend-Server: Konfigurationsfehler")
            else:
                self.gbTvhServer.setTitle(u"TVHeadend-Server: Configuration Error")
        if serverOk:
            self.lbServerUrl.setStyleSheet(u"")
        else:
            self.lbServerUrl.setStyleSheet(u"background-color: rgb(252, 192, 192); color: rgb(165, 29, 45);")
        if usrPwOk:
            self.lbUserName.setStyleSheet(u"")
            self.lbPassword.setStyleSheet(u"")
        else:
            self.lbUserName.setStyleSheet(u"background-color: rgb(252, 192, 192); color: rgb(165, 29, 45);")
            self.lbPassword.setStyleSheet(u"background-color: rgb(252, 192, 192); color: rgb(165, 29, 45);")

    # Build new configuration and return it to calling method
    def getDataFromForm(self):
        config = {}
        bugManager.push(bugManager.configDialog,'getDataFromForm')
        try:
            config['language'] = self.configManager.getLanguage()
            if self.rbSourceTvh.isChecked():
                config['source'] = 'tvh'
            else:
                config['source'] = 'm3u'
            config['tvhServer'] = {
                'url': self.leServerUrl.text(),
                'username': self.leUserName.text(), 
                'password': self.lePassword.text()
            }
            config['m3uFile'] = self.cbVlcPLaylist.itemText(self.cbVlcPLaylist.currentIndex())
            bugManager.pop(bugManager.configDialog)
        except:
            config = {}
            bugManager.setError(bugManager.configDialog)
        return config
    
    # Detect errors in user input for THVServer data
    def tvhServerOk(self, url='', user='', password=''):
        serverOk = False
        usrPwOk = True
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WaitCursor))
        try:
            base_url = url
            api_url = f'{base_url}/api/channel/grid?limit=10000'
            usrPw = (user, password)
            response = requests.get(api_url, auth=usrPw, timeout=2)
            serverOk = True
            if response.status_code in [401, 403]: # 401=Unauthorized, 403=Forbidden
                usrPwOk = False
        except:
            serverOk = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        return serverOk, usrPwOk
    
    # Exit dialog or cancel in case of thv errors
    def exitDialog(self):
        bugManager.push(bugManager.configDialog, 'ConfigDialog.exitDialog')
        self.showTvhStatus(language=self.language, serverOk=True, usrPwOk=True)
        newConfig = self.getDataFromForm()
        serverOk = True
        usrPwOk = True
        # Skip cancellation if THVServer is not selected as source
        if newConfig['source'] == 'tvh':
            tvhServer = newConfig['tvhServer']
            serverOk, usrPwOk = self.tvhServerOk(url=tvhServer['url'],user=tvhServer['username'],password=tvhServer['password'])
        if serverOk and usrPwOk:
            self.configManager.updateConfig(newConfig, errorType=bugManager.configDialog)
            bugManager.pop(bugManager.configDialog)
            self.done(0)
        else:
            self.showTvhStatus(language=self.language, serverOk=serverOk, usrPwOk=usrPwOk)
            bugManager.pop(bugManager.configDialog)
    
    # Cancel dialog inputs and exit dialog
    def cancelDialog(self):
        self.done(1)

# Class VideoManager
class VideoManager(QtWidgets.QDialog):
    def __init__(self, parent=None, configManager=None, videoFrame=None, indicatorDic=None):
        super().__init__(parent)
        # Basic settiings
        self.videoManagerOk = False
        self.configManager = configManager
        self.soundManager = None
        self.vlcSetupOk = False
        self.vlcInstance = None
        self.mediaPlayer = None
        self.indicatorDic = indicatorDic
        self.lbPageLogo = None
        self.lbVlcBusy = None
        self.vlcBusyImages = []
        self.lbPlayError = None
        self.lbMuted = None
        if self.indicatorDic != None:
            self.lbPageLogo = indicatorDic['lbPageLogo']
            self.lbPlayError = indicatorDic['lbPlayError']
            self.lbVlcBusy = indicatorDic['lbVlcBusy']
            self.vlcBusyImages = indicatorDic['busyImages']
            self.lbMuted = indicatorDic['lbMuted']
        self.videoFrame = videoFrame
        try:
            stackPos = bugManager.push(bugManager.videoManager,'__init__: Started')
            # Init VLC Player
            try:
                self.vlcInstance = vlc.Instance()
                self.mediaPlayer = self.vlcInstance.media_player_new()
                self.vlcSetupOk = True
            except:
                self.vlcInstance = None
                self.mediaPlayer = None
                self.vlcSetupOk = False
                bugManager.push(bugManager.videoManager,'__init__: VLC-Error (Exception caught)', setError=True)
            if self.vlcSetupOk:
                # Disable VLC video and mouse input: X11 / Win32 only! Not implemented in Mac OS.
                try:
                    if sys.platform != "darwin":
                        self.mediaPlayer.video_set_mouse_input(False)
                        self.mediaPlayer.video_set_key_input(False)
                except:
                    bugManager.push(bugManager.videoManager,'__init__: Error disabling mouse/keyboard input (Exception caught)', setNotification=True)
                # Set up videoFrame to display VLC streams
                try:            
                    winID=self.videoFrame.winId().__int__()
                    if sys.platform.startswith('linux'):
                        if winID is not None:
                            self.mediaPlayer.set_xwindow(winID)
                    elif sys.platform == "win32":
                        self.mediaPlayer.set_hwnd(winID)
                    elif sys.platform == "darwin":
                        self.mediaPlayer.set_nsobject(winID)
                except:
                    bugManager.push(bugManager.videoManager,'__init__: Error setting VLC videoframe (Exception caught)', setError=True)
            
            # Setup GUI
            bugManager.push(bugManager.videoManager,'__init__: Setup Gui')
            self.setWindowFlags(QtCore.Qt.WindowType.Popup)
            self.resize(285, 300)
            font = QtGui.QFont()
            font.setFamilies([u"Arial"])
            font.setPointSize(9)
            self.setFont(font)
            self.verticalLayout = QtWidgets.QVBoxLayout(self)
            self.verticalLayout.setSpacing(3)
            self.verticalLayout.setContentsMargins(3, 3, 3, 3)
            self.channelList = QtWidgets.QTableWidget(self)
            self.channelList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.channelList.setAutoScroll(True)
            self.channelList.setColumnCount(2)
            self.channelList.horizontalHeader().setVisible(False)
            self.channelList.verticalHeader().setVisible(False)
            self.channelList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
            self.channelList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
            self.channelList.setSortingEnabled(False)
            self.channelList.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
            self.channelList.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.channelList.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.verticalLayout.addWidget(self.channelList)
            self.channelListMaxWidth = 300
            self.channelListWidth = self.channelListMaxWidth
            bugManager.pop(bugManager.videoManager)
            bugManager.push(bugManager.videoManager,'__init__: Setup Objects')
            # Init TV-Channels
            self.tvChannels = []
            self.aktChannelName = ''
            # Init Message Label
            self.lbMessage = QtWidgets.QLabel(parent=self)
            self.setuplbMessage(bugManager.videoManager)
            # Init Status Timer and Vars
            self.isPlaying = False
            self.volume = 50
            self.volumeTimeout = 50 # 50 * 200ms = 10s
            self.volumeTimeoutCnt = 0
            self.busyCnt = 0
            self.playerStatus = vlc.State.Stopped
            self.statusTimer = QtCore.QTimer()
            self.statusTimer.setInterval(200)
            self.statusTimer.timeout.connect(self.timerGetStatus)
            self.lbPageLogo.show()
            self.lbPageLogo.raise_()
            bugManager.pop(bugManager.videoManager)

            bugManager.push(bugManager.videoManager,'__init__: Connect Signal-SLot')
            # self.channelList.itemDoubleClicked.connect(self.play) # Triggers itemActivated as well > work around: mouseDoubleClickEvent
            self.channelList.itemActivated.connect(self.play)       # Return key triggers itemActivated
            bugManager.pop(bugManager.videoManager)

            # Setup Video config
            self.videoManagerOk = self.setupVideoConfig(errorType=bugManager.videoManager)

            bugManager.pop(bugManager.videoManager, stackPos=stackPos)
        except:
            bugManager.setError(bugManager.videoManager)

    # Play video on mouseDoubleClickEvent
    def mouseDoubleClickEvent(self, event):
        self.play()
        event.accept()
    
    # Set soundManager
    def setSoundManager(self, soundManager=None):
        self.soundManager = soundManager
        if self.soundManager != None and self.soundManager.soundManagerOk:
            self.volume = self.soundManager.getVolume()

    # Set up message label: channel list empty
    def setuplbMessage(self, errorType=1):
        bugManager.push(errorType, 'setuplbMessage')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbMessage.sizePolicy().hasHeightForWidth())
        self.lbMessage.setSizePolicy(sizePolicy)
        self.lbMessage.setMinimumSize(QtCore.QSize(160, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbMessage.setFont(font)
        self.lbMessage.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.lbMessage.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.lbMessage.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbMessage.setWordWrap(True)
        self.lbMessage.setObjectName("lbMessage")
        if self.configManager.getLanguage() == 'de':
            self.lbMessage.setText("Programmliste leer")
        else:
            self.lbMessage.setText("Channel list empty")
        self.lbMessage.hide()
        bugManager.pop(errorType)

    # Set up video configuration
    def setupVideoConfig(self, errorType=1):
        videoConfigOk = False
        stackPos1 = bugManager.push(errorType, 'setupVideoConfig')
        try:
            # Basic setings
            bugManager.push(errorType, 'setupVideoConfig: Init Vars')
            self.source = self.configManager.getSource()
            self.tvhServer = self.configManager.getTvhServer()
            self.m3uFilePath = self.configManager.getM3uFilePath()
            bugManager.pop(errorType)

            # Read tvChannels
            stackPos2 = bugManager.push(errorType, 'setupVideoConfig: Read tvChannels')
            if self.source == 'tvh':
                self.tvChannels = self.fetchThvChannels(errorType=errorType)
            else:
                self.tvChannels = self.fetchM3uChannels(errorType=errorType)
            bugManager.pop(errorType, stackPos=stackPos2)

            # Initialize QTableWidget channelList
            bugManager.push(errorType, 'setupVideoConfig: Setup QTableWidget')
            fm = QtGui.QFontMetrics(self.font())
            chWidth = 200
            while self.channelList.rowCount() > 0:
                self.channelList.removeRow(0)
            for channel in self.tvChannels:
                row = self.channelList.rowCount()
                self.channelList.insertRow(row)
                chNumber = QtWidgets.QTableWidgetItem()
                chNumber.setText(' ' + str(row+1) + ' ')
                chNumber.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
                self.channelList.setItem(row, 0, chNumber)
                nameItem = QtWidgets.QTableWidgetItem(channel['name'])
                nameItem.setText(' ' + channel['name'])
                nameItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
                self.channelList.setItem(row, 1, nameItem)
                chWidth = max(chWidth, int(fm.boundingRect(''.zfill(len('0000000000' + channel['name']))).width()))
            if self.channelList.rowCount() > 0:
                self.channelList.selectRow(0)
                try:
                    self.channelList.verticalScrollBar().setValue(0)
                    self.channelList.horizontalScrollBar().setValue(0)
                except:
                    pass
            self.channelListWidth = min(self.channelListMaxWidth,chWidth)
            bugManager.pop(errorType)
            
            bugManager.pop(errorType, stackPos=stackPos1)
            videoConfigOk = True
        except:
            videoConfigOk = False
            self.tvChannels = []
            while self.channelList.rowCount() > 0:
                self.channelList.removeRow(0)
            bugManager.setError(errorType)
        return videoConfigOk

    # Show message if channel ist is empty
    def showlbMessage(self, isVisible=True, errorType=1):
        if self.videoManagerOk:
            bugManager.push(errorType,'showlbMessage')
            try:
                if isVisible:
                    posX = int((self.geometry().width()- self.lbMessage.size().width()) / 2)
                    posY = int((self.geometry().height()- self.lbMessage.size().height()) / 2)
                    width = self.lbMessage.size().width()
                    height = self.lbMessage.size().height()
                    self.lbMessage.setGeometry(posX,posY,width,height)
                    self.lbMessage.show()
                else:
                    self.lbMessage.hide()
                bugManager.pop(errorType)
            except:
                bugManager.setError(errorType)

    # Fetch tv channels from THVServer
    def fetchThvChannels(self, errorType=1):
        channels = []
        try:
            base_url = self.tvhServer['url']
            api_url = f'{base_url}/api/channel/grid?limit=10000'
            usrPw = (self.tvhServer.get('username', ''), self.tvhServer.get('password', ''))
            response = requests.get(api_url, auth=usrPw, timeout=2)
            channels = sorted(response.json()['entries'], key=lambda channel: channel['number'])
        except:
            channels = []
            bugManager.push(errorType,'fetchTvhChannels: Exception caught', setNotification=True)
        return channels
    
    # Fetch tv channels from m3u playlist
    def fetchM3uChannels(self, errorType=1):
        channels = []
        try:
            lines = []
            for enc in ['utf-8', 'cp1252']: # cp1252 = ANSI
                try:
                    f = open(self.m3uFilePath,'r', encoding=enc)
                    lines = f.readlines()
                    f.close()
                    break
                except:
                    lines = []
            channel = {}
            for line in lines:
                line = line.strip()
                if line.startswith("#EXTINF:"):
                    channel = {}
                    infos = str(line[len("#EXTINF:"):]).split(',')
                    if len(infos) > 1:
                        channel['name'] = infos[1].strip()
                if len(channel) == 1 and not line.startswith("#"):
                    channel["url"] = line
                    channels.append(channel)
                    channel = {}
        except:
            channels = []
            bugManager.push(errorType,'fetchM3uChannels: Exception caught', setNotification=True)
        return channels
    
    # Stop streaming channel
    def stop(self, errorType=1):
        if self.videoManagerOk:
            bugManager.push(errorType,'stop')
            try:
                if self.vlcSetupOk:
                    self.statusTimer.stop()
                    waitTime = 3 # 3 = Timeout 1,5s
                    while self.statusTimer.isActive() and waitTime > 0:
                        time.sleep(0.5)
                        waitTime -= 1
                    self.mediaPlayer.stop()
                    self.playerStatus = vlc.State.Stopped
                self.isPlaying = False
                self.indicatorDic['pageLogoVisible'] = True
                if self.lbMuted.isVisible():
                    self.lbPageLogo.hide()
                else:
                    self.lbPageLogo.show()
                    self.lbPageLogo.raise_()
                self.lbVlcBusy.hide()
                self.lbPlayError.hide()
                self.videoFrame.update()
                bugManager.pop(errorType)
            except:
                bugManager.setError(bugManager.videoManager)

    # Start streaming selected channel
    def play(self, item=None, errorType=None):
        if self.videoManagerOk:
            if errorType == None:
                errorType = bugManager.videoManager
            bugManager.push(errorType,'play')
            try:
                if item == None and self.channelList.rowCount() > 0 and len(self.channelList.selectedItems()) > 0:
                    item = self.channelList.selectedItems()[0]
                if item != None:
                    # Wait for statusTimer
                    bugManager.push(errorType,'play: Wait for statusTimer')
                    self.statusTimer.stop()
                    waitTime = 3 # 3 = Timeout 1,5s
                    while self.statusTimer.isActive() and waitTime > 0:
                        time.sleep(0.5)
                        waitTime -= 1
                    bugManager.pop(errorType)
                    # Get url
                    bugManager.push(errorType,'play: Get url')
                    url = ''
                    self.aktChannelName = ''
                    if self.source == 'tvh':
                        url, self.aktChannelName = self.getUrlTvh(item, errorType=bugManager.videoManager)
                    elif self.source == 'm3u':
                        url, self.aktChannelName = self.getUrlM3u(item, errorType=bugManager.videoManager)
                    bugManager.pop(errorType)
                    # Start streaming
                    bugManager.push(errorType,'play: Start streaming')
                    if url != '' and self.vlcSetupOk:
                        self.indicatorDic['pageLogoVisible'] = False
                        self.lbPageLogo.hide()
                        self.lbPlayError.hide()
                        if self.playerStatus == vlc.State.Playing:
                            self.mediaPlayer.stop()
                            self.playerStatus = vlc.State.Stopped
                            self.videoFrame.update()
                        media = self.vlcInstance.media_new(url)
                        self.mediaPlayer.set_media(media)
                        self.mediaPlayer.play()
                        if self.soundManager != None and self.soundManager.soundManagerOk:
                            self.volume = self.soundManager.getVolume()
                            if self.soundManager.isMuted():
                                self.volume = 0
                        self.volumeTimeoutCnt = 0
                        self.busyCnt = 0
                        self.lbVlcBusy.setPixmap(self.vlcBusyImages[0])
                        self.statusTimer.start()
                    bugManager.pop(errorType)
                bugManager.pop(errorType)
            except:
                bugManager.setError(errorType)

    # Get streaming url from TVHServer
    def getUrlTvh(self, item, errorType=1):
        url = ''
        name = ''
        bugManager.push(errorType,'getUrlTvh')
        if self.videoManagerOk:
            try:
                ch = item.row()
                usr = self.tvhServer.get('username', '')
                pw  = self.tvhServer.get('password', '')
                svrUrl = self.tvhServer['url']
                protocol = svrUrl[:svrUrl.rfind('/')+1]
                ipPort = svrUrl[svrUrl.rfind('/')+1:]
                chUuid = self.tvChannels[ch]['uuid']
                url = protocol + usr +':' + pw + '@' + ipPort + '/stream/channel/' + chUuid
                name = self.tvChannels[ch]['name']
                bugManager.pop(bugManager.videoManager)
            except:
                url = ''
                name = ''
                bugManager.setError(errorType)
        return url, name

    # Get streaming url from m3u playlist
    def getUrlM3u(self, item, errorType=1):
        url = ''
        name = ''
        bugManager.push(errorType, 'getUrlM3u')
        if self.videoManagerOk:
            try:
                url = self.tvChannels[item.row()]['url']
                name = self.tvChannels[item.row()]['name']
                bugManager.pop(errorType)
            except:
                url = ''
                name = ''
                bugManager.setError(errorType)
        return url, name
    
    # Timer method to handle VLC status return codes
    def timerGetStatus(self):
        if self.videoManagerOk:
            try:
                bugManager.push(bugManager.statusTimer,'timerGetStatus')
                if self.vlcSetupOk:
                    # Increment counter for timer intervals and show busy indicator after one second
                    if self.busyCnt == 4:
                        self.lbVlcBusy.show()
                        self.lbVlcBusy.raise_()
                    self.lbVlcBusy.setPixmap(self.vlcBusyImages[self.busyCnt % 4])
                    self.busyCnt += 1
                    # Get actual player status
                    self.playerStatus = self.mediaPlayer.get_state()
                    self.isPlaying = self.playerStatus == vlc.State.Playing
                    # Show error indicator in case of error or irregularly ended streaming
                    if self.playerStatus in [vlc.State.Ended, vlc.State.Error]:
                        if self.configManager.getLanguage() == 'de':
                          self.lbPlayError.setToolTip('Streamingfehler: ' + self.aktChannelName)
                        else:
                          self.lbPlayError.setToolTip('Streaming error: ' + self.aktChannelName)
                        self.lbPlayError.show()
                        self.lbPlayError.raise_()
                    # Clean up in case of success
                    if self.playerStatus in [vlc.State.Playing, vlc.State.Paused, vlc.State.Ended, vlc.State.Error, vlc.State.Stopped]:
                        # Check if VLC sound is ready and skip cleaning up if it is not: Timeout 10s
                        vlcSoundReady = False
                        if self.playerStatus == vlc.State.Playing:
                            self.mediaPlayer.audio_set_volume(self.volume*2)
                            vlcSoundReady = self.mediaPlayer.audio_get_volume() != -1
                            self.volumeTimeoutCnt += 1
                        else:
                            vlcSoundReady = True
                        # Hide busy label and challel window if videostream is playing
                        if vlcSoundReady or self.volumeTimeoutCnt >= self.volumeTimeout:
                            self.lbVlcBusy.hide()
                            self.statusTimer.stop()
                            self.hide()
                else:
                    self.lbVlcBusy.hide()
                    self.statusTimer.stop()
                bugManager.pop(bugManager.statusTimer)
            except:
                bugManager.setError(bugManager.statusTimer)
        else:
            self.statusTimer.stop()

# Class SoundManager
class SoundManager(QtWidgets.QDialog):
    def __init__(self, parent=None, mediaPlayer=None, indicatorDic=None, volume=50):
        super().__init__(parent)
        # Basic settings
        self.soundManagerOk = False
        self.mediaPlayer = mediaPlayer
        try:
            bugManager.push(bugManager.soundManager,'__init__: Started')

            # Set up indicators and vars
            bugManager.push(bugManager.soundManager,'__init__: Indicators and vars')
            self.indicatorDic = indicatorDic
            self.lbMuted = None
            self.lbPageLogo = None
            if self.indicatorDic != None:
                self.lbMuted = self.indicatorDic['lbMuted']
                self.lbPageLogo = self.indicatorDic['lbPageLogo']
            self.volume = volume
            self.muted = self.volume == 0
            if self.muted:
                self.lbMuted.show()
                self.lbMuted.raise_()
            bugManager.pop(bugManager.soundManager)

            # Set up Gui
            bugManager.push(bugManager.soundManager,'__init__: Setup Gui')

            # Basic settings
            self.setWindowFlags(QtCore.Qt.WindowType.Popup)
            self.resize(69, 217)
            self.setMouseTracking(True)
            self.verticalLayout = QtWidgets.QVBoxLayout(self)

            # Set up QSlider vslVolume
            bugManager.push(bugManager.soundManager,'__init__: Setup QSlider vslVolume')
            self.horizontalLayout1 = QtWidgets.QHBoxLayout()
            self.hSpacer11 = QtWidgets.QSpacerItem(13, 128, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
            self.horizontalLayout1.addItem(self.hSpacer11)
            self.vslVolume = QtWidgets.QSlider(self)
            self.vslVolume.setMaximum(100)
            self.vslVolume.setValue(0)
            self.vslVolume.setOrientation(QtCore.Qt.Orientation.Vertical)
            self.vslVolume.setPageStep(1)
            self.vslVolume.setSingleStep(1)
            self.vslVolume.setMouseTracking(True)
            self.vslVolume.setMinimum(0)
            self.vslVolume.setMaximum(100)
            self.vslVolume.setValue(self.volume)
            self.horizontalLayout1.addWidget(self.vslVolume)
            self.hSpacer12 = QtWidgets.QSpacerItem(13, 128, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
            self.horizontalLayout1.addItem(self.hSpacer12)
            self.verticalLayout.addLayout(self.horizontalLayout1)
            bugManager.pop(bugManager.soundManager)
            
            # Set up QLabel lbVolume
            bugManager.push(bugManager.soundManager,'__init__: Setup QLabel lbVolume')
            self.horizontalLayout2 = QtWidgets.QHBoxLayout()
            self.hSpacer21 = QtWidgets.QSpacerItem(13, 17, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
            self.horizontalLayout2.addItem(self.hSpacer21)
            self.lbVolume = QtWidgets.QLabel(self)
            self.lbVolume.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.lbVolume.setMouseTracking(True)
            self.lbVolume.setText(str(self.volume).zfill(3)+'%')
            self.horizontalLayout2.addWidget(self.lbVolume)
            self.hSpacer22 = QtWidgets.QSpacerItem(13, 17, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
            self.horizontalLayout2.addItem(self.hSpacer22)
            self.verticalLayout.addLayout(self.horizontalLayout2)
            bugManager.pop(bugManager.soundManager)
            
            # Set up icons speakerIcon, muteIcon
            bugManager.push(bugManager.soundManager,'__init__: Icons')
            self.speakerIcon = QtGui.QIcon()
            self.speakerIcon.addPixmap(QtGui.QPixmap(os.path.join(resourcePath,"Speaker.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.muteIcon = QtGui.QIcon()
            self.muteIcon.addPixmap(QtGui.QPixmap(os.path.join(resourcePath,"Mute.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            bugManager.pop(bugManager.soundManager)

            # Set up QPushButton pbMute
            bugManager.push(bugManager.soundManager,'__init__: Setup QPushButton pbMute')
            self.horizontalLayout3 = QtWidgets.QHBoxLayout()
            self.hSpacer31 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
            self.horizontalLayout3.addItem(self.hSpacer31)
            self.pbMute = QtWidgets.QPushButton(self)
            self.pbMute.setMinimumSize(QtCore.QSize(30, 30))
            self.pbMute.setMaximumSize(QtCore.QSize(30, 30))
            self.pbMute.setMouseTracking(True)
            self.pbMute.setIcon(self.speakerIcon)
            self.pbMute.setIconSize(QtCore.QSize(24, 24))
            self.horizontalLayout3.addWidget(self.pbMute)
            self.hSpacer32 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
            self.horizontalLayout3.addItem(self.hSpacer32)
            self.verticalLayout.addLayout(self.horizontalLayout3)
            bugManager.pop(bugManager.soundManager)

            bugManager.pop(bugManager.soundManager)

            # Init mediaplayer volume
            bugManager.push(bugManager.soundManager,'__init__: Init mediaplayer volume')
            if self.mediaPlayer != None:
                self.mediaPlayer.audio_set_volume(self.volume*2)
            bugManager.pop(bugManager.soundManager)

            # Connect Signals and Slots
            bugManager.push(bugManager.soundManager,'__init__: Set slots')
            self.vslVolume.valueChanged.connect(self.setVolume)
            self.pbMute.clicked.connect(partial(self.toggleVolumeMuted,errorType=None))
            self.shortcutAudioMuted = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Space), self)
            self.shortcutVolumeUp = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Up), self)
            self.shortcutVolumeDown = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Down), self)
            self.shortcutAudioMuted.activated.connect(partial(self.toggleVolumeMuted,errorType=None))
            self.shortcutVolumeUp.activated.connect(partial(self.volumeKeyAction,volumeUp=True))        
            self.shortcutVolumeDown.activated.connect(partial(self.volumeKeyAction,volumeUp=False))        
            bugManager.pop(bugManager.soundManager)

            # Init Timer
            bugManager.push(bugManager.soundManager,'__init__: Init timer')
            self.closeWindowTimer = QtCore.QTimer()
            self.closeWindowTimerInterval = 3000
            self.closeWindowTimer.setInterval(self.closeWindowTimerInterval)
            self.closeWindowTimer.timeout.connect(self.timerCloseWindow)
            bugManager.pop(bugManager.soundManager)

            self.soundManagerOk = True
            bugManager.pop(bugManager.soundManager)
        except:
            bugManager.setError(bugManager.soundManager)

    # Control volume via mouse wheel
    def wheelEvent(self, event):
        if self.soundManagerOk:
            volume = self.volume
            if event.angleDelta().y() > 0:
                volume = min(100,volume+1)
            elif event.angleDelta().y() < 0:
                volume = max(0,volume-1)
            self.vslVolume.setValue(volume)
            event.accept()
    
    # Control Volume via key shortcut
    def volumeKeyAction(self, volumeUp=True):
        if self.soundManagerOk:
            volume = self.volume
            if volumeUp > 0:
                volume = min(100,volume+1)
            else:
                volume = max(0,volume-1)
            self.vslVolume.setValue(volume)

    # Get volume
    def getVolume(self):
        volume = 50
        try:
            volume = self.volume
        except:
            volume = 50
        return volume

    # Read if sound is muted
    def isMuted(self):
        muted = False
        try:
            muted = self.muted
        except:
            muted = False
        return muted

    # Set volume
    def setVolume(self, volume):
        if self.mediaPlayer != None and self.soundManagerOk:
            errorType = bugManager.soundManager
            bugManager.push(errorType,'setVolume')
            try:
                # Restart close window timer if active
                bugManager.push(errorType,'setVolume: Restart timer')
                if self.closeWindowTimer.isActive():
                    self.closeWindowTimer.start(self.closeWindowTimerInterval)
                bugManager.pop(errorType)

                # Show muted indicator if muted else show page logo
                bugManager.push(errorType,'setVolume: Set icon and text')
                if volume != 0:
                    self.pbMute.setIcon(self.speakerIcon)
                    if self.indicatorDic['pageLogoVisible']:
                        self.lbPageLogo.show()
                    self.muted = False
                    self.lbMuted.hide()
                else:
                    self.pbMute.setIcon(self.muteIcon)
                    if self.indicatorDic['pageLogoVisible']:
                        self.lbPageLogo.hide()
                    self.muted = True
                    self.lbMuted.show()
                    self.lbMuted.raise_()
                self.lbVolume.setText(str(volume).zfill(3)+'%')
                bugManager.pop(errorType)

                # VLC: set volume
                bugManager.push(errorType,'setVolume: Set volume')
                self.volume = volume
                self.mediaPlayer.audio_set_volume(volume*2)
                bugManager.pop(errorType)

                bugManager.pop(errorType)
            except:
                bugManager.setError(errorType)

    # Mute / unmute sound
    def toggleVolumeMuted(self, errorType=None):
        if self.mediaPlayer != None and self.soundManagerOk:
            if errorType == None:
                errorType = bugManager.soundManager
            bugManager.push(errorType,'toggleVolumeMuted')
            try:
                # Restart close window timer if active
                bugManager.push(errorType,'toggleVolumeMuted: Restart timer')
                if self.closeWindowTimer.isActive():
                    self.closeWindowTimer.start(self.closeWindowTimerInterval)
                bugManager.pop(errorType)

                # Show muted indicator if muted else show page logo
                bugManager.push(errorType,'toggleVolumeMuted: Set icon and text')
                if self.muted and self.volume > 0:
                    self.pbMute.setIcon(self.speakerIcon)
                    if self.indicatorDic['pageLogoVisible']:
                        self.lbPageLogo.show()
                    self.muted = False
                    self.lbMuted.hide()
                else:
                    self.pbMute.setIcon(self.muteIcon)
                    if self.indicatorDic['pageLogoVisible']:
                        self.lbPageLogo.hide()
                    self.muted = True
                    self.lbMuted.show()
                    self.lbMuted.raise_()
                volume = self.volume
                if self.muted:
                    volume = 0
                self.lbVolume.setText(str(volume).zfill(3)+'%')
                bugManager.pop(errorType)

                # VLC: set volume
                bugManager.push(errorType,'toggleVolumeMuted: Set volume')
                self.vslVolume.valueChanged.disconnect(self.setVolume)
                self.vslVolume.setValue(volume)
                self.vslVolume.valueChanged.connect(self.setVolume)
                self.mediaPlayer.audio_set_volume(volume*2)
                bugManager.pop(errorType)

                bugManager.pop(errorType)
            except:
                bugManager.setError(errorType)

    # Hide soundManager window and stop timer
    def hide(self):
        if self.soundManagerOk:
            self.closeWindowTimer.stop()
        super().hide()

    # Close window timer: 
    # Is started if source for volume action is key shortcut or mousewheel
    # Closes the window after timeout
    def timerCloseWindow(self):
        try:
            bugManager.push(bugManager.closeWindowTimer,'timerCloseWindow')
            self.closeWindowTimer.stop()
            super().hide()
            bugManager.pop(bugManager.closeWindowTimer)
        except: 
            bugManager.setError(bugManager.closeWindowTimer)

# class EpgManger
class EpgManager():
    def __init__(self, configManager=None, videoManager=None):
        self.epgManagerOk = False
        bugManager.push(bugManager.epgManager,'__init__: Started')
        try:
            # Basic settings
            bugManager.push(bugManager.epgManager,'__init__: Vars')
            self.configManager = configManager
            self.videoManager = videoManager
            bugManager.pop(bugManager.epgManager)

            # Set up EPG timer
            bugManager.push(bugManager.epgManager,'__init__: updateTime')
            self.updateEpgTimer = QtCore.QTimer()
            self.updateEpgTimerBusy = False
            self.updateEpgInterval = 300000 # Interval for EPG updates = 300s
            self.updateEpgTimer.setInterval(self.updateEpgInterval)
            self.updateEpgTimer.timeout.connect(self.timerUpdateEpg)
            bugManager.pop(bugManager.epgManager)
            
            self.epgManagerOk = True

            # Get EPG data
            bugManager.push(bugManager.epgManager,'__init__: Get epgData')
            self.epgData = []
            self.fetchEpgData(errorType=bugManager.epgManager)
            bugManager.pop(bugManager.epgManager)

            bugManager.pop(bugManager.epgManager)
        except:
            bugManager.setError(bugManager.epgManager)

    # Fetch EPG Data
    def fetchEpgData(self, errorType=1):
        if self.epgManagerOk and self.videoManager != None and self.videoManager.videoManagerOk:
            bugManager.push(errorType,'fetchEpgData')
            self.updateEpgTimer.stop()
            source = self.configManager.getSource()
            epgData = []
            if source == 'tvh':
                epgData = self.fetchEpgDataTvh(errorType=errorType)
                if len(epgData) > 0: 
                    self.updateEpgTimer.start(self.updateEpgInterval)
            elif source == 'm3u':
                epgData = self.fetchEpgDataM3u(errorType=errorType)
            self.epgData = epgData
            bugManager.pop(errorType)
    
    # Fetch EPG data from TVHServer
    def fetchEpgDataTvh(self, errorType=1):
        data = []
        try:
            bugManager.push(errorType,'fetchEpgDataTvh')
            channelList = self.videoManager.channelList
            tvhServer = self.configManager.getTvhServer()
            usrPw = (tvhServer.get('username', ''), tvhServer.get('password', ''))
            for row, tvChannel in enumerate(self.videoManager.tvChannels):
                epgEntry = []
                epgEntry.append(channelList.item(row,1))
                epgEntry.append(datetime.now())
                url = tvhServer['url'] + '/api/epg/events/grid'
                response = requests.get(url, params={'limit': 4, 'channel': tvChannel['uuid']}, auth=usrPw, timeout=10)
                if response.status_code == 200:
                    toolTip = epgEntry[0].text().strip()
                    epgResult = response.json()['entries']
                    for index, entry in enumerate(epgResult):
                        if index == 0:
                            epgEntry[1] = datetime.fromtimestamp(entry['stop'])
                        epgLine = datetime.fromtimestamp(entry['start']).strftime('%H:%M') + ' ' + entry['title']
                        if len(epgLine) > 0:
                            toolTip += '\n' + epgLine
                    epgEntry[0].setToolTip(toolTip)
                data.append(epgEntry)
            bugManager.pop(errorType)
        except:
            data = []
            bugManager.setError(errorType)
        return data

    # Fetch data from m3u playlist: Only returns channel name as tooltip
    def fetchEpgDataM3u(self, errorType=1):
        data = []
        try:
            bugManager.push(errorType, 'fetchEpgDataM3u')
            channelList = self.videoManager.channelList
            for row, tvChannel in enumerate(self.videoManager.tvChannels):
                epgEntry = []
                epgEntry.append(channelList.item(row,1))
                epgEntry.append(datetime.max)
                toolTip = epgEntry[0].text().strip()
                epgEntry[0].setToolTip(toolTip)
                data.append(epgEntry)
            bugManager.pop(errorType)
        except:
            data = []
            bugManager.setError(errorType)
        return data
    
    # Update EPG data (No update for m3u lists)
    def updateEpgData(self, errorType=1):
        if self.epgManagerOk and self.videoManager != None and self.videoManager.videoManagerOk:
            bugManager.push(errorType,'updateEpgData')
            if self.configManager.getSource() == 'tvh':
                self.updateEpgDataTvh(errorType=errorType)
            bugManager.pop(errorType)
    
    # Update EPG data from THVServer
    def updateEpgDataTvh(self, errorType=1):
        bugManager.push(errorType,'updateEpgDataTvh')
        tvhServer = self.configManager.getTvhServer()
        usrPw = (tvhServer.get('username', ''), tvhServer.get('password', ''))
        for row, tvChannel in enumerate(self.videoManager.tvChannels):
            if self.epgData[row][1] < datetime.now():
                url = tvhServer['url'] + '/api/epg/events/grid'
                response = requests.get(url, params={'limit': 4, 'channel': tvChannel['uuid']}, auth=usrPw, timeout=2)
                if response.status_code == 200:
                    epgResult = response.json()['entries']
                    epgEntry = []
                    epgEntry.append(self.epgData[row][0])
                    epgEntry.append(datetime.now())
                    toolTip = epgEntry[0].text().strip()
                    for index, entry in enumerate(epgResult):
                        if index == 0:
                            epgEntry[1] = datetime.fromtimestamp(entry['stop'])
                        epgLine = datetime.fromtimestamp(entry['start']).strftime('%H:%M') + ' ' + entry['title']
                        if len(epgLine) > 0:
                            toolTip += '\n' + epgLine
                    epgEntry[0].setToolTip(toolTip)
                    self.epgData[row] = epgEntry
        bugManager.pop(errorType)
    
    # Update EPG when videoManager channellist popup is about to be opened
    def waitForTimerAndUpdate(self, errorType=1):
        if self.epgManagerOk:
            # Wait for updateEpgTimer to avoid race condition
            maxWait = 0
            while self.updateEpgTimerBusy:
                time.sleep(100)
                maxWait += 100
                if maxWait > 10000:
                    self.updateEpgTimer.stop()
                    self.updateEpgTimerBusy = False
            # Update EPG - only if not already done by timer
            if maxWait == 0:
                try:
                    bugManager.push(errorType,'waitForTimerAndUpdate') 
                    self.updateEpgData(errorType=errorType)
                    bugManager.pop(errorType)
                except:
                    bugManager.setError(errorType)
    
    # Timer to periodicylly update EPG data in the background
    def timerUpdateEpg(self):
        try:
            bugManager.push(bugManager.updateEpgTimer,'timerUpdateEpg')
            if not self.videoManager.isVisible():
                self.updateEpgTimerBusy = True
                self.updateEpgData(errorType=bugManager.updateEpgTimer)
                self.updateEpgTimerBusy = False
            bugManager.pop(bugManager.updateEpgTimer)
        except:
            self.updateEpgTimer.stop()
            bugManager.setError(bugManager.updateEpgTimer)
    
# class HelpManager
class HelpManager():
    def __init__(self):
        self.helpDic = {'de' : [], 'en': []}
        bugManager.push(bugManager.helpManager,'__init__: Reading Help File')
        try:
            # Get help lines from help.txt
            helpFilePath = os.path.join(resourcePath,'Help.txt')
            if os.path.isfile(helpFilePath):
                f = open(helpFilePath, 'r', encoding='utf8')
                lines = f.readlines()
                f.close()
                for line in lines:
                    parts = line.strip().split('~')
                    if len(parts) == 2:
                        helpLine = parts[1].replace('\n','').rstrip()
                        if parts[0].strip() == 'de':
                            self.helpDic['de'].append(helpLine)
                        elif parts[0].strip() == 'en':
                            self.helpDic['en'].append(helpLine)
            else:
                raise
            bugManager.pop(bugManager.helpManager)
        except:
            self.helpDic = {'de' : [], 'en': []}
            bugManager.setError(bugManager.helpManager)
        pass

    # Return help lines
    def getHelpText(self, language='de'):
        helpText = self.helpDic['de']
        if language == 'en':
            helpText = self.helpDic['en']
        return helpText

class InfoDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, caption='', infoText=None):
        super().__init__(parent)
        # Setup UI
        self.setWindowTitle(caption)
        self.parent = parent
        self.setWindowFlags(QtCore.Qt.WindowType.Dialog)
        self.resize(int(450*scalingFactor), int(300*scalingFactor))
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName(u"verticalLayout")
        # QListWidget lwInfoText
        self.lwInfoText = QtWidgets.QListWidget(self)
        self.lwInfoText.setObjectName(u"lwHelpText")
        font = QtGui.QFont()
        font.setFamilies([u"Courier New"])
        font.setBold(True)
        self.lwInfoText.setFont(font)
        self.lwInfoText.setStyleSheet(u"")
        self.lwInfoText.setAutoScroll(True)
        self.verticalLayout.addWidget(self.lwInfoText)
        # QPushButton pbOk
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.hSpacer1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(self.hSpacer1)
        self.pbOK = QtWidgets.QPushButton(self)
        self.pbOK.setObjectName(u"pbOK")
        self.pbOK.setText('OK')
        self.pbOK.setStyleSheet(u"background-color: rgb(214, 214, 214);")
        self.horizontalLayout.addWidget(self.pbOK)
        self.hSpacer2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(self.hSpacer2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pbOK.clicked.connect(self.closeDialog)
        # Set up Infotext
        for line in infoText:
            self.lwInfoText.addItem(line)

    # Close dialog
    def closeDialog(self):
        self.close()

# class AboutDialog
class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, language='de'):
        super().__init__(parent)
        pictureName = 'Logo-de.png'
        if language != 'de':
            pictureName = 'Logo-en.png'
        # Set up UI
        self.parent = parent
        self.setWindowFlags(QtCore.Qt.WindowType.Dialog)
        self.setMinimumSize(QtCore.QSize(400, 400))
        self.resize(int(400*scalingFactor), int(400*scalingFactor))
        self.setStyleSheet(u"background-color: rgb(235, 235, 235); color: rgb(0, 0, 0);")
        # Set up QLabel lbLogo with Pixmap
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbLogo = QtWidgets.QLabel(self)
        self.lbLogo.setMinimumSize(QtCore.QSize(180, 175))
        self.lbLogo.setPixmap(QtGui.QPixmap(os.path.join(resourcePath,pictureName)))
        self.lbLogo.setScaledContents(True)
        self.lbLogo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.lbLogo)
        # Set up QPushButton pbOk
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.hSpacer1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(self.hSpacer1)
        self.pbOK = QtWidgets.QPushButton(self)
        self.pbOK.setText('OK')
        self.horizontalLayout.addWidget(self.pbOK)
        self.hSpacer2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(self.hSpacer2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pbOK.clicked.connect(self.closeDialog)

    # Close dialog
    def closeDialog(self) :
        self.close()

# Class Bug Manager
# Purpose: Simplify debugging and bug fixing for user reported errors
# How it works:
#   - Each class and each timer has its own error stack.
#   - Each error is marked by a unique number.
#   - Error number and program step description are pushed on / popped from error stack.
#     If error occurs exception is caught and messages remain on the stack.
#     Afterwards a time stamp is added and the error number is increased.
#   - Thus each error has a stack trace which helps to analyze bug conditions.
# If user quits program an error message is shown and errors are saved to CyberTelly.log
# Beside errors there are notifications:
#   If the errorDic only contains notifications it is stored to CyberTelly.log, but
#   there is no message if user quits the program.
class BugManager():
    def __init__(self):
        self.logFile = os.path.join(configPath,'CyberTelly.log')
        # Get text for error dialog from global var errorDic
        self.errorMessage = getErrorDescription(key='programError',language=sysLanguage, singleString=True)
        self.maxExceptions = 50
        self.maxNotifications = 50
        # Error type codes
        self.systemInfo = 0
        self.mainProgram = 1
        self.configManager = 2
        self.configDialog = 3
        self.videoManager = 4
        self.soundManager = 5
        self.epgManager = 6
        self.helpManager = 7
        self.cursorOffTimer = 8
        self.setIndicatorGeometryTimer = 9
        self.fixVlcCursorIssueTimer = 10
        self.setupTimer = 11
        self.statusTimer = 12
        self.closeWindowTimer = 13
        self.updateEpgTimer = 14
        # Create error dictionary and set basic vars
        self.errorDic = self.createErrorDic()
        self.fatalErrorOccured = False
        self.errorOccurred = False
        self.notification = False
    
    # Create information about the system on which the error occurred
    def createSysInfo(self):
        distro = '----' if platform.system() != 'Linux' else platform.freedesktop_os_release()['NAME'] + ' ' + platform.freedesktop_os_release()['VERSION']
        sessionType = '----' if platform.system() != 'Linux' else getSessionType()
        sysInfo = [
            'Program version: ' + version + ' ' + build,
            'Platform.......: ' + platform.system() + ' ' + platform.release(),
            'Distribution...: ' + distro,
            'Session-Type...: ' + sessionType,
            'VLC-Player.....: ' + getVlcVersion(),
        ]
        return sysInfo
    
    # Create error dictionary
    def createErrorDic(self):
        errorDic = {
            self.systemInfo: self.createSysInfo(),
            self.mainProgram: {
                'name': 'Main Program',
                'exceptCnt': 0,
                'notifyCnt': 0,
                'maxExcept': 100,
                'maxNotify': 100,
                'infoStack' : []
            },
            self.configManager: {
                'name': 'Class: ConfigManager',
                'exceptCnt': 0,
                'notifyCnt': 0,
                'maxExcept': 100,
                'maxNotify': 100,
                'infoStack' : []
            },
            self.configDialog: {
                'name': 'Dialog: ConfigDialog',
                'exceptCnt': 0,
                'notifyCnt': 0,
                'maxExcept': 10,
                'maxNotify': 10,
                'infoStack' : []
            },
            self.videoManager: {
                'name': 'Class: VideoManager',
                'exceptCnt': 0,
                'notifyCnt': 0,
                'maxExcept': 100,
                'maxNotify': 100,
                'infoStack' : []
            },
            self.soundManager: {
                'name': 'Class: SoundManager',
                'exceptCnt': 0,
                'notifyCnt': 0,
                'maxExcept': 100,
                'maxNotify': 100,
                'infoStack' : []
            },
            self.epgManager: {
                'name': 'Class: EpgManager',
                'exceptCnt': 0,
                'notifyCnt': 0,
                'maxExcept': 100,
                'maxNotify': 100,
                'infoStack' : []
            },
            self.helpManager: {
                'name': 'Class: HelpManager',
                'exceptCnt': 0,
                'notifyCnt': 0,
                'maxExcept': 5,
                'maxNotify': 5,
                'infoStack' : []
            },
            self.cursorOffTimer: {
                'name': 'Timer: cursorOffTimer',
                'exceptCnt': 0,
                'notifyCnt': 0,
                'maxExcept': 5,
                'maxNotify': 5,
                'infoStack' : []
            },
            self.setIndicatorGeometryTimer: {
                'name': 'Timer: setIndicatorGeometryTimer',
                'exceptCnt': 0,
                'notifyCnt': 0,
                'maxExcept': 5,
                'maxNotify': 5,
                'infoStack' : []
            },
            self.fixVlcCursorIssueTimer: {
                'name': 'Timer: fixVlcCursorIssueTimer',
                'exceptCnt': 0,
                'notifyCnt': 0,
                'maxExcept': 5,
                'maxNotify': 5,
                'infoStack' : []
            },
            self.setupTimer: {
                'name': 'Timer: setupTimer',
                'exceptCnt': 0,
                'notifyCnt': 0,
                'maxExcept': 5,
                'maxNotify': 5,
                'infoStack' : []
            },
            self.statusTimer: {
                'name': 'Timer: statusTimer',
                'exceptCnt': 0,
                'notifyCnt': 0,
                'maxExcept': 5,
                'maxNotify': 5,
                'infoStack' : []
            },
            self.closeWindowTimer: {
                'name': 'Timer: closeWindowTimer',
                'exceptCnt': 0,
                'notifyCnt': 0,
                'maxExcept': 5,
                'maxNotify': 5,
                'infoStack' : []
            },
            self.updateEpgTimer: {
                'name': 'Timer: updateEpgTimer',
                'exceptCnt': 0,
                'notifyCnt': 0,
                'maxExcept': 5,
                'maxNotify': 5,
                'infoStack' : []
            }
        }
        return errorDic

    # Push description of program step onto stack
    def push(self, errorType, functionName, setError=False, setNotification=False):
        indexPos = -1
        if errorType != None:
            indexPos = len(self.errorDic[errorType]['infoStack'])
            if setError:
                self.errorOccurred = True    
                self.notification = True
            elif setNotification:
                self.notification = True
            exceptCnt = self.errorDic[errorType]['exceptCnt']
            if not (setError or setNotification):
                if exceptCnt < self.errorDic[errorType]['maxExcept']:
                    self.errorDic[errorType]['infoStack'].append((exceptCnt,str(self.errorDic[errorType]['exceptCnt']).zfill(2) + ' ' + functionName))
                else:
                    indexPos = -1
            elif self.errorDic[errorType]['notifyCnt'] < self.errorDic[errorType]['maxNotify']:
                self.errorDic[errorType]['infoStack'].append((-1,'-- ' + functionName))
        return indexPos
    
    # Pop description of program step from stack
    def pop(self, errorType, stackPos=None):
        if errorType != None:
            if stackPos == None:
                stackPos = len(self.errorDic[errorType]['infoStack'])-1
            if stackPos != -1 and stackPos in range(len(self.errorDic[errorType]['infoStack'])) and \
                self.errorDic[errorType]['infoStack'][stackPos][0] == self.errorDic[errorType]['exceptCnt']:
                    self.errorDic[errorType]['infoStack'].pop(stackPos)

    # Set error indicating vars and increase error counter
    def setError(self, errorType, isFatalError=False):
        if errorType != None:
            if isFatalError:
                self.fatalErrorOccured = True
            self.errorOccurred = True
            self.notification = True
            if self.errorDic[errorType]['exceptCnt'] < self.errorDic[errorType]['maxExcept']:
                self.errorDic[errorType]['infoStack'].append((self.errorDic[errorType]['exceptCnt'], 
                                                            str(self.errorDic[errorType]['exceptCnt']).zfill(2) + ' ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.errorDic[errorType]['exceptCnt'] += 1

    # Save errorDic to CyberTelly.log
    def saveErrorLog(self):
        try:
            f = open(self.logFile,'w', encoding='utf-8')
            f.write('**********************************************\n')
            f.write('*  CyberTelly Log File  ')
            f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '  *\n')
            f.write('**********************************************\n')
            f.write('* For bug fixing you may send this file to:  *\n')
            f.write('* >>>>>>>>>>> info@cybertelly.tv <<<<<<<<<<  *\n')
            f.write('* Please add a short error description.      *\n')
            f.write('**********************************************\n')
            for errType in self.errorDic.keys():
                if errType == self.systemInfo:
                    for line in self.errorDic[errType]:
                        f.write('\n'+line)    
                else:
                    errDic = self.errorDic[errType]
                    f.write('\n\n' + 'Source.....: '+ errDic['name'] + '\n')
                    f.write(          'ExceptCount: '+ str(errDic['exceptCnt']) + '\n')
                    f.write(          'Stack Trace:')
                    if len(errDic['infoStack']) > 0:
                        for num, item in enumerate(errDic['infoStack']):
                            f.write('\n  ' + item[1])
                    else:
                        f.write(' ----')
            f.close()
        except:
            pass

##################################################
# Globally available functions and their purpose #
##################################################

# Calculate average screen dpi: Necessary if system has two or more screens with different scaling factors.
def getDpi():
    screens = scInfo.get_monitors()
    dpi = 0.0
    numScreens = 0
    try:
        for screen in screens:
            scrDpi = screen.width / (screen.width_mm / 25.4)
            if screen.width <= 1600:
                scrDpi = 96
            dpi += scrDpi
            numScreens += 1
        dpi = int(dpi / numScreens)
        if dpi < 120:
            dpi = 96
        elif dpi < 144:
            dpi = 120
        elif dpi < 168:
            dpi = 144
        elif dpi < 192:
            dpi = 168
        else:
            dpi = 192
    except:
        dpi = 96
    return dpi

# Set all necessary path vars
# Returns different results, if program is run from either a virtual environment or a pyinstaller package
def setProgPaths():
    try:
        pathsOk = True
        progPath = ''
        resourcePath = ''
        configPath = ''
        if getattr(sys, 'frozen', False):
            progPath = sys._MEIPASS
            # Bug fix for VLC / PyInstaller: Plugin-Folder is not found (Linux only)
            # Sets environment var VLC_PLUGIN_PATH
            if sys.platform.startswith('linux'):
                result = subprocess.run(['whereis', 'vlc'],text= True,capture_output=True)
                paths = str(result).split(' ')
                for path in paths:
                    pluginPath = os.path.join(path.strip(),'plugins')
                    if os.path.isdir(pluginPath):
                        os.environ['VLC_PLUGIN_PATH'] = pluginPath
                        break
        else:
            progPath = os.path.dirname(os.path.abspath(__file__))
        resourcePath = os.path.join(progPath,'resources')
        progName = os.path.basename(__file__)
        confDirName, ext = os.path.splitext(progName)
        configPath = os.path.join(os.path.expanduser('~'), confDirName)
        os.chdir(progPath)
    except:
        pathsOk = False
        progPath = ''
        resourcePath = ''
        configPath = os.path.join(os.path.expanduser('~'), 'CyberTelly')
    return pathsOk, progPath, progName, resourcePath, configPath

# Determine system language
def getSystemLanguage():
    sysLanguage = 'de'
    try:
        localeInfo = locale.getlocale()
        if localeInfo[0] != None and not localeInfo[0].startswith('de'):
            sysLanguage = 'en'
    except:
        sysLanguage = 'de'
    return sysLanguage

# Read error dictionary at startup with fallback to predefined messages
def readErrorDic():
    readError = True
    errorDic = {'de': {}, 'en': {}}
    errorsFilePath = os.path.join(resourcePath,'Errors.txt')
    lines = []
    for enc in ['utf-8', 'cp1252']: # cp1252 = ANSI
        try:
            f = open(errorsFilePath,'r', encoding=enc)
            lines = f.readlines()
            f.close()
            break
        except:
            lines = []
    for line in lines:
        parts = line.strip().split('~')
        if len(parts) == 3:
            parts[0] = parts[0].strip()
            parts[1] = parts[1].strip()
            if parts[0] in errorDic.keys():
                readError = False
                if parts[1] in errorDic[parts[0]].keys():
                    errorDic[parts[0]][parts[1]].append(parts[2])
                else:
                    errorDic[parts[0]][parts[1]] = [parts[2]]
    if readError:
        errorDic['de']['readError'] = [
            'CyberTelly: Programmfehler aufgetreten',
            '',
            'Da Fehlermeldungen nicht gefunden wurden, ist eine',
            'qualifizierte Beschreibung nicht verfügbar.',
            'Weitere Infos ggf. in der Datei CyberTelly.log.',
            '',
            'Speicherort:',
            'Windows: C:\\Benutzer\\<user>\\CyberTelly\\',
            'Linux:   /home/<user>/CyberTelly/'
        ]
        errorDic['en']['readError'] = [
            'CyberTelly: Error occurred',
            '',
            "Error messages could not be found. That's why",
            "a detailed description is not available.",
            'More Information may be in file CyberTelly.log.',
            '',
            'Where to find CyberTelly.log:',
            'Windows: C:\\Users\\<user>\\CyberTelly\\',
            'Linux:   /home/<user>/CyberTelly/'
        ]
    return errorDic

# Get error messages from error dictionary
def getErrorDescription(key=None, language='de', singleString=False):
    description = []
    if language in errorDic.keys():
        if key != None:
            if not key in errorDic[language].keys():
                key = 'readError'
            if key in errorDic[language].keys():
                description = errorDic[language][key]
                if singleString:
                    errString = ''
                    lineSeparator = ''
                    for line in description:
                        errString += lineSeparator + line
                        lineSeparator = '\n'
                    description = errString
    return description
        
# Determine if X11 or wayland is running (Linux)
def getSessionType():
    sessionType = 'x11'
    if sys.platform.startswith('linux'):
        envVar = os.environ['XDG_SESSION_TYPE']
        if envVar.lower() == 'wayland':
            sessionType = 'wayland'
    return sessionType

# Determine VLC version: Used in BugManager
def getVlcVersion():
    try:
        if platform.system() == 'Windows':
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\VideoLAN\VLC")
                version, _ = winreg.QueryValueEx(key, "Version")
                return 'VLC-Version ' + version
            except:
                # On 64-bit Windows, VLC might be in Wow6432Node
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\VideoLAN\VLC")
                    version, _ = winreg.QueryValueEx(key, "Version")
                    return 'VLC-Version ' + version
                except:
                    return 'VLC-Version unbekannt'
        else:
            vlcPath = 'vlc'
            result = subprocess.run([vlcPath, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.splitlines()[0].strip()
                return version
            else:
                return 'VLC-Version unbekannt'
    except:
        return 'VLC-Version unbekannt'

###########################
# CyberTelly Main Program #
###########################

if __name__ == "__main__":
    result = 1
    pathsOk, progPath, progName, resourcePath, configPath = setProgPaths()
    sysLanguage = getSystemLanguage()
    errorDic = readErrorDic()
    bugManager = BugManager()
    try:
        if getSessionType() == 'x11': # x11 = Default value for Linux with x11, Windows und MacOS
            # QT_ENABLE_HIGHDPI_SCALING = 0: 
            #   If high dpi scaling is enabled, systems with two or more screens and different scaling factors
            #   completely destroy window geometry if window is moved between the screens.
            #   That's why it has to be disabled - although not recommended.
            os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '0'
            # Calculate average dpi (Necessary if high dpi scaling is disabled)
            os.environ['QT_USE_PHYSICAL_DPI'] = '1'
            dpi = getDpi()
            scalingFactor = dpi / 96
            os.environ['QT_FONT_DPI'] = str(dpi)
            # Setup main window
            cyberTellyApp = QtWidgets.QApplication(sys.argv)
            cyberTellyApp.setAttribute(QtCore.Qt.ApplicationAttribute.AA_NativeWindows)
            cyberTellyApp.setStyle('fusion')
            cyberTellyWin = Window()
            cyberTellyWin.show()
        else:
            # Show error message if session type is wayland:
            # libvlc that comes with VLC 3.0.20+ doesn't support wayland.
            cyberTellyApp = QtWidgets.QApplication(sys.argv)
            dlg = QtWidgets.QMessageBox()
            dlg.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
            dlg.setWindowTitle(" ")
            dlg.setText(getErrorDescription(key='waylandError',language=sysLanguage,singleString=True))
            dlg.show()
        # Run application
        result = cyberTellyApp.exec()
    except:
        pass
    # Save CybterTelly.log if errors or notifications have occurred.
    if bugManager.notification:
        bugManager.saveErrorLog()
    sys.exit(result)