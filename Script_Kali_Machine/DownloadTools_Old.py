# List slow update ..
Optional_Installation = {
    # Update ExploitDB
    "EXPLOITDB" : True,

    # Install ZAP
    # It have some bug in old kali linux, if you are running old kali linux please disable it.
    "ZAP" : False,

    # Install DBeaver
    "DBEAVER" : True,

    # Install Big Webshell Collection ~ 0.84 GByte
    # I think kali buildin webshell just enough.
    # URL: https://github.com/tennc/webshell.git 
    "BIG_WEBSHELL" : False,

    # Install Dictionary-Of-Pentesting (like seclist) ~ 1.2 GByte
    "DOP" : False,

}

####################################################################### 
################################# END ################################# 
####################################################################### 

print("""
 ▄▀▀▄ ▄▀▄  ▄▀▀█▄   ▄▀▀▄ ▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▄▄▄▄  
█  █ ▀  █ ▐ ▄▀ ▀▄ █  █ █ █ ▐  ▄▀   ▐ █ █   ▐ ▐  ▄▀   ▐ █ █    ▌ 
▐  █    █   █▄▄▄█ ▐  █  ▀█   █▄▄▄▄▄     ▀▄     █▄▄▄▄▄  ▐ █      
  █    █   ▄▀   █   █   █    █    ▌  ▀▄   █    █    ▌    █      
▄▀   ▄▀   █   ▄▀  ▄▀   █    ▄▀▄▄▄▄    █▀▀▀    ▄▀▄▄▄▄    ▄▀▄▄▄▄▀ 
█    █    ▐   ▐   █    ▐    █    ▐    ▐       █    ▐   █     ▐  
▐    ▐            ▐         ▐                 ▐        ▐     
            Download Tools on AMD64 - Tools4me by Mane.
                           Version: 20220301
                https://github.com/manesec/tools4me
---------------------------------------------------------------""")
import os

# Mkdir 
os.system("rm -rf Linux")
os.system("rm -rf Windows")
os.system("rm -rf Tools")
os.system("rm -rf Additions")
os.system("rm -rf Wordlists")
os.system("rm -rf Tools4mane")

os.mkdir("Linux")
os.mkdir("Windows")
os.mkdir("Tools")
os.mkdir("Additions")
os.mkdir("Wordlists")

print(" :: Apt pre-install ::")
os.system("sudo apt update && sudo apt -y install python3-pip neo4j gobuster zaproxy hashcat nikto feroxbuster")

print("---------------------------------------------------------------")
if Optional_Installation["EXPLOITDB"]:
    print(" :: Updating ExploitDB And MSF ::")
    os.system("sudo apt update && sudo apt -y install exploitdb metasploit-framework && sudo searchsploit -u")
    os.system("sudo msfdb reinit")
print("---------------------------------------------------------------")
if Optional_Installation["ZAP"] : 
    print(" :: Setting up zaproxy ::")
    print("[!] Set up for zaproxy it need to take a long time.")
    import pexpect,time

    print("[>] Installing all additions ...")
    zap = pexpect.spawn('zaproxy -addoninstallall -daemon -port 12345',timeout=60*10)
    zap.expect("ZAP is now listening")
    print(" -  Waiting for 5 second ...")
    time.sleep(5)
    zap.kill(9)

    print("[>] Updating all additions ...")
    zap = pexpect.spawn('zaproxy -addonupdate -daemon -port 12345',timeout=60*10)
    zap.expect("ZAP is now listening")
    print(" -  Waiting for 5 second ...")
    time.sleep(5)
    zap.kill(9)

    print("[>] Uninstall Non-compatible additions ...")
    zap = pexpect.spawn('zaproxy -addonuninstall browserView -daemon -port 12345',timeout=60*10)
    zap.expect("ZAP is now listening")
    print(" -  Waiting for 5 second ...")
    time.sleep(5)
    zap.kill(9)

if Optional_Installation["DBEAVER"]:
    print(" :: Setting up DBeaver ::")
    os.mkdir("tmp")
    os.chdir("tmp")
    os.system("wget https://github.com/dbeaver/dbeaver/releases/download/21.3.5/dbeaver-ce_21.3.5_amd64.deb -O dbeaver.deb")
    os.system("sudo dpkg -i dbeaver.deb")
    os.chdir("..")
    os.system("rm -rf tmp")
    
