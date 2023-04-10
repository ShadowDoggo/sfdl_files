# Troubleshooting Guide

A small guide to help you troubleshoot common errors you may encounter in SFDL for Cemu. If you have any questions or need further assistance, you can ask for help in the server's assistance channel.

## Cemu related errors

### Splatoon causes Cemu to crash after uninstalling the splatfest files:

If you're using cemu 1.27 or older, you'll need to manually reinstall the boss files after uninstalling the splatfest. This is due to a bug that was fixed in 2.0.

You can download the clean boss files from [here](https://github.com/ShadowDoggo/sfdl_files/tree/main/Files%2FClean). Extract them to your mlc01 folder.

### Cemu.exe not found:
![](https://media.discordapp.net/attachments/735577694489804986/1048017855989436486/image.png)

This error is caused by the app not being able to find the Cemu executable. The app needs to be in the root of your Cemu folder to work properly.

### Unable to read Cemu settings:
![](https://media.discordapp.net/attachments/735577694489804986/1048018276694888448/image.png)
![](https://media.discordapp.net/attachments/735577694489804986/1048018020938813511/image.png)

This error means the app is unable to read Cemu's settings file. This is also usually caused by the app not being in the root of your Cemu folder. If it still fails, you can manually set a custom MLC path in the settings.

![](https://media.discordapp.net/attachments/735577694489804986/1048019057191944252/image.png)


## Install errors

### Install failed. No such file or directory: '/mlc01/usr/...':

![](https://media.discordapp.net/attachments/735577694489804986/1048019770907295744/image.png)

This error means the app couldn't install the splatfest files. It's commonly caused by setting the wrong region in the settings. It can also be caused by an incorrect MLC path, or the app not having write permissions to the MLC folder.

### Install failed. No such file or directory: './memorySearcher/...':

![](https://media.discordapp.net/attachments/735577694489804986/1048019956224249856/image.png)

This error means the app couldn't install the memory searcher file. It's commonly caused by setting the wrong region in the settings. It can also be caused by the app not having write permissions to the memorySearcher folder.

### Checking your region:

![](https://media.discordapp.net/attachments/735577694489804986/1048022175023636510/image.png)

You can check your game's region in Cemu's game list. Make sure it matches the region set in SFDL.

### Write permissions:

If the app is still unable to install the files, it probably means it doesn't have write permissions to the MLC and memorySearcher folders. Running the app as admin should resolve these issues.

![](https://media.discordapp.net/attachments/735577694489804986/1048023076547330058/image.png)

Alternatively you can check the permissions for both of the folders to make sure the app can write to them.

## Download errors:

### HTTP Errors:

![](https://media.discordapp.net/attachments/735577694489804986/1048024154877730816/image.png)

These errors probably mean that GitHub is down or having server issues. You'll have to wait until the issue is resolved, or install the files manually.

### Urlopen error:

![](https://media.discordapp.net/attachments/735577694489804986/1048025544056373288/err2.PNG)
![](https://media.discordapp.net/attachments/735577694489804986/1048025544517759066/err3.PNG)

These errors mean that you don't have an internet connection, or the app is blocked by your firewall/antivirus. Running the app as admin should fix this issue. If not, you'll need to whitelist it in your firewall settings.

## Other errors:

### Unable to create config file:

![](https://media.discordapp.net/attachments/735577694489804986/1048027083131072542/image.png)

This error means the app doesn't have write permissions to the Cemu folder. If it's in Program Files or any other location that requires admin permissions to write files, you'll need to run the app as admin.

![](https://media.discordapp.net/attachments/735577694489804986/1048023076547330058/image.png)

### Windows Defender protected your PC:

![](https://media.discordapp.net/attachments/735577694489804986/1048029501277356134/image.png)

The app's executable is unsigned, so Windows Defender detects it as suspicious. To get around this, click More info > Run anyway.

### Unhandled exception in script:

This is a very rare error that occurs if something went really wrong. It can be caused by a corrupted executable, weird permission issues, a broken VC++ instalation and other issues with your system. Try deleting the app's executable and running the updater again.

If the message says anything about "readconfig", delete the app's config file (sfdl/Config/config.cfg).

Example (from beta version 1.0):

![](https://media.discordapp.net/attachments/597729491615350797/1042163177414197358/image.png)

##

© 2022 Shadow Doggo.
