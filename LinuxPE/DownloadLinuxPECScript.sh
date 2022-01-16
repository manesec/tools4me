#! /bin/sh

echo "
 ▄▀▀▄ ▄▀▄  ▄▀▀█▄   ▄▀▀▄ ▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▄▄▄▄  
█  █ ▀  █ ▐ ▄▀ ▀▄ █  █ █ █ ▐  ▄▀   ▐ █ █   ▐ ▐  ▄▀   ▐ █ █    ▌ 
▐  █    █   █▄▄▄█ ▐  █  ▀█   █▄▄▄▄▄     ▀▄     █▄▄▄▄▄  ▐ █      
  █    █   ▄▀   █   █   █    █    ▌  ▀▄   █    █    ▌    █      
▄▀   ▄▀   █   ▄▀  ▄▀   █    ▄▀▄▄▄▄    █▀▀▀    ▄▀▄▄▄▄    ▄▀▄▄▄▄▀ 
█    █    ▐   ▐   █    ▐    █    ▐    ▐       █    ▐   █     ▐  
▐    ▐            ▐         ▐                 ▐        ▐        
        Get Linux PE Check Script - Tools4me by Mane.
                           Version: 0.1
                https://github.com/manesec/tools4me
---------------------------------------------------------------"
rm -rf tmpdata
mkdir tmpdata
cd tmpdata

echo [+] Downloading LinPEAS ...
wget "https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh" -O linpeas.sh

echo [+] Downloading LinuxSmartEnumeration ...
wget "https://raw.githubusercontent.com/diego-treitos/linux-smart-enumeration/master/lse.sh" -O lse.sh

echo [+] Downloading LinEnum ...
wget "https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh" -O LinEnum.sh

echo [+] Downloading BeRoot ...
git clone "https://github.com/AlessandroZ/BeRoot.git"
rm -rf BeRoot/Windows
rm -rf BeRoot/README.md

echo [+] Downloading unix-privesc-check ...
git clone "https://github.com/pentestmonkey/unix-privesc-check.git"
rm -rf unix-privesc-check/doc
rm -rf unix-privesc-check/tools

echo [+] Downloading sudo killer
wget "https://raw.githubusercontent.com/TH3xACE/SUDO_KILLER/master/SUDO_KILLERv2.2.1.sh" -O sudokiller.sh
wget "https://raw.githubusercontent.com/TH3xACE/SUDO_KILLER/master/cve_updatev2.sh" -O cve_updatev2.sh
wget "https://raw.githubusercontent.com/TH3xACE/SUDO_KILLER/master/cve.sudo.manual.txt" -O cve.sudo.manual.txt 
wget "https://raw.githubusercontent.com/TH3xACE/SUDO_KILLER/master/extract.sh" -O extract.sh
chmod u+x cve_updatev2.sh && ./cve_updatev2.sh

chmod u+x *.sh 

cd ..

echo [+] Copying inject files ...
cp inject/* tmpdata/*

echo [+] Making PE Pack ...
rm -rf PE_Pack.tar.gz
tar -cvf PE_Pack.tar.gz tmpdata

echo [+] Clearing the files ...
rm -rf tmpdata

echo "Done! Upload PE_Pack.tar.gz and RunLinuxPE.sh to server and run RunLinuxPE.sh"
echo "Make sure PE_Pack.tar.gz and RunLinuxPE.sh in same directory."