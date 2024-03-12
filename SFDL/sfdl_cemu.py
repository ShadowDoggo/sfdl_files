# SFDL for Cemu. Copyright (c) 2022 Shadow Doggo.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import configparser
import urllib.request
import webbrowser
import shutil
import requests
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)  # Enable DPI awareness (I trust Windows to not mess up the GUI).

thisVersion = "v1.0b_devbeta2"

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.geometry("450x390")
        self.master.resizable(False, False)
        self.master.title("SFDL for Cemu")
        self.infoWindow = None
        self.settingsWindow = None
        self.isFuncActive = False
        try:
            self.master.iconbitmap("./sfdl/assets/icon.ico")  # (os.path.join(sys._MEIPASS, "./icon.ico")) for pyinstaller.
        except:
            pass
        self.readconfig()

    def readconfig(self):
        config = configparser.ConfigParser()
        config.read("./sfdl/config.cfg")
        section = config["config"]
        self.mlcLocation = section["mlc_location"]
        self.regionType = section["region"]
        self.status = section["status"]
        self.backup = section["backup"]
        self.mystery = section["mystery"]
        self.accountID = section["accountID"]
        self.localfesID = section["local_fest_version"]
        try:
            tree = ET.parse("./settings.xml")
            self.cemuSettings = tree.getroot()
        except:
            self.cemuSettings = None

        if self.mlcLocation == "Auto":
            if self.cemuSettings is not None:
                mlcBase = self.cemuSettings[2].text
                if mlcBase is not None:
                    self.mlcPath = mlcBase.replace("\\", "/" )
                else:
                    self.mlcPath = "./mlc01"
            else:
                messagebox.showwarning(title="SFDL for Cemu", message="Unable to read Cemu settings. The MLC path will be set to default. Check the troubleshooting guide for more info.")
                config = configparser.ConfigParser()
                config.add_section("config")
                config.set("config", "region", self.regionType)
                config.set("config", "mlc_location", "Default")
                config.set("config", "mlc_path", "./mlc01")
                config.set("config", "backup", self.backup)
                config.set("config", "mystery", self.mystery)
                config.set("config", "accountID", self.accountID)
                config.set("config", "status", self.status)
                config.set("config", "local_fest_version", self.localfesID)
                with open("./sfdl/config.cfg", "w") as configfile:
                    config.write(configfile)
                restart()
        else:
            self.mlcPath = (section["mlc_path"]).replace("\\", "/")
        regions = 0  # Crude way of detecting mutliple regions.
        if self.regionType == "Auto":
            if os.path.isdir(f"{self.mlcPath}/usr/boss/00050000/10176900/"):
                regions += 1
                region = "USA"
            if os.path.isdir(f"{self.mlcPath}/usr/boss/00050000/10176a00/"):
                regions += 1
                region = "EUR"
            if os.path.isdir(f"{self.mlcPath}/usr/boss/00050000/10162b00/"):
                regions += 1
                region = "JPN"
            if 0 < regions < 2:
                self.region = region
            elif regions == 0:
                messagebox.showwarning(title="SFDL for Cemu", message="Unable to automatically detect region. The MLC path may be incorrect. Check the troubleshooting guide for more info.")
                self.region = "USA"
            else:
                messagebox.showwarning(title="SFDL for Cemu", message="More than one region detected. Please set the desired region manually in the settings.")
                self.region = "USA"
        else:
            self.region = self.regionType
        try:
            self.fesImg = urllib.request.urlopen("https://github.com/ShadowDoggo/sfdl_files/raw/main/Files/image.png").read()
            API = requests.get(url="https://splatfest.discloud.app/api/splatfest-info/lastest")  # Get fest data from API.
            fesData = API.json()
            self.fesID = str(fesData["id"])
            teamAlpha = fesData["team_alpha"]
            teamBravo = fesData["team_bravo"]
            self.fesStart = (fesData["start_time"].replace("-", ".")).split("T", 1)[0]
            self.fesEnd = (fesData["end_time"].replace("-", ".")).split("T", 1)[0]
            self.fesTheme = teamAlpha + " vs. " + teamBravo
        except Exception as exception:
            messagebox.showwarning(title="SFDL for Cemu", message=f"Unable to get splatfest data. {exception}. Check the troubleshooting guide for more info.")
            config = configparser.ConfigParser()
            config.read("./sfdl/assets/fest.cfg")  # os.path.join(sys._MEIPASS, "./fest.cfg").
            section = config["splatfest"]
            self.fesTheme = section["theme"]
            self.fesStart = section["start"]
            self.fesEnd = section["end"]
            self.fesID = section["version"]
        if self.fesID != self.localfesID:
            config = configparser.ConfigParser()
            config.add_section("config")
            config.set("config", "region", self.regionType)
            config.set("config", "mlc_location", self.mlcLocation)
            config.set("config", "mlc_path", self.mlcPath)
            config.set("config", "backup", self.backup)
            config.set("config", "mystery", self.mystery)
            config.set("config", "accountID", self.accountID)
            config.set("config", "status", "Not installed")
            config.set("config", "local_fest_version", self.fesID)
            with open("./sfdl/config.cfg", "w") as configfile:
                config.write(configfile)
            restart()

        self.mainwindow()

    def mainwindow(self):
        self.var0 = tk.StringVar()  # Install button.
        self.var1 = tk.StringVar()  # Uninstall button.
        self.var0.set("Install Files")
        self.var1.set("Uninstall Files")
        self.frame = tk.Frame(self.master, width=450, height=390)
        try:
            self.img = tk.PhotoImage(data=self.fesImg)
        except:
            self.img = tk.PhotoImage(file="./sfdl/assets/image.png")  # os.path.join(sys._MEIPASS, "./image.png").
        self.canvas = tk.Canvas(self.frame, width=384, height=216)
        self.label0 = ttk.Label(self.frame, text=self.fesTheme)
        self.label1 = ttk.Label(self.frame, text=f"Starts: {self.fesStart}")
        self.label2 = ttk.Label(self.frame, text=f"Ends: {self.fesEnd}")
        self.label3 = ttk.Label(self.frame, text=f"Splatfest ID: {self.fesID}")
        self.label4 = ttk.Label(self.frame, text=f"App version: {thisVersion}")
        self.label5 = ttk.Label(self.frame, text=f"Status: {self.status}")
        self.button0 = ttk.Button(self.frame, width=15, textvariable=self.var0, command=lambda: Thread(target=self.installmsg).start())
        self.button1 = ttk.Button(self.frame, width=15, textvariable=self.var1, command=lambda: Thread(target=self.uninstallmsg).start())
        self.button2 = ttk.Button(self.frame, width=3, text="🛈", command=self.info)
        self.button3 = ttk.Button(self.frame, width=3, text="⚙", command=self.settings)
        self.frame.pack()
        self.canvas.place(y=170, relx=0.5, anchor=tk.CENTER)
        self.canvas.create_image(0,0, anchor=tk.NW, image=self.img)
        self.label0.place(y=20, relx=0.5, anchor=tk.CENTER)
        self.label1.place(x=35, y=30)  # The positions for these need to be fixed.
        self.label2.place(x=300, y=30)
        self.label3.place(y=120, relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.label4.place(y=140, relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.label5.place(y=100, relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.button0.place(y=170, x=-65, relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.button1.place(y=170, x=65, relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.button2.place(y=170, x=166, relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.button3.place(y=170, x=200, relx=0.5, rely=0.5, anchor=tk.CENTER)

    def installmsg(self):
        if not self.isFuncActive:
            if self.status == "Not installed":
                self.install()
            else:
                self.master.bell()
                messageboxBox = messagebox.askquestion(title="SFDL for Cemu", message="The files are already installed.\nDo you wish to reinstall them?")
                if messageboxBox == "yes":
                    self.install()
        else:
            return

    def uninstallmsg(self):
        if not self.isFuncActive:
            if self.status == "Installed":
                self.remove()
            else:
                messagebox.showwarning(title="SFDL for Cemu", message="The files aren't installed.")
        else:
            return

    def info(self):
        if self.infoWindow is None:
            self.infoWindow = tk.Toplevel(self.master)
            self.infoWindow.protocol("WM_DELETE_WINDOW", lambda: self.closewindow(0))
            self.infoWindow.geometry("400x180")
            self.infoWindow.resizable(False, False)
            self.infoWindow.title("SFDL for Cemu")
            self.infoWindow.lift()
            self.infoWindow.focus()
            try:
                self.infoWindow.iconbitmap("./sfdl/assets/icon.ico")  # os.path.join(sys._MEIPASS, "./icon.ico").
            except:
                pass
            self.infoWindow.bell()
            self.iFrame = ttk.LabelFrame(self.infoWindow, text="Info", width=390, height=170)
            self.iLabel0 = ttk.Label(self.iFrame, text=f"SFDL for Cemu {thisVersion}\n© 2022 Shadow Doggo. All rights reserved.\nThis program comes with ABSOLUTELY NO WARRANTY.\nThe splatfest files and artwork are made by the\nSplatfestival team.")
            self.iButton0 = ttk.Button(self.iFrame, text="Splatfestival Discord", width=21, command=lambda:
                                       webbrowser.open("https://discord.gg/grMSxZf", new=0))
            self.iButton1 = ttk.Button(self.iFrame, text="Troubleshooting Guide", width=21, command=lambda:
                                       webbrowser.open("https://github.com/ShadowDoggo/sfdl_files/blob/main/SFDL/Troubleshooting.md", new=0))
            self.iFrame.pack(pady=5, padx=5)
            self.iLabel0.place(y=25, x=185, relx=0.5, rely=0.5, anchor=tk.SE)
            self.iButton0.place(y=50, x=-90, relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.iButton1.place(y=50, x=90, relx=0.5, rely=0.5, anchor=tk.CENTER)
        else:
            self.infoWindow.lift()
            self.infoWindow.focus()

    def settings(self):
        if self.settingsWindow is None:
            self.settingsWindow = tk.Toplevel(self.master)
            self.settingsWindow.protocol("WM_DELETE_WINDOW", lambda: self.closewindow(1))
            self.settingsWindow.geometry("240x380")
            self.settingsWindow.resizable(False, False)
            self.settingsWindow.title("SFDL for Cemu")
            self.settingsWindow.lift()
            self.settingsWindow.focus()
            try:
                self.settingsWindow.iconbitmap("./sfdl/assets/icon.ico")  # os.path.join(sys._MEIPASS, "./icon.ico").
            except:
                pass
            self.cVar0 = tk.StringVar()  # Region combobox.
            self.cVar1 = tk.StringVar()  # MLC Location combobox.
            self.cVar2 = tk.StringVar()  # MLC Path entry.
            self.cVar3 = tk.StringVar()  # MLC Path label.
            self.cVar4 = tk.StringVar()  # Backup checkbutton.
            self.cVar5 = tk.StringVar()  # Account ID combobox.
            self.cVar6 = tk.StringVar()  # Mystery checkbutton.
            self.sFrame = ttk.Labelframe(self.settingsWindow, text="Settings", width=230, height=370)
            self.sLabel0 = ttk.Label(self.sFrame, text="Region")
            self.sLabel1 = ttk.Label(self.sFrame, text="MLC Location")
            self.sLabel2 = ttk.Label(self.sFrame, textvariable=self.cVar3)
            self.sLabel3 = ttk.Label(self.sFrame, text="Account ID")
            self.sButton0 = ttk.Button(self.sFrame, text="Apply", width=10, command=self.makeconfig)
            self.sButton1 = ttk.Button(self.sFrame, text="Browse", width=10, command=self.pathselect)
            self.scBox0 = ttk.Combobox(self.sFrame, textvariable=self.cVar0, width=5)
            self.scBox1 = ttk.Combobox(self.sFrame, textvariable=self.cVar1, width=10)
            self.scBox2 = ttk.Combobox(self.sFrame, textvariable=self.cVar5, width=10)
            self.sEntry0 = ttk.Entry(self.sFrame, textvariable=self.cVar2, width=25)
            self.scButton0 = ttk.Checkbutton(self.sFrame, text="Backup save & memory\nsearcher file", variable=self.cVar4,
                                             onvalue="true", offvalue="false", command=self.hide2)
            self.scButton1 = ttk.Checkbutton(self.sFrame, text="Mystery setting", variable=self.cVar6, onvalue="true",
                                             offvalue="false")
            self.sFrame.pack(pady=5, padx=5)
            self.sLabel0.place(x=5, y=0)
            self.sLabel1.place(x=5, y=50)
            self.sLabel2.place(x=5, y=100)
            self.sLabel3.place(x=5, y=195)
            self.sButton0.place(y=320, relx=0.5, anchor=tk.CENTER)
            self.sButton1.place(x=7, y=155)
            self.scBox0.place(x=7, y=25)
            self.scBox1.place(x=7, y=75)
            self.scBox2.place(x=7, y=235)
            self.sEntry0.place(x=7, y=125)
            self.scButton0.place(x=7, y=185)
            self.scButton1.place(x=7, y=265)
            self.scBox0["values"] = ("Auto", "USA", "EUR", "JPN")
            self.scBox0["state"] = "readonly"
            self.scBox1["values"] = ("Auto", "Default", "Custom")
            self.scBox1["state"] = "readonly"
            self.scBox2["values"] = ("80000001", "80000002", "80000003", "80000004", "80000005", "80000006", "80000007",
                                     "80000008", "80000009", "80000010", "80000011", "80000012", "80000013", "80000014",
                                     "80000015", "80000016")  # Why would you need more than 16 accounts?
            self.scBox2["state"] = "readonly"
            self.scBox1.bind("<<ComboboxSelected>>", self.hide)
            if self.mlcLocation != "Custom" or self.mlcPath is None:
                self.mlcFolder = "Unset"
            else:
                self.mlcFolder = self.mlcPath
            if self.mlcLocation == "Default":  # This handles the visibility of the widgets.
                self.cVar2.set(self.mlcFolder)
                self.cVar3.set("Custom MLC Path:")
                self.sButton1.config(state="disabled")
                self.sLabel2.config(state="disabled")
                self.sEntry0.config(state="disabled")
            elif self.mlcLocation == "Auto":
                if self.mlcPath == "./mlc01":
                    self.cVar2.set("Default")
                else:
                    self.cVar2.set(self.mlcPath)
                self.cVar3.set("Detected MLC Path:")
                self.sButton1.config(state="disabled")
                self.sLabel2.config(state="normal")
                self.sEntry0.config(state="readonly")
                self.cVar0.set(self.regionType)
            else:
                self.cVar3.set("Custom MLC Path:")
                self.cVar2.set(self.mlcPath)
                self.sButton1.config(state="normal")
                self.sLabel2.config(state="normal")
                self.sEntry0.config(state="normal")
            if self.backup == "false":
                self.scBox2.config(state="disabled")
                self.sLabel3.config(state="disabled")
            else:
                self.scBox2.config(state="readonly")
                self.sLabel3.config(state="normal")
            self.cVar0.set(self.regionType)
            self.cVar1.set(self.mlcLocation)
            self.cVar5.set(self.accountID)
            self.cVar4.set(self.backup)
            self.cVar6.set(self.mystery)
        else:
            self.settingsWindow.lift()
            self.settingsWindow.focus()

    def hide(self):  # This probably shouldn't exist.
        if self.scBox1.get() == "Custom":
            self.cVar3.set("Custom MLC Path:")
            self.sButton1.config(state="normal")
            self.sLabel2.config(state="normal")
            self.sEntry0.config(state="normal")
            self.cVar2.set(self.mlcFolder)
        elif self.scBox1.get() == "Auto":
            self.cVar3.set("Detected MLC Path:")
            self.sButton1.config(state="disabled")
            self.sLabel2.config(state="normal")
            self.sEntry0.config(state="readonly")
            if self.cemuSettings is not None:
                mlcBase = self.cemuSettings[2].text
                if mlcBase is not None:
                    mlc = mlcBase.replace("\\", "/")
                    self.cVar2.set(mlc)
                else:
                    self.cVar2.set("Default")
            else:
                messagebox.showerror(title="SFDL for Cemu", message="Unable to read Cemu settings. Check the troubleshooting guide for more info.", parent=self.settingsWindow)
        else:
            self.sButton1.config(state="disabled")
            self.sLabel2.config(state="disabled")
            self.sEntry0.config(state="disabled")

    def hide2(self):
        if self.cVar4.get() == "false":
            self.scBox2.config(state="disabled")
            self.sLabel3.config(state="disabled")
        else:
            self.scBox2.config(state="readonly")
            self.sLabel3.config(state="normal")

    def makeconfig(self):
        if self.scBox1.get() == "Custom":
            mlc = self.mlcFolder
            pathType = "Custom"
        elif self.scBox1.get() == "Auto":  # Auto path detection.
            if self.cemuSettings is not None:
                mlcBase = self.cemuSettings[2].text
                if mlcBase is not None:
                    mlc = mlcBase.replace("\\", "/")
                    self.mlcFolder = mlc
                else:
                    mlc = "./mlc01"
                    self.mlcFolder = "Default"
                pathType = "Auto"
            else:
                messagebox.showerror(title="SFDL for Cemu", message="Unable to read Cemu settings. Check the troubleshooting guide for more info.", parent=self.settingsWindow)
                return
        else:
            mlc = "./mlc01"
            self.mlcFolder = "Default"
            pathType = "Default"
        if not self.mlcFolder or self.mlcFolder == "Unset":
            messagebox.showwarning(title="SFDL for Cemu", message="Please set the MLC path.", parent=self.settingsWindow)
            self.pathselect()
            self.makeconfig()
        config = configparser.ConfigParser()
        config.add_section("config")
        config.set("config", "region", self.scBox0.get())
        config.set("config", "mlc_location", pathType)
        config.set("config", "mlc_path", mlc)
        config.set("config", "backup", self.cVar4.get())
        config.set("config", "mystery", self.cVar6.get())
        config.set("config", "accountID", self.scBox2.get())
        config.set("config", "status", self.status)
        config.set("config", "local_fest_version", self.localfesID)
        with open("./sfdl/config.cfg", "w") as configfile:
            config.write(configfile)
        restart()

    def pathselect(self):
        self.mlcFolder = filedialog.askdirectory(initialdir="./", title="Select mlc01 folder")
        self.cVar2.set(self.mlcFolder)
        self.settingsWindow.lift()
        self.settingsWindow.focus()

    def install(self):  # Code readability? Never heard of her.
        if not self.isFuncActive:
            self.isFuncActive = True
        try:
            self.var0.set("Installing...")
            if self.region == "USA":
                if self.backup == "true":
                    shutil.copyfile(f"{self.mlcPath}/usr/save/00050000/10176900/user/{self.accountID}/save.dat",
                                    "./sfdl/save.dat.bak")
                    if os.path.isfile("./memorySearcher/0005000010176900.ini"):
                        shutil.copyfile("./memorySearcher/0005000010176900.ini", "./sfdl/0005000010176900.ini.bak")
                file0 = "https://github.com/Sheldon10095/Splatfestival_StaffFiles/raw/main/FestFiles/00000543"
                urllib.request.urlretrieve(file0, f"{self.mlcPath}/usr/boss/00050000/10176900/user/common/data/optdat2/00000543")
                file1 = "https://github.com/Sheldon10095/Splatfestival_StaffFiles/raw/main/FestFiles/00000544"
                urllib.request.urlretrieve(file1, f"{self.mlcPath}/usr/boss/00050000/10176900/user/common/data/optdat2/00000544")
                file2 = "https://github.com/Sheldon10095/Splatfestival_StaffFiles/raw/main/FestFiles/00000545"
                urllib.request.urlretrieve(file2, f"{self.mlcPath}/usr/boss/00050000/10176900/user/common/data/optdat2/00000545")
                file3 = "https://github.com/ShadowDoggo/sfdl_files/raw/main/Files/Extra/0005000010176900.ini"
                urllib.request.urlretrieve(file3, "./memorySearcher/0005000010176900.ini")
            elif self.region == "EUR":
                if self.backup == "true":
                    shutil.copyfile(f"{self.mlcPath}/usr/save/00050000/10176a00/user/{self.accountID}/save.dat",
                                    "./sfdl/save.dat.bak")
                    if os.path.isfile("./memorySearcher/0005000010176a00.ini"):
                        shutil.copyfile("./memorySearcher/0005000010176a00.ini", "./sfdl/0005000010176a00.ini.bak")
                file0 = "https://github.com/Sheldon10095/Splatfestival_StaffFiles/raw/main/FestFiles/00000543"
                urllib.request.urlretrieve(file0, f"{self.mlcPath}/usr/boss/00050000/10176a00/user/common/data/optdat2/0000054e")
                file1 = "https://github.com/Sheldon10095/Splatfestival_StaffFiles/raw/main/FestFiles/00000544"
                urllib.request.urlretrieve(file1, f"{self.mlcPath}/usr/boss/00050000/10176a00/user/common/data/optdat2/0000054d")
                file2 = "https://github.com/Sheldon10095/Splatfestival_StaffFiles/raw/main/FestFiles/00000545"
                urllib.request.urlretrieve(file2, f"{self.mlcPath}/usr/boss/00050000/10176a00/user/common/data/optdat2/0000054c")
                file3 = "https://github.com/ShadowDoggo/sfdl_files/raw/main/Files/Extra/0005000010176900.ini"
                urllib.request.urlretrieve(file3, "./memorySearcher/0005000010176a00.ini")
            elif self.region == "JPN":
                if self.backup == "true":
                    shutil.copyfile(f"{self.mlcPath}/usr/save/00050000/10162b00/user/{self.accountID}/save.dat",
                                    "./sfdl/save.dat.bak")
                    if os.path.isfile("./memorySearcher/0005000010162b00.ini"):
                        shutil.copyfile("./memorySearcher/0005000010162b00.ini", "./sfdl/0005000010162b00.ini.bak")
                file0 = "https://github.com/Sheldon10095/Splatfestival_StaffFiles/raw/main/FestFiles/00000543"
                urllib.request.urlretrieve(file0, f"{self.mlcPath}/usr/boss/00050000/10162b00/user/common/data/optdat2/000005d3")
                file1 = "https://github.com/Sheldon10095/Splatfestival_StaffFiles/raw/main/FestFiles/00000544"
                urllib.request.urlretrieve(file1, f"{self.mlcPath}/usr/boss/00050000/10162b00/user/common/data/optdat2/000005d2")
                file2 = "https://github.com/Sheldon10095/Splatfestival_StaffFiles/raw/main/FestFiles/00000545"
                urllib.request.urlretrieve(file2, f"{self.mlcPath}/usr/boss/00050000/10162b00/user/common/data/optdat2/000005d4")
                file3 = "https://github.com/ShadowDoggo/sfdl_files/raw/main/Files/Extra/0005000010176900.ini"
                urllib.request.urlretrieve(file3, "./memorySearcher/0005000010162b00.ini")
            # Graphic pack files.
            fileList = urllib.request.urlopen("https://raw.githubusercontent.com/ShadowDoggo/sfdl_files/main/SFDL/file_list.txt")
            fileListSheldon = urllib.request.urlopen("https://raw.githubusercontent.com/Sheldon10095/Splatfestival_StaffFiles/main/Other/FileList")
            if not os.path.isdir("./graphicPacks/Splatoon_CustomSplatfest"):
                os.mkdir("./graphicPacks/Splatoon_CustomSplatfest")
            for line in fileList:
                path = (line.decode('utf-8')).strip("\n")
                urllib.request.urlretrieve(f"https://github.com/ShadowDoggo/sfdl_files/raw/main/Files/Extra/{path}",
                                           f"./graphicPacks/Splatoon_CustomSplatfest/{path}")
            for line in fileListSheldon:
                path = (((line.decode('utf-8')).replace("SFDL_cafiine/00050000FFFFFFFF/CustomSplatfest/", "")).strip("\n")).split("sd:/", 1)[1]
                if not os.path.isdir(f"./graphicPacks/Splatoon_CustomSplatfest/{os.path.dirname(path)}"):
                    os.makedirs(f"./graphicPacks/Splatoon_CustomSplatfest/{os.path.dirname(path)}")
                path_no_content = path.replace("content/", "")
                urllib.request.urlretrieve(f"https://github.com/Sheldon10095/Splatfestival_StaffFiles/raw/main/ExtraFiles/{path_no_content}",
                                           f"./graphicPacks/Splatoon_CustomSplatfest/{path}")
            fileList = urllib.request.urlopen("https://raw.githubusercontent.com/ShadowDoggo/sfdl_files/main/SFDL/file_list.txt")
            fileListSheldon = urllib.request.urlopen("https://raw.githubusercontent.com/Sheldon10095/Splatfestival_StaffFiles/main/Other/FileList")
            for line in fileList:
                path = (line.decode('utf-8')).strip("\n")
                if not os.path.isfile(f"./graphicPacks/Splatoon_CustomSplatfest/{path}"):
                    raise Exception(f"Failed to download file:'./graphicPacks/Splatoon_CustomSplatfest/{path}'. Try installing the files again")
            for line in fileListSheldon:
                path = (((line.decode('utf-8')).replace("SFDL_cafiine/00050000FFFFFFFF/CustomSplatfest/", "")).strip("\n")).split("sd:/", 1)[1]
                if not os.path.isfile(f"./graphicPacks/Splatoon_CustomSplatfest/{path}"):
                    raise Exception(f"Failed to download file:'./graphicPacks/Splatoon_CustomSplatfest/{path}'. Try installing the files again")
            if self.mystery == "true":
                myst_list = urllib.request.urlopen("https://raw.githubusercontent.com/ShadowDoggo/sfdl_files/main/SFDL/mystery_list.txt")
                for line in myst_list:
                    path = (line.decode('utf-8')).strip("\n")
                    urllib.request.urlretrieve(f"https://github.com/ShadowDoggo/sfdl_files/raw/main/Files/Extra/{path}",
                                               f"./graphicPacks/Splatoon_CustomSplatfest/{path}")
            self.var0.set("Install Files")
            config = configparser.ConfigParser()
            config.add_section("config")
            config.set("config", "region", self.regionType)
            config.set("config", "mlc_location", self.mlcLocation)
            config.set("config", "mlc_path", self.mlcPath)
            config.set("config", "backup", self.backup)
            config.set("config", "mystery", self.mystery)
            config.set("config", "accountID", self.accountID)
            config.set("config", "status", "Installed")
            config.set("config", "local_fest_version", self.localfesID)
            with open("./sfdl/config.cfg", "w") as configfile:
                config.write(configfile)
            self.isFuncActive = False
            messagebox.showinfo(title="SFDL for Cemu", message="Files successfuly installed.")
            restart()
        except Exception as exception:
            self.isFuncActive = False
            self.var0.set("Install Files")
            messagebox.showerror(title="SFDL for Cemu", message=f"Install failed. {exception}. Check the troubleshooting guide for more info.")

    def remove(self):
        if not self.isFuncActive:
            self.isFuncActive = True
        try:
            self.var1.set("Uninstalling...")
            if self.region == "USA":
                os.remove(f"{self.mlcPath}/usr/boss/00050000/10176900/user/common/data/optdat2/00000543")
                os.remove(f"{self.mlcPath}/usr/boss/00050000/10176900/user/common/data/optdat2/00000544")
                os.remove(f"{self.mlcPath}/usr/boss/00050000/10176900/user/common/data/optdat2/00000545")
                if os.path.isfile("./memorySearcher/0005000010176900.ini"):
                    os.remove("./memorySearcher/0005000010176900.ini")
            elif self.region == "EUR":
                os.remove(f"{self.mlcPath}/usr/boss/00050000/10176a00/user/common/data/optdat2/0000054c")
                os.remove(f"{self.mlcPath}/usr/boss/00050000/10176a00/user/common/data/optdat2/0000054d")
                os.remove(f"{self.mlcPath}/usr/boss/00050000/10176a00/user/common/data/optdat2/0000054e")
                if os.path.isfile("./memorySearcher/0005000010176a00.ini"):
                    os.remove("./memorySearcher/0005000010176a00.ini")
            elif self.region == "JPN":
                os.remove(f"{self.mlcPath}/usr/boss/00050000/10162b00/user/common/data/optdat2/000005d2")
                os.remove(f"{self.mlcPath}/usr/boss/00050000/10162b00/user/common/data/optdat2/000005d3")
                os.remove(f"{self.mlcPath}/usr/boss/00050000/10162b00/user/common/data/optdat2/000005d4")
                if os.path.isfile("./memorySearcher/0005000010162b00.ini"):
                    os.remove("./memorySearcher/0005000010162b00.ini")
            shutil.rmtree("./graphicPacks/Splatoon_CustomSplatfest")
            self.var1.set("Uninstall Files")
            config = configparser.ConfigParser()
            config.add_section("config")
            config.set("config", "region", self.regionType)
            config.set("config", "mlc_location", self.mlcLocation)
            config.set("config", "mlc_path", self.mlcPath)
            config.set("config", "backup", self.backup)
            config.set("config", "mystery", self.mystery)
            config.set("config", "accountID", self.accountID)
            config.set("config", "status", "Not installed")
            config.set("config", "local_fest_version", self.localfesID)
            with open("./sfdl/config.cfg", "w") as configfile:
                config.write(configfile)
            self.isFuncActive = False
            messagebox.showinfo(title="SFDL for Cemu", message="Files successfuly uninstalled.")
            restart()
        except Exception as exception:
            self.isFuncActive = False
            self.var1.set("Uninstall Files")
            messagebox.showerror(title="SFDL for Cemu", message=f"Uninstall failed. {exception}. Check the troubleshooting guide for more info.")

    def closewindow(self, window):
        if window == 0:
            self.infoWindow.destroy()
            self.infoWindow = None
        elif window == 1:
            self.settingsWindow.destroy()
            self.settingsWindow = None

def restart():
    os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)

if not os.path.isdir("./sfdl"):
    try:
        os.mkdir("./sfdl")
    except:
        pass

if not os.path.isfile("./sfdl/config.cfg"):
    try:
        tree = ET.parse("./settings.xml")
        root = tree.getroot()
        mlcPath1_s = root[2].text
        if mlcPath1_s is not None:
            mlcPath_s = mlcPath1_s.replace("\\", "/")
        else:
            mlcPath_s = "./mlc01"
        pathType_s = "Auto"
    except:
        mlcPath_s = "./mlc01"
        pathType_s = "Default"
        messagebox.showwarning(title="SFDL for Cemu", message="Unable to read Cemu settings. The MLC path will be set to default. Check the troubleshooting guide for more info.")
    config = configparser.ConfigParser()
    config.add_section("config")
    config.set("config", "region", "Auto")
    config.set("config", "mlc_location", pathType_s)
    config.set("config", "mlc_path", mlcPath_s)
    config.set("config", "backup", "true")
    config.set("config", "mystery", "false")
    config.set("config", "accountID", "80000001")
    config.set("config", "status", "Not installed")
    config.set("config", "local_fest_version", "00")
    try:
        with open("./sfdl/config.cfg", "w") as configfile:
            config.write(configfile)
    except:
        messagebox.showerror(title="SFDL for Cemu", message="Unable to create config file. If the app is in a folder that requires admin permissions to write files (e.g. Program Files, Program Files(x86), ProgramData), you'll need to run the app as an admin.")
        sys.exit()

# try:
#     latestVer = urllib.request.urlopen("https://github.com/ShadowDoggo/sfdl_files/raw/main/SFDL/latest_version.txt").read().decode("utf-8")
# except Exception as exception:
#     messagebox.showerror(title="SFDL for Cemu", message=f"Unable to check for updates. {exception}. Check the troubleshooting guide for more info.")
#     latestVer = thisVersion
# if latestVer != thisVersion:
#     messagebox.showwarning(title="SFDL for Cemu", message="A new version is available. Please download the latest version.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()
