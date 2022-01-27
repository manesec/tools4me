print("""
 ▄▀▀▄ ▄▀▄  ▄▀▀█▄   ▄▀▀▄ ▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▄▄▄▄  
█  █ ▀  █ ▐ ▄▀ ▀▄ █  █ █ █ ▐  ▄▀   ▐ █ █   ▐ ▐  ▄▀   ▐ █ █    ▌ 
▐  █    █   █▄▄▄█ ▐  █  ▀█   █▄▄▄▄▄     ▀▄     █▄▄▄▄▄  ▐ █      
  █    █   ▄▀   █   █   █    █    ▌  ▀▄   █    █    ▌    █      
▄▀   ▄▀   █   ▄▀  ▄▀   █    ▄▀▄▄▄▄    █▀▀▀    ▄▀▄▄▄▄    ▄▀▄▄▄▄▀ 
█    █    ▐   ▐   █    ▐    █    ▐    ▐       █    ▐   █     ▐  
▐    ▐            ▐         ▐                 ▐        ▐        
                Download Tools - Tools4me by Mane.
                           Version: 0.1.1
                https://github.com/manesec/tools4me
---------------------------------------------------------------""")
import os

# Mkdir 
os.system("rm -rfy Linux")
os.system("rm -rf Windows")
os.system("rm -rf Tools")
os.system("rm -rf Additions")
os.system("rm -rf Wordlists")
os.mkdir("Linux")
os.mkdir("Windows")
os.mkdir("Tools")
os.mkdir("Additions")
os.mkdir("Wordlists")

print(" :: Apt pre-install ::")
os.system("sudo apt update && sudo apt -y install python3-pip neo4j gobuster zaproxy hashcat nikto")

print("---------------------------------------------------------------")
print(" :: Updating ExplotDB ::")
os.system("sudo apt update && sudo apt -y install exploitdb && sudo searchsploit -u")

print("---------------------------------------------------------------")
print(" :: Setting up zaproxy ::")
print("[!] Set up for zaproxy it need to take a long time.")
import pexpect,time

print("[>] Installing all additions ...")
zap = pexpect.spawn('zaproxy -addoninstallall -daemon',timeout=60*10)
zap.expect("ZAP is now listening")
print(" -  Waiting for 5 second ...")
time.sleep(5)
zap.kill(9)

print("[>] Updating all additions ...")
zap = pexpect.spawn('zaproxy -addonupdate -daemon',timeout=60*10)
zap.expect("ZAP is now listening")
print(" -  Waiting for 5 second ...")
time.sleep(5)
zap.kill(9)

print("[>] Uninstall Non-compatible additions ...")
zap = pexpect.spawn('zaproxy -addonuninstall browserView -daemon',timeout=60*10)
zap.expect("ZAP is now listening")
print(" -  Waiting for 5 second ...")
time.sleep(5)
zap.kill(9)

print("---------------------------------------------------------------")
print(" :: pip pre install ::")
print("[>] Getting pwncat-cs ...")
os.system("sudo pip3 install pwncat-cs")

print("---------------------------------------------------------------")
print(" :: Installing Tools ::")

print("[>] Getting nmapAutomator ...")
os.system("wget https://raw.githubusercontent.com/21y4d/nmapAutomator/master/nmapAutomator.sh --quiet -O Tools/nmapAutomator.sh")

print("[>] Getting Godzilla ...")
os.system("wget https://github.com/BeichenDream/Godzilla/releases/latest/download/godzilla.jar --quiet -O Tools/godzilla.jar")

print("[>] Getting Behinder ...")
os.mkdir("tmp")
os.chdir("tmp")
os.system("wget https://github.com/rebeyond/Behinder/releases/download/Behinder_v3.0_Beta_11_for_tools/Behinder_v3.0_Beta_11.t00ls.zip --quiet -O Behinder.zip")
os.system("wget https://gluonhq.com/download/javafx-11-0-2-sdk-linux/ --quiet -O javafx.zip")
os.system("unzip Behinder.zip")
os.system("unzip javafx.zip")
os.remove("Behinder.zip")
os.remove("javafx.zip")
os.system("mv javafx-sdk-*/lib .")
os.system("rm -rf javafx-sdk-*")
os.chdir("..")
os.system("mv tmp Tools/Behinder")


print("---------------------------------------------------------------")
print(" :: Installing For Windows Tools ::")

print("[>] Getting BloodHound ...")
os.chdir("Windows")
os.system("wget https://github.com/BloodHoundAD/BloodHound/releases/download/4.0.3/BloodHound-linux-x64.zip -O BloodHound-linux-x64.zip")
os.system("unzip BloodHound-linux-x64.zip")
os.system("rm -rf BloodHound-linux-x64.zip")
os.chdir("..")