print("---------------------------------------------------------------")
print(" :: pip pre install ::")
print("[>] Getting pwncat-cs ...")
os.system("sudo pip3 install pwncat-cs")

print("---------------------------------------------------------------")
print(" :: Installing Tools ::")

print("[>] Getting tools4mane ...")
os.system("git clone https://github.com/manesec/tools4mane.git Tools4mane")

print("[>] Getting nmapAutomator ...")
os.system("wget https://raw.githubusercontent.com/21y4d/nmapAutomator/master/nmapAutomator.sh --quiet -O Tools/nmapAutomator.sh")

print("[>] Getting Godzilla ...")
os.system("wget https://github.com/BeichenDream/Godzilla/releases/latest/download/godzilla.jar --quiet -O Tools/godzilla.jar")

print("[>] Getting Chisel ...")
os.chdir("Tools")
os.mkdir("Chisel")
os.chdir("Chisel")
os.system("wget https://github.com/jpillora/chisel/releases/latest/download/chisel_1.7.7_linux_386.gz --quiet -O chisel_linux_386.gz")
os.system("wget https://github.com/jpillora/chisel/releases/latest/download/chisel_1.7.7_linux_amd64.gz --quiet -O chisel_linux_amd64.gz")
os.system("wget https://github.com/jpillora/chisel/releases/latest/download/chisel_1.7.7_windows_386.gz --quiet -O chisel_windows_386.gz")
os.system("wget https://github.com/jpillora/chisel/releases/latest/download/chisel_1.7.7_windows_amd64.gz --quiet -O chisel_windows_amd64.gz")
os.system("gzip -d *.gz")
os.chdir("..")
os.chdir("..")

print("---------------------------------------------------------------")
print(" :: Installing For Windows Tools ::")

print("[>] Getting Beroot ...")
os.chdir("Windows")
os.system("wget https://github.com/AlessandroZ/BeRoot/releases/latest/download/beRoot.zip -O beRoot.zip --quiet")
os.system("unzip beRoot.zip")
os.system("rm -r beRoot.zip")
os.chdir("..")

print("[>] Getting BloodHound ...")
os.chdir("Windows")
os.system("wget https://github.com/BloodHoundAD/BloodHound/releases/latest/download/BloodHound-linux-x64.zip -O BloodHound-linux-x64.zip")
os.system("unzip BloodHound-linux-x64.zip")
os.system("rm -rf BloodHound-linux-x64.zip")
os.chdir("..")

print("[>] Getting PowerSploit ...")
os.chdir("Windows")
os.system("git clone https://github.com/PowerShellMafia/PowerSploit.git PowerSoloit_dev -b dev")
os.system("git clone https://github.com/PowerShellMafia/PowerSploit.git PowerSoloit_master -b master")
os.chdir("..")

print("[>] Getting Evil-winrm ...")
os.chdir("Windows")
os.system("git clone https://github.com/Hackplayers/evil-winrm.git Evil-winrm")
os.system("sudo gem install evil-winrm")
os.chdir("..")

print("[>] Getting Nishang ...")
os.chdir("Windows")
os.system("git clone https://github.com/samratashok/nishang.git Nishang")
os.chdir("..")

print("[>] Getting RedTeamPowershellScripts ...")
os.chdir("Windows")
os.system("git clone https://github.com/Mr-Un1k0d3r/RedTeamPowershellScripts.git RedTeamPowershellScripts")
os.chdir("..")

print("[>] Getting gosecretsdump ...")
os.chdir("Windows")
os.system("wget https://github.com/C-Sto/gosecretsdump/releases/download/v0.3.1/gosecretsdump_win_v0.3.1.exe --quiet")
os.chdir("..")

print("[>] Getting python Impacket ...")
os.chdir("Windows")
os.system("git clone https://github.com/SecureAuthCorp/impacket.git Impacket")
os.chdir("Impacket")
os.system("pip3 install .")
os.chdir("..")
os.chdir("..")

print("[>] Getting WinPEAS ...")
os.chdir("Windows")
os.mkdir("WinPEAS")
os.chdir("WinPEAS")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEAS.bat --quiet -O winPEAS.bat")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEASany.exe  --quiet -O winPEASany.exe")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEASany_ofs.exe --quiet -O winPEASany_ofs.exe")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEASx64.exe --quiet -O winPEASx64.exe")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEASx64_ofs.exe --quiet -O winPEASx64_ofs.exe")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEASx86.exe --quiet -O winPEASx86.exe")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEASx86_ofs.exe --quiet -O winPEASx86_ofs.exe")
os.chdir("..")
os.chdir("..")

print("[>] Getting Mimikatz ...")
os.mkdir("tmp")
os.chdir("tmp")
os.system("wget https://github.com/gentilkiwi/mimikatz/releases/latest/download/mimikatz_trunk.zip --quiet -O mimikatz.zip")
os.system("unzip mimikatz.zip")
os.system("rm mimikatz.zip")
os.chdir("..")
os.system("mv tmp Windows/Mimikatz")

print("[>] Getting AD Collector ...")
os.chdir("Windows")
os.system("wget https://github.com/dev-2null/ADCollector/releases/download/Release/ADCollector.exe --quiet")
os.chdir("..")

print("[>] Getting ADACLScanner  ...")
os.chdir("Windows")
os.system("wget https://github.com/canix1/ADACLScanner/releases/latest/download/ADACLScan.ps1 --quiet")
os.chdir("..")


print("[>] Getting WinPwn ...")
os.chdir("Windows")
os.system("wget https://github.com/S3cur3Th1sSh1t/WinPwn/releases/latest/download/WinPwn.exe --quiet")
os.system("wget https://github.com/S3cur3Th1sSh1t/WinPwn/releases/latest/download/WinPwn.ps1 --quiet")
os.chdir("..")

print("[>] Getting juicy-potato ...")
os.chdir("Windows")
os.system("wget https://github.com/ohpe/juicy-potato/releases/latest/download/JuicyPotato.exe --quiet")
os.chdir("..")

print("[>] Getting Lovely-Potato ...")
os.chdir("Windows")
os.system("git clone https://github.com/TsukiCTF/Lovely-Potato.git")
os.chdir("..")

print("[>] Getting PowerUpSQL ...")
os.chdir("Windows")
os.system("wget https://raw.githubusercontent.com/NetSPI/PowerUpSQL/master/PowerUpSQL.ps1 -O PowerUpSQL.ps1 --quiet")
os.chdir("..")

print("[>] Getting kerbrute ...")
os.chdir("Windows")
os.system("git clone https://github.com/TarlogicSecurity/kerbrute")
os.chdir("kerbrute")
os.system("pip3 install -r requirements.txt")
os.chdir("..")
os.chdir("..")

print("[>] Getting Sharp Collection ...")
os.chdir("Windows")
os.system("git clone https://github.com/Flangvik/SharpCollection.git SharpCollection")
os.chdir("..")

print("[>] Getting Sharp ADModule ...")
os.chdir("Windows")
os.system("git clone https://github.com/samratashok/ADModule.git ADModule")
os.chdir("..")

print("[>] Getting ADCS.ps1 ...")
os.chdir("Windows")
os.system("wget https://raw.githubusercontent.com/cfalta/PoshADCS/master/ADCS.ps1 -O ADCS.ps1 --quiet")
os.chdir("..")

print("[>] Getting Privesc.ps1 ...")
os.chdir("Windows")
os.system("wget https://raw.githubusercontent.com/enjoiz/Privesc/master/privesc.ps1 -O Privesc.ps1 --quiet")
os.chdir("..")


print("[>] Getting SharpView ...")
os.chdir("Windows")
os.system("wget https://github.com/tevora-threat/SharpView/raw/master/Compiled/SharpView.exe -O SharpView.exe --quiet")
os.chdir("..")

print("[>] Getting NetSPI PowerShell Scripts ...")
os.chdir("Windows")
os.system("git clone https://github.com/NetSPI/PowerShell.git NetSPIPowerShell")
os.chdir("..")


print("---------------------------------------------------------------")
print(" :: Installing For Linux Tools ::")

print("[>] Getting pspy ...")
os.chdir("Linux")
os.mkdir("Pspy")
os.chdir("Pspy")
os.system("wget https://github.com/DominicBreuker/pspy/releases/latest/download/pspy32 --quiet -O pspy32")
os.system("wget https://github.com/DominicBreuker/pspy/releases/latest/download/pspy64 --quiet -O pspy64")
os.system("wget https://github.com/DominicBreuker/pspy/releases/latest/download/pspy32s --quiet -O pspy32s")
os.system("wget https://github.com/DominicBreuker/pspy/releases/latest/download/pspy64s --quiet -O pspy64s")
os.chdir("..")
os.chdir("..")

print("[>] Getting LinPEAS ...")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh --quiet -O Linux/linpeas.sh")

print("[>] Getting LinuxSmartEnumeration ...")
os.system("wget https://raw.githubusercontent.com/diego-treitos/linux-smart-enumeration/master/lse.sh --quiet -O Linux/lse.sh")

print("[>] Getting LinEnum ...")
os.system("wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh --quiet -O Linux/LinEnum.sh")

print("[>] Getting unix-privesc-check ...")
os.chdir("Linux")
os.system("git clone https://github.com/pentestmonkey/unix-privesc-check.git Unix-privesc-check")
os.system("tar -cf Unix-privesc-check.tar.gz Unix-privesc-check")
os.system("rm -rf Unix-privesc-check")
os.chdir("..")

print("[>] Getting SUDO_KILLER ...")
os.chdir("Linux")
os.system("git clone https://github.com/TH3xACE/SUDO_KILLER.git Sudo_Killer")
os.system("tar -cf Sudo_Killer.tar.gz Sudo_Killer")
os.system("rm -rf Sudo_Killer")
os.chdir("..")

print("---------------------------------------------------------------")
print(" :: Installing Additions Tools ::")

if Optional_Installation["BIG_WEBSHELL"] :
    print("[>] Getting Big Webshell Collection ...")
    os.chdir("Additions")
    os.system("git clone https://github.com/tennc/webshell.git")
    os.chdir("webshell")
    os.system("git submodule update --init --recursive")
    os.chdir("..")
    os.chdir("..")

print("[>] Getting Hack-browser ...")
os.chdir("Additions")
os.mkdir("Hack-browser")
os.chdir("Hack-browser")
os.system("wget https://github.com/moonD4rk/HackBrowserData/releases/latest/download/hack-browser-data--linux-amd64.zip --quiet ")
os.system("wget https://github.com/moonD4rk/HackBrowserData/releases/latest/download/hack-browser-data--linux-386.zip --quiet ")
os.system("wget https://github.com/moonD4rk/HackBrowserData/releases/latest/download/hack-browser-data--windows-32bit.zip --quiet ")
os.system("wget https://github.com/moonD4rk/HackBrowserData/releases/latest/download/hack-browser-data--windows-64bit.zip --quiet ")
os.system("unzip hack-browser-data--linux-amd64.zip")
os.system("unzip hack-browser-data--linux-386.zip")
os.system("unzip hack-browser-data--windows-32bit.zip")
os.system("unzip hack-browser-data--windows-64bit.zip")
os.remove("hack-browser-data--linux-amd64.zip")
os.remove("hack-browser-data--linux-386.zip")  
os.remove("hack-browser-data--windows-32bit.zip")
os.remove("hack-browser-data--windows-64bit.zip")
os.chdir("..")
os.chdir("..")

print("---------------------------------------------------------------")
print(" :: Installing Wordlists ::")

print("[>] Getting secLists ...")
os.chdir("Wordlists")
os.system("git clone https://github.com/danielmiessler/SecLists.git")
os.chdir("..")

print("[>] Getting Auto_Wordlists ...")
os.chdir("Wordlists")
os.system("git clone https://github.com/carlospolop/Auto_Wordlists.git")
os.chdir("..")

print("[>] Getting rockyou.txt ...")
os.system("wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -O Wordlists/rockyou.txt")

if Optional_Installation["DOP"]:
    print("[>] Getting Dictionary-Of-Pentesting ...")
    os.chdir("Wordlists")
    os.system("git clone https://github.com/insightglacier/Dictionary-Of-Pentesting.git")
    os.chdir("..")

print("[>] Getting Update.sh")
os.system("wget https://raw.githubusercontent.com/manesec/tools4me/main/Script_Kali_Machine/Update.sh --quiet")
os.system("chmod u+x Update.sh")
print("If you want to update \"DownloadTools.py\" just run ./Update.sh ")

print("-------------------------- Total ------------------------------")
os.system("du -h --max-depth=1 .")
print("\nDone! -- by manesec.")
