# Cemu Instructions

How to use SFDL for Cemu.

If you're encountering an error or any of the steps are unclear, check the [Troubleshooting guide](https://github.com/ShadowDoggo/sfdl_files/blob/main/SFDL/Troubleshooting.md) or ask for help in the assistance channel.

## Online files

In order to participate in the splatfests, you'll need to dump the online files from your Wii U using [this](https://cemu.cfw.guide/online-play.html) guide.

## Downloads

#### <ins>Note: If you're updating from a pre-1.0b version, delete the old config.cfg file.</ins>

### Windows:

Available as a standalone executable and python script.

The Python version requires Python 3.10 or newer and the [requests](https://pypi.org/project/requests/) module.

[Executable](https://github.com/ShadowDoggo/sfdl_files/raw/main/SFDL/sfdl_for_cemu_win_exec.zip)

[Python script](https://github.com/ShadowDoggo/sfdl_files/raw/main/SFDL/sfdl_for_cemu_win.zip)

Extract the .exe/.py file and the sfdl folder to the root of your Cemu folder (where Cemu.exe is).

Defender or certain browsers may falsely detect the executable as a virus.

### Linux (beta):

Distros tested so far: Ubuntu, Mint, Manjaro.

Available only as Python script. Requires Python 3.10 or newer and the [requests](https://pypi.org/project/requests/) module.

[Python script](https://github.com/ShadowDoggo/sfdl_files/raw/main/SFDL/sfdl_for_cemu_linux.zip)

## Installing the Splatfest

### Step 1:

Run SFDL for Cemu.

<img src="./img/ins1.png" width="400"/>

### Step 2:

Click the Install Files button. If nothing went wrong, the app will install the splatfest and restart.

<img src="./img/ins3.png" width="400"/>

## After installing

### Step 1:

Open Cemu, right click on Splatoon and select Edit graphic packs.

<img src="./img/ins4.png" width="400"/>

Under the Mods section, enable the Custom Splatfest graphic pack.

<img src="./img/ins5.png" width="500"/>

### Step 2:

Launch Splatoon. The splatfest should now be active.

<img src="./img/ins6.png" width="500"/>

### Step 3:

Before going into the lobby, open Tools > Memory searcher, make sure that the power reset entries are enabled and leave the window open.

<img src="./img/ins7.png" width="400"/>

You can now participate in splatfest matches! Get your splatfest team role and head over to the matchmaking channel.

<img src="./img/ins8.png" width="500"/>

## Uninstalling the Splatfest

Click the Uninstall Files button. Your game should now be back to normal.

To restore your previous memorySearcher file, copy the 00050000(titleid).ini.bak file from the sfdl folder to the memorySearcher folder and remove the .bak extension.

##

© 2022 Shadow Doggo.
