#! /bin/bash

echo "Updating DownloadTools.py ..."
rm -r DownloadTools.py
wget https://raw.githubusercontent.com/manesec/tools4me/main/Script_Kali_Machine/DownloadTools.py

echo "Done."
echo "If you want to update the tools just run \"python3 DownloadTools.py\"."
echo "Please know that it will be delete all data in this sub folder."