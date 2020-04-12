
# Authentication System

Simple authentication system using Raspberry PI 4, RFID module rc522 and Raspberry PI Camera Module

### Starting the project on Raspberry PI

Pull the repository in a folder on your Raspberry PI system.

After that you should enable the SPI interface, used by the RFID module, and the Camera interface in the Raspberry PI Configuration.

It is required to install the mfrc522 python library using the following command:

```

sudo pip3 install mfrc522

```

You can currently test the read and write capabilities for your RFID tag and record a simple video using the Raspbery Pi Camera Module.

Run each of the scripts using the python3 command and the name of the script.