print("[>] Getting PowerSploit ...")
os.chdir("Windows")
os.system("git clone https://github.com/PowerShellMafia/PowerSploit.git PowerSoloit_dev -b dev")
os.system("git clone https://github.com/PowerShellMafia/PowerSploit.git PowerSoloit_master -b master")
os.chdir("..")

print("[>] Getting evil-winrm ...")
os.chdir("Windows")
os.system("git clone https://github.com/Hackplayers/evil-winrm.git")
os.chdir("..")

print("[>] Getting nishang ...")
os.chdir("Windows")
os.system("git clone https://github.com/samratashok/nishang.git")
os.chdir("..")

print("[>] Getting python impacket ...")
os.chdir("Windows")
os.system("git clone https://github.com/SecureAuthCorp/impacket.git")
os.chdir("impacket")
os.system("pip3 install .")
os.chdir("..")
os.chdir("..")

print("[>] Getting winPEAS ...")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/download/refs%2Fpull%2F260%2Fmerge/winPEAS.bat --quiet -O Windows/winPEAS.bat")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/download/refs%2Fpull%2F260%2Fmerge/winPEASany.exe  --quiet -O Windows/winPEASany.exe")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/download/refs%2Fpull%2F260%2Fmerge/winPEASany_ofs.exe --quiet -O Windows/winPEASany_ofs.exe")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/download/refs%2Fpull%2F260%2Fmerge/winPEASx64.exe --quiet -O Windows/winPEASx64.exe")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/download/refs%2Fpull%2F260%2Fmerge/winPEASx64_ofs.exe --quiet -O Windows/winPEASx64_ofs.exe")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/download/refs%2Fpull%2F260%2Fmerge/winPEASx86.exe --quiet -O Windows/winPEASx86.exe")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/download/refs%2Fpull%2F260%2Fmerge/winPEASx86_ofs.exe --quiet -O Windows/winPEASx86_ofs.exe")

print("[>] Getting mimikatz ...")
os.mkdir("tmp")
os.chdir("tmp")
os.system("wget https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20210810-2/mimikatz_trunk.zip --quiet -O mimikatz.zip")
os.system("unzip mimikatz.zip")
os.system("rm mimikatz.zip")
os.chdir("..")
os.system("mv tmp Windows/mimikatz")

print("---------------------------------------------------------------")
print(" :: Installing For Linux Tools ::")

print("[>] Getting pspy ...")
os.system("wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy32 --quiet -O Linux/pspy32")
os.system("wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy64 --quiet -O Linux/pspy64")
os.system("wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy32s --quiet -O Linux/pspy32s")
os.system("wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy64s --quiet -O Linux/pspy64s")

print("[>] Getting LinPEAS ...")
os.system("wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh --quiet -O Linux/linpeas.sh")

print("[>] Getting LinuxSmartEnumeration ...")
os.system("wget https://raw.githubusercontent.com/diego-treitos/linux-smart-enumeration/master/lse.sh --quiet -O Linux/lse.sh")

print("[>] Getting LinEnum ...")
os.system("wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh --quiet -O Linux/LinEnum.sh")

print("[>] Getting unix-privesc-check ...")
os.chdir("Linux")
os.system("git clone https://github.com/pentestmonkey/unix-privesc-check.git")
os.chdir("..")

print("[>] Getting SUDO_KILLER ...")
os.chdir("Linux")
os.system("git clone https://github.com/TH3xACE/SUDO_KILLER.git")
os.chdir("..")

print("---------------------------------------------------------------")
print(" :: Installing Additions Tools ::")

print("[>] Getting BeRoot ...")
os.chdir("Additions")
os.system("git clone https://github.com/AlessandroZ/BeRoot.git")
os.chdir("..")

print("[>] Getting big Webshell ...")
os.chdir("Additions")
os.system("git clone https://github.com/tennc/webshell.git")
os.chdir("webshell")
os.system("git submodule update --init --recursive")
os.chdir("..")
os.chdir("..")

print("---------------------------------------------------------------")
print(" :: Installing Word list ::")

print("[>] Getting secLists ...")
os.chdir("Wordlists")
os.system("git clone https://github.com/danielmiessler/SecLists.git")
os.chdir("..")

print("[>] Getting rockyou.txt ...")
os.system("wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -O Wordlists/rockyou.txt")


print("-------------------------- Total ------------------------------")
os.system("du -h --max-depth=1 .")
print("\nDone! -- by manesec.")