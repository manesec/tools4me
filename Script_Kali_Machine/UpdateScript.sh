#! /bin/bash

echo "Updating DownloadDocument.py ..."
rm -r DownloadDocument.py
wget https://raw.githubusercontent.com/manesec/tools4me/main/Script_Down_Documents/DownloadDocument.py

echo "Done."
echo "If you want to update the tools just run \"python3 DownloadDocument.py\"."
echo "Please know that it will be delete all data in this sub folder."