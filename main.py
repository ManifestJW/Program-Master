# ============================================
# JAPM (Just Another Program Manager)
# Author: Nayla Hanegan (naylahanegan@gmail.com)
# Date: 9/14/2024
# License: MIT
# ============================================

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import queue
import threading
import customtkinter
import version
import webbrowser
import platform
import credits
from CTkToolTip import *

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window properties
        self.title("Just Another Program Manager")  # Set the window title
        self.geometry(f"{1330}x{780}")  # Set the window size

        # Configure grid layout for the main application window
        self.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand
        self.grid_columnconfigure((2, 3), weight=0)  # Fixed width for columns 2 and 3
        self.grid_rowconfigure((0, 1, 2), weight=1)  # Allow rows 0, 1, and 2 to expand

        # Create sidebar frame for navigation
        self.sidebarFrame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")  # Position sidebar frame
        self.sidebarFrame.grid_rowconfigure(3, weight=1)  # Allow row 3 to expand

        # Add logo label to the sidebar
        self.logoLabel = customtkinter.CTkLabel(self.sidebarFrame, text="Just Another\nProgram Manager", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.logoLabel.grid(row=0, column=0, padx=20, pady=(20, 10))  # Position logo label

        # Create buttons for navigation
        self.applicationsButton = customtkinter.CTkButton(self.sidebarFrame, text="Applications", command=self.appsView)
        self.applicationsButton.grid(row=1, column=0, padx=20, pady=10)  # Position Applications button

        self.creditsButton = customtkinter.CTkButton(self.sidebarFrame, text="Credits", command=self.creditsView)
        self.creditsButton.grid(row=4, column=0, padx=20, pady=10)  # Position Credits button

        # Display application version in the sidebar
        self.versionLabel = customtkinter.CTkLabel(self.sidebarFrame, text=version.appVersion, anchor="w", font=("Arial", 16, "bold"))
        self.versionLabel.grid(row=5, column=0, padx=20, pady=(10, 0))  # Position version label

        self.currentGameFrame = None  # Placeholder for the current game frame

        # Set default button states and initialize the main frame
        self.applicationsButton.configure(state="disabled")  # Disable Applications button initially
        self.currentGameFrame = self.createAppInstaller()  # Create the app installer frame
        self.currentGameFrame.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), rowspan=3, sticky="nsew")  # Position the frame

    def appsView(self):
        # Switch to the applications view
        self.applicationsButton.configure(state="disabled")  # Disable Applications button
        self.creditsButton.configure(state="enabled")  # Enable Credits button
        self.resetGameFrames()  # Reset any existing frames
        self.createGameFrame("App Installers")  # Create the app installers frame

    def creditsView(self):
        # Switch to the credits view
        self.applicationsButton.configure(state="enabled")  # Enable Applications button
        self.creditsButton.configure(state="disabled")  # Disable Credits button
        self.resetGameFrames()  # Reset any existing frames
        self.createGameFrame("Credits")  # Create the credits frame

    def resetGameFrames(self):
        # Remove any existing game-specific widgets from the main frame
        if self.currentGameFrame:
            self.currentGameFrame.destroy()  # Destroy the current game frame

    def createGameFrame(self, appType):
        # Create a new game frame based on the selected application type
        self.resetGameFrames()  # Reset existing frames

        if appType == "App Installers":
            self.currentGameFrame = self.createAppInstaller()  # Create app installer frame
        elif appType == "Credits":
            self.currentGameFrame = self.createCredits()  # Create credits frame
        
        self.currentGameFrame.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), rowspan=3, sticky="nsew")  # Position the new frame

    def createCredits(self):
        # Create the credits frame with tabs for different sections
        frame = customtkinter.CTkFrame(self, fg_color=("#fcfcfc", "#2e2e2e"))  # Create frame with light and dark mode colors
        tabview = customtkinter.CTkTabview(frame, width=2000, height=650, fg_color=("#fcfcfc", "#323232"))  # Create tab view
        tabview.pack(padx=20, pady=20)  # Pack the tab view into the frame
        tabview.add("Credits")  # Add Credits tab
        tabview.add("About")  # Add About tab
        tabview.add("License")  # Add License tab
        tabview.set("About")  # Set default tab to About

        # Add content to the License tab
        mitLicenseWidget = customtkinter.CTkLabel(tabview.tab("License"), width=80, height=20, text=credits.get_mit_license_text())
        mitLicenseWidget.pack(padx=10, pady=10)  # Pack the license text

        # Add content to the Credits tab
        creditsWidget = customtkinter.CTkLabel(tabview.tab("Credits"), width=80, height=20, text=credits.get_credits_text())
        creditsWidget.pack(padx=10, pady=10)  # Pack the credits text

        # Add content to the About tab
        aboutWidget = customtkinter.CTkLabel(tabview.tab("About"), width=80, height=20, text=credits.get_about_text())
        aboutWidget.pack(padx=10, pady=10)  # Pack the about text

        return frame  # Return the credits frame

    def createAppInstaller(self):
        # Create the app installer frame with various sections
        frame = customtkinter.CTkFrame(self, fg_color=("#fcfcfc", "#2e2e2e"))  # Create frame with light and dark mode colors
        frame.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")  # Position the frame with padding
    
        # Create a border frame for the browser section
        borderFrameBrowser = customtkinter.CTkFrame(frame, fg_color="#00FFFF", border_width=2, width=240, height=690)  # Aqua border color
        borderFrameBrowser.grid(row=1, column=0, padx=(5, 0), pady=(5, 5), sticky="nsew")  # Position the border frame
        browserCanvas = customtkinter.CTkCanvas(borderFrameBrowser, bg="#3a3a3a", width=210, height=690)  # Dark background for the canvas
        browserFrame = customtkinter.CTkFrame(browserCanvas, fg_color=("#3a3a3a", "#3a3a3a"))  # Dark frame for browser widgets
        browserScrollbar = customtkinter.CTkScrollbar(borderFrameBrowser, orientation="vertical", command=browserCanvas.yview, fg_color="#3a3a3a")  # Dark scrollbar
        browserScrollbar.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="ns")  # Position scrollbar next to the canvas
        browserCanvas.configure(yscrollcommand=browserScrollbar.set)  # Link scrollbar to canvas
        browserCanvas.grid(row=0, column=0, padx=(5, 0), pady=(5, 5), sticky="nsew")  # Position canvas in the border frame
        browserCanvas.create_window((0, 0), window=browserFrame, anchor="nw")  # Create window in canvas for browser frame
        self.createBrowserWidgets(browserFrame)  # Create browser widgets in the frame
    
        # Create a border frame for the chat section
        borderFrameChat = customtkinter.CTkFrame(frame, fg_color="#00FFFF", border_width=2, width=240, height=690)  # Aqua border color
        borderFrameChat.grid(row=1, column=3, padx=(5, 0), pady=(5, 5), sticky="nsew")  # Position the border frame
        chatCanvas = customtkinter.CTkCanvas(borderFrameChat, bg="#3a3a3a", width=210, height=690)  # Dark background for the canvas
        chatFrame = customtkinter.CTkFrame(chatCanvas, fg_color=("#3a3a3a", "#3a3a3a"))  # Dark frame for chat widgets
        chatScrollbar = customtkinter.CTkScrollbar(borderFrameChat, orientation="vertical", command=chatCanvas.yview, fg_color="#3a3a3a")  # Dark scrollbar
        chatScrollbar.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="ns")  # Position scrollbar next to the canvas
        chatCanvas.configure(yscrollcommand=chatScrollbar.set)  # Link scrollbar to canvas
        chatCanvas.grid(row=0, column=0, padx=(5, 0), pady=(5, 5), sticky="nsew")  # Position canvas in the border frame
        chatCanvas.create_window((0, 0), window=chatFrame, anchor="nw")  # Create window in canvas for chat frame
        self.createChatWidgets(chatFrame)  # Create chat widgets in the frame

        # Create a border frame for the development section
        borderFrameDev = customtkinter.CTkFrame(frame, fg_color="#00FFFF", border_width=2, width=240, height=690)  # Aqua border color
        borderFrameDev.grid(row=1, column=6, padx=(5, 0), pady=(5, 5), sticky="nsew")  # Position the border frame
        devCanvas = customtkinter.CTkCanvas(borderFrameDev, bg="#3a3a3a", width=210, height=690)  # Dark background for the canvas
        devFrame = customtkinter.CTkFrame(devCanvas, fg_color=("#3a3a3a", "#3a3a3a"))  # Dark frame for development widgets
        devScrollbar = customtkinter.CTkScrollbar(borderFrameDev, orientation="vertical", command=devCanvas.yview, fg_color="#3a3a3a")  # Dark scrollbar
        devScrollbar.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="ns")  # Position scrollbar next to the canvas
        devCanvas.configure(yscrollcommand=devScrollbar.set)  # Link scrollbar to canvas
        devCanvas.grid(row=0, column=0, padx=(5, 0), pady=(5, 5), sticky="nsew")  # Position canvas in the border frame
        devCanvas.create_window((0, 0), window=devFrame, anchor="nw")  # Create window in canvas for development frame
        self.createDevWidgets(devFrame)  # Create development widgets in the frame

        # Create a border frame for the documentation section
        borderFrameDocu = customtkinter.CTkFrame(frame, fg_color="#00FFFF", border_width=2, width=240, height=690)  # Aqua border color
        borderFrameDocu.grid(row=1, column=9, padx=(5, 0), pady=(5, 5), sticky="nsew")  # Position the border frame
        docuCanvas = customtkinter.CTkCanvas(borderFrameDocu, bg="#3a3a3a", width=210, height=690)  # Dark background for the canvas
        docuFrame = customtkinter.CTkFrame(docuCanvas, fg_color=("#3a3a3a", "#3a3a3a"))  # Dark frame for documentation widgets
        docuScrollbar = customtkinter.CTkScrollbar(borderFrameDocu, orientation="vertical", command=devCanvas.yview, fg_color="#3a3a3a")  # Dark scrollbar
        docuScrollbar.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="ns")  # Position scrollbar next to the canvas
        docuCanvas.configure(yscrollcommand=docuScrollbar.set)  # Link scrollbar to canvas
        docuCanvas.grid(row=0, column=0, padx=(5, 0), pady=(5, 5), sticky="nsew")  # Position canvas in the border frame
        docuCanvas.create_window((0, 0), window=docuFrame, anchor="nw")  # Create window in canvas for documentation frame
        self.createDocuWidgets(docuFrame)  # Create documentation widgets in the frame
    
        # Update the scroll region of the canvas when the frame is resized
        def update_scroll_region(event):
            browserCanvas.configure(scrollregion=browserCanvas.bbox("all"))  # Update scroll region for browser canvas
            chatCanvas.configure(scrollregion=chatCanvas.bbox("all"))  # Update scroll region for chat canvas
    
        browserFrame.bind("<Configure>", update_scroll_region)  # Bind resize event for browser frame
        chatFrame.bind("<Configure>", update_scroll_region)  # Bind resize event for chat frame
    
        # Create category labels for each section with right padding
        self.browserLabel = customtkinter.CTkLabel(browserFrame, text="Internet Browsers", font=("Arial", 16, "bold"))
        self.browserLabel.place(x=5, y=5)  # Position browser label
    
        self.chatLabel = customtkinter.CTkLabel(chatFrame, text="Communication", font=("Arial", 16, "bold"))
        self.chatLabel.place(x=5, y=5)  # Position chat label
    
        self.devLabel = customtkinter.CTkLabel(devFrame, text="Development", font=("Arial", 16, "bold"))
        self.devLabel.place(x=5, y=5)  # Position development label

        self.docuLabel = customtkinter.CTkLabel(docuFrame, text="Documents", font=("Arial", 16, "bold"))
        self.docuLabel.place(x=5, y=5)  # Position documentation label

        # Create the Install Selected button above the frames
        self.parseButton = customtkinter.CTkButton(master=frame, command=self.parseDownloads, text="Install Selected", fg_color="#00FFFF")  # Aqua color
        self.parseButton.grid(row=0, column=0, padx=(5, 5), pady=(10, 5), sticky="w")  # Position Install Selected button
    
        # Create the Update All Apps button next to Install Selected
        self.updateButton = customtkinter.CTkButton(master=frame, command=self.updateAllApps, text="Update ALL Apps", width=150, fg_color="#00FFFF")  # Aqua color
        self.updateButton.place(x=165, y=10)  # Position next to the Install Selected button

        return frame  # Return the app installer frame

    def createBrowserWidgets(self, frame):
        # Define browser options with their corresponding open functions
        browsers = [
            ("", lambda: None),  # Placeholder that does nothing
            ("Arc", lambda: webbrowser.open('https://arc.net', new=2)),
            ("Brave", lambda: webbrowser.open('https://brave.com', new=2)),
            ("Chrome", lambda: webbrowser.open('https://www.google.com/chrome', new=2)),
            ("Chromium", lambda: webbrowser.open('https://www.chromium.org/Home/', new=2)),
            ("Edge", lambda: webbrowser.open('https://www.microsoft.com/en-us/edge', new=2)),
            ("Firefox", lambda: webbrowser.open('https://www.mozilla.org/en-US/firefox/new', new=2)),
            ("Floorp", lambda: webbrowser.open('https://floorp.app', new=2)),
            ("LibreWolf", lambda: webbrowser.open('https://librewolf.net', new=2)),
            ("Opera", lambda: webbrowser.open('https://www.opera.com', new=2)),
            ("Opera GX", lambda: webbrowser.open('https://www.opera.com/gx', new=2)),
            ("Orion", lambda: webbrowser.open('https://kagi.com/orion', new=2)),
            ("Thorium", lambda: webbrowser.open('https://thorium.rocks', new=2)),
            ("Tor", lambda: webbrowser.open('https://www.torproject.org/download', new=2)),
            ("Ungoogled Chromium", lambda: webbrowser.open('https://ungoogled-software.github.io/ungoogled-chromium-binaries', new=2)),
            ("Vivaldi", lambda: webbrowser.open('https://vivaldi.com', new=2)),
            ("Zen", lambda: webbrowser.open('https://zen-browser.app', new=2)),
        ]

        for i, (name, command) in enumerate(browsers):
            button = customtkinter.CTkButton(frame, text=f"[?]", font=("Arial", 11, "bold"), text_color="aqua", command=command, fg_color="#3a3a3a", hover_color="#3a3a3a", width=6)
            button.grid(row=i + 1, column=0, sticky="w", pady=(5, 0), padx=(0, 0))  # 5 pixels padding above and below
            
            toggle = customtkinter.CTkCheckBox(frame, text=name, checkbox_width=12, checkbox_height=12)
            toggle.grid(row=i + 1, column=1, sticky="w", pady=(5, 0), padx=(0, 0))  # Align with the button and same padding
            
            goodName = name.replace(" ", "").lower()
            setattr(self, f"{goodName}Toggle", toggle)  # Dynamically set toggle attribute

    def createChatWidgets(self, frame):
        # Define chat application options with invalid links
        chatApps = [
            ("", lambda: None),  # Placeholder that does nothing
            ("Discord", lambda: webbrowser.open('https://discord.com', new=2)),
            ("Ferdium", lambda: webbrowser.open('https://ferdium.org', new=2)),
            ("Guilded", lambda: webbrowser.open('https://guilded.gg', new=2)),
            ("TeamSpeak", lambda: webbrowser.open('https://teamspeak.com', new=2)),
            ("Textual", lambda: webbrowser.open('https://www.//chatterino.com', new=2)),
            ("Google Chat", lambda: webbrowser.open('https://github.com/squalou/google-chat-linux', new=2)),
            ("Chatterino", lambda: webbrowser.open('https:/https://chatterino.com/', new=2)),
            ("HexChat", lambda: webbrowser.open('https://hexchat.github.io/', new=2)),
            ("Jami", lambda: webbrowser.open('https://jami.net/', new=2)),
            ("Linphone", lambda: webbrowser.open('https://www.linphone.org/', new=2)),
            ("Element", lambda: webbrowser.open('https://element.io', new=2)),
            ("Session", lambda: webbrowser.open('https://getsession.org', new=2)),
            ("Signal", lambda: webbrowser.open('https://signal.org/', new=2)),
            ("Skype", lambda: webbrowser.open('https://www.skype.com/', new=2)),
            ("Slack", lambda: webbrowser.open('https://slack.com', new=2)),
            ("Teams", lambda: webbrowser.open('https://www.microsoft.com/en-us/microsoft-teams/group-chat-software', new=2)),
            ("Telegram", lambda: webbrowser.open('https://telegram.org/', new=2)),
            ("Thunderbird", lambda: webbrowser.open('https://www.thunderbird.net/', new=2)),
        ]

        for i, (name, command) in enumerate(chatApps):
            button = customtkinter.CTkButton(frame, text=f"[?]", font=("Arial", 11, "bold"), text_color="aqua", command=command, fg_color="#3a3a3a", hover_color="#3a3a3a", width=6)
            button.grid(row=i + 1, column=0, sticky="w", pady=(5, 0), padx=(0, 0))  # 5 pixels padding above and below
            
            toggle = customtkinter.CTkCheckBox(frame, text=name, checkbox_width=12, checkbox_height=12)
            toggle.grid(row=i + 1, column=1, sticky="w", pady=(5, 0), padx=(0, 0))  # Align with the button and same padding
            
            goodName = name.replace(" ", "").lower()
            setattr(self, f"{goodName}Toggle", toggle)  # Dynamically set toggle attribute

    def createDevWidgets(self, frame):
        # Define development application options with invalid links
        devApps = [
            ("", lambda: None),  # Placeholder that does nothing
            ("Git", lambda: webbrowser.open('https://git-scm.com', new=2)),
        ]

        for i, (name, command) in enumerate(devApps):
            button = customtkinter.CTkButton(frame, text=f"[?]", font=("Arial", 11, "bold"), text_color="aqua", command=command, fg_color="#3a3a3a", hover_color="#3a3a3a", width=6)
            button.grid(row=i + 1, column=0, sticky="w", pady=(5, 0), padx=(0, 0))  # 5 pixels padding above and below
            
            toggle = customtkinter.CTkCheckBox(frame, text=name, checkbox_width=12, checkbox_height=12)
            toggle.grid(row=i + 1, column=1, sticky="w", pady=(5, 0), padx=(0, 0))  # Align with the button and same padding
            
            goodName = name.replace(" ", "").lower()
            setattr(self, f"{goodName}Toggle", toggle)  # Dynamically set toggle attribute

    def createDocuWidgets(self, frame):
        # Define documentation application options with invalid links
        docuApps = [
            ("", lambda: None),  # Placeholder that does nothing
            ("Adobe Reader DC", lambda: webbrowser.open('https://www.adobe.com/acrobat/pdf-reader.html', new=2)),
        ]

        for i, (name, command) in enumerate(docuApps):
            button = customtkinter.CTkButton(frame, text=f"[?]", font=("Arial", 11, "bold"), text_color="aqua", command=command, fg_color="#3a3a3a", hover_color="#3a3a3a", width=6)
            button.grid(row=i + 1, column=0, sticky="w", pady=(5, 0), padx=(0, 0))  # 5 pixels padding above and below
            
            toggle = customtkinter.CTkCheckBox(frame, text=name, checkbox_width=12, checkbox_height=12)
            toggle.grid(row=i + 1, column=1, sticky="w", pady=(5, 0), padx=(0, 0))  # Align with the button and same padding
            
            goodName = name.replace(" ", "").lower()
            setattr(self, f"{goodName}Toggle", toggle)  # Dynamically set toggle attribute

    def parseDownloads(self):
        # Disable the button before executing commands
        self.parseButton.configure(state=tk.DISABLED)
        distro = self.detectDistro()  # Detect the operating system distribution
        commands = self.buildCommands(distro)  # Build the commands based on selected applications

        if commands:
            # Create a new window for terminal output
            terminalWindow = tk.Toplevel(self)
            terminalWindow.title("Terminal Output")
            terminalWindow.geometry("600x400")

            terminalOutput = scrolledtext.ScrolledText(terminalWindow, wrap=tk.WORD, background="#323232", foreground="#ffffff")
            terminalOutput.pack(expand=True, fill='both')

            process = subprocess.Popen(commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

            # Function to read the output asynchronously
            def readOutput(file, queue, lock):
                while True:
                    line = file.readline()
                    if not line:
                        break
                    with lock:
                        queue.put(line)

            # Set up queues and lock
            stdoutQueue = queue.Queue()
            stderrQueue = queue.Queue()
            outputLock = threading.Lock()

            # Create file event handlers
            stdoutHandler = threading.Thread(target=readOutput, args=(process.stdout, stdoutQueue, outputLock))
            stderrHandler = threading.Thread(target=readOutput, args=(process.stderr, stderrQueue, outputLock))

            # Start file event handlers
            stdoutHandler.start()
            stderrHandler.start()

            def checkOutput():
                with outputLock:
                    while not stdoutQueue.empty():
                        terminalOutput.configure(state='normal')
                        terminalOutput.insert(tk.END, stdoutQueue.get())
                        terminalOutput.yview(tk.END)  # Scroll to the bottom
                        terminalOutput.configure(state='disabled')

                    while not stderrQueue.empty():
                        terminalOutput.configure(state='normal')
                        terminalOutput.insert(tk.END, stderrQueue.get())
                        terminalOutput.yview(tk.END)  # Scroll to the bottom
                        terminalOutput.configure(state='disabled')

                if process.poll() is None:
                    # The process is still running, so check again after a short delay
                    terminalOutput.after(100, checkOutput)
                else:
                    # Command finished, clean up
                    stdoutHandler.join()
                    stderrHandler.join()

                    # Enable the button after command execution is complete
                    self.parseButton.configure(state=tk.NORMAL)

            # Start checking for output
            checkOutput()

    def detectDistro(self):
        if platform.system().lower() == "linux":
            with open('/etc/os-release') as f:
                osInfo = f.read().lower()
                if 'arch' in osInfo or 'manjaro' in osInfo or 'endeavouros' in osInfo:
                    return "arch"
                elif 'fedora' in osInfo or 'centos' in osInfo or 'rhel' in osInfo:
                    return "fedora"
                elif 'debian' in osInfo or 'ubuntu' in osInfo or 'linuxmint' in osInfo:
                    return "debian"
        elif platform.system().lower() == "windows":
            return "windows"
        elif platform.system().lower() == "darwin":
            return "macos"
        else:
            return "unknown"

    def buildCommands(self, distro):
        commands = ""
        def appendCommand(toggle, commandWin, commandMac, commandArch):
            nonlocal commands
            if toggle.get() == 1:
                commands += commandWin if distro == "windows" else commandMac if distro == "macos" else commandArch if distro == "arch" else ""
            
        # Example commands for brew and winget
        if distro == "macos":
            commands += "brew install --display-times "  # Initial command for Homebrew on macOS
        elif distro == "windows":
            commands += "winget install --accept-package-agreements --accept-source-agreements "  # Initial command for winget on Windows
        elif distro == "arch":
            commands += "yay -S --noconfirm "  # Initial command for yay on Arch

        # Internet Browsers
        appendCommand(self.arcToggle, "TheBrowserCompany.Arc ", "arc ", "")
        appendCommand(self.braveToggle, "Brave.Brave ", "brave-browser ", "brave-browser ")
        appendCommand(self.chromeToggle, "Google.Chrome ", "google-chrome ", "google-chrome ")
        appendCommand(self.chromiumToggle, "Hibbiki.Chromium ", "chromium ", "chromium ")
        appendCommand(self.edgeToggle, "Microsoft.Edge ", "microsoft-edge ", "microsoft-edge-stable-bin ")
        appendCommand(self.firefoxToggle, "Mozilla.Firefox ", "firefox ", "firefox ")
        appendCommand(self.floorpToggle, "Ablaze.Floorp ", "floorp ", "floorp-bin ")
        appendCommand(self.librewolfToggle, "LibreWolf.LibreWolf ", "librewolf ", "librewolf-bin ")
        appendCommand(self.operaToggle, "Opera.Opera ", "opera ", "opera ")
        appendCommand(self.operagxToggle, "Opera.OperaGX ", "opera-gx ", "")
        appendCommand(self.orionToggle, "", "orion ", "")
        appendCommand(self.thoriumToggle, "Alex313031.Thorium.AVX2 ", "alex313031-thorium ", "thorium-browser-bin ")
        appendCommand(self.torToggle, "TorProject.TorBrowser ", "tor-browser ", "tor-browser-bin ")
        appendCommand(self.ungoogledchromiumToggle, "eloston.ungoogled-chromium ", "eloston-chromium ", "ungoogled-chromium-bin ")
        appendCommand(self.vivaldiToggle, "VivaldiTechnologies.Vivaldi ", "vivaldi ", "vivaldi ")
        appendCommand(self.zenToggle, "Zen-Team.Zen-Browser ", "zen-browser ", "zen-browser-bin ")

        # Communications
        appendCommand(self.discordToggle, "Discord.Discord ", "discord ", "discord ")
        appendCommand(self.ferdiumToggle, "Ferdium.Ferdium ", "ferdium ", "ferdium-bin ")
        appendCommand(self.guildedToggle, "Guilded.Guilded ", "guilded ", "guilded ")
        appendCommand(self.teamspeakToggle, "TeamSpeakSystems.TeamSpeakClient ", "teamspeak-client ", "teamspeak ")
        appendCommand(self.textualToggle, "", "textual", "")
        appendCommand(self.googlechatToggle, "squalou.google-chat-linux ", "", "google-chat-linux-bin ")
        appendCommand(self.chatterinoToggle, "ChatterinoTeam.Chatterino ", "chatterino ", "chatterino2-bin ")
        appendCommand(self.hexchatToggle, "HexChat.HexChat ", "", "hexchat")
        appendCommand(self.jamiToggle, "SFLinux.Jami ", "jami ", "jami ")
        appendCommand(self.linphoneToggle, "BelledonneCommunications.Linphone ", "linphone ", "linphone-desktop ")
        appendCommand(self.elementToggle, "Element.Element ", "element ", "element-desktop ")
        appendCommand(self.sessionToggle, "Oxen.Session ", "session ", "session-desktop-bin ")
        appendCommand(self.signalToggle, "OpenWhisperSystems.Signal ", "signal ", "signal-desktop-beta-bin ")
        appendCommand(self.skypeToggle, "Microsoft.Skype ", "skype ", "skypeforlinux-bin ")
        appendCommand(self.slackToggle, "SlackTechnologies.Slack ", "slack ", "slack-desktop ")
        appendCommand(self.teamsToggle, "Microsoft.Teams ", "microsoft-teams ", "teams ")
        appendCommand(self.telegramToggle, "Telegram.TelegramDesktop ", "telegram ", "telegram-desktop ")
        appendCommand(self.thunderbirdToggle, "Mozilla..ThThunderbird ", "thunderbird ", "thunderbird ")

        # Documents
        appendCommand(self.adobereaderdcToggle, "Adobe.Acrobat.Reader.64-bit ", "adobe-acrobat-reader ", "")

        # Development
        appendCommand(self.gitToggle, "Git.Git ", "git ", "git ")

        return commands

    def updateAllApps(self):
        # Disable the button before executing commands
        self.updateButton.configure(state=tk.DISABLED)

        # Create a new window for terminal output
        terminalWindow = tk.Toplevel(self)
        terminalWindow.title("Terminal Output")
        terminalWindow.geometry("600x400")

        terminalOutput = scrolledtext.ScrolledText(terminalWindow, wrap=tk.WORD, background="#323232", foreground="#ffffff")
        terminalOutput.pack(expand=True, fill='both')

        # Command to run
        if platform.system().lower() == "darwin":
            command = "brew upgrade"
        elif platform.system().lower() == "windows":
            command = "winget upgrade --all"
        else:
            command = "yay -Syyuu"

        # Run the command in a separate thread
        def run_command():
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

            # Function to read the output asynchronously
            def read_output(file, queue):
                while True:
                    line = file.readline()
                    if not line:
                        break
                    queue.put(line)

            # Set up queues
            stdoutQueue = queue.Queue()
            stderrQueue = queue.Queue()

            # Create threads to read stdout and stderr
            stdoutHandler = threading.Thread(target=read_output, args=(process.stdout, stdoutQueue))
            stderrHandler = threading.Thread(target=read_output, args=(process.stderr, stderrQueue))

            # Start the threads
            stdoutHandler.start()
            stderrHandler.start()

            # Check for output
            def check_output():
                while not stdoutQueue.empty():
                    terminalOutput.configure(state='normal')
                    terminalOutput.insert(tk.END, stdoutQueue.get())
                    terminalOutput.yview(tk.END)  # Scroll to the bottom
                    terminalOutput.configure(state='disabled')

                while not stderrQueue.empty():
                    terminalOutput.configure(state='normal')
                    terminalOutput.insert(tk.END, stderrQueue.get())
                    terminalOutput.yview(tk.END)  # Scroll to the bottom
                    terminalOutput.configure(state='disabled')

                if process.poll() is None:
                    terminalOutput.after(100, check_output)  # Check again after a short delay
                else:
                    stdoutHandler.join()
                    stderrHandler.join()
                    self.updateButton.configure(state=tk.NORMAL)  # Re-enable the button after command execution

            # Start checking for output
            check_output()

        # Start the command in a separate thread
        threading.Thread(target=run_command).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()