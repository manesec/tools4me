#! /bin/sh
FILE=PE_Pack.tar.gz
if [ ! -f $FILE ]; then
  echo "[ERR] No such file PE_Pack.tar.gz, Please download it in DownloadLinuxPECScript.sh"
  return 1
fi

echo [+] Preparing Pack ...
tar -xvf PE_Pack.tar.gz
cd tmpdata
mkdir output

echo "
---------------------------------------------------------------
 ▄▀▀▄ ▄▀▄  ▄▀▀█▄   ▄▀▀▄ ▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▄▄▄▄  
█  █ ▀  █ ▐ ▄▀ ▀▄ █  █ █ █ ▐  ▄▀   ▐ █ █   ▐ ▐  ▄▀   ▐ █ █    ▌ 
▐  █    █   █▄▄▄█ ▐  █  ▀█   █▄▄▄▄▄     ▀▄     █▄▄▄▄▄  ▐ █      
  █    █   ▄▀   █   █   █    █    ▌  ▀▄   █    █    ▌    █      
▄▀   ▄▀   █   ▄▀  ▄▀   █    ▄▀▄▄▄▄    █▀▀▀    ▄▀▄▄▄▄    ▄▀▄▄▄▄▀ 
█    █    ▐   ▐   █    ▐    █    ▐    ▐       █    ▐   █     ▐  
▐    ▐            ▐         ▐                 ▐        ▐        
              Run Linux PE Script - Tools4me by Mane.
                           Version: 0.1
                https://github.com/manesec/tools4me
---------------------------------------------------------------"

echo [+] Running LinPEAS ...
./linpeas.sh > output/linepeas 

echo [+] Running LinuxSmartEnumeration ...
./lse.sh > output/lse

echo [+] Running LinEnum ...
./LinEnum.sh -r output/LinEnum

echo [+] Running BeRoot ...
/usr/bin/python3 BeRoot/Linux/beroot.py | tee output/beroot

echo [+] Running unix-privesc-check
cd unix-privesc-check
./upc.sh > ../output/upc
cd ..

echo [+] Running sudokiller ...
./sudokiller.sh -s | tee output/sudokiller

echo [!] Done!