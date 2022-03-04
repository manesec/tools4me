import os
import sys
import json
import re
from datetime import datetime
import time
import subprocess

print("""
 ▄▀▀▄ ▄▀▄  ▄▀▀█▄   ▄▀▀▄ ▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▄▄▄▄  
█  █ ▀  █ ▐ ▄▀ ▀▄ █  █ █ █ ▐  ▄▀   ▐ █ █   ▐ ▐  ▄▀   ▐ █ █    ▌ 
▐  █    █   █▄▄▄█ ▐  █  ▀█   █▄▄▄▄▄     ▀▄     █▄▄▄▄▄  ▐ █      
  █    █   ▄▀   █   █   █    █    ▌  ▀▄   █    █    ▌    █      
▄▀   ▄▀   █   ▄▀  ▄▀   █    ▄▀▄▄▄▄    █▀▀▀    ▄▀▄▄▄▄    ▄▀▄▄▄▄▀ 
█    █    ▐   ▐   █    ▐    █    ▐    ▐       █    ▐   █     ▐  
▐    ▐            ▐         ▐                 ▐        ▐     
        Download Tools on AMD64 for kali - Tools4me by Mane.
                        Version: 20220304
                https://github.com/manesec/tools4me
---------------------------------------------------------------""")
COUNTER_RUNNING = 0
COUNTER_TOTAL = 0
LOCAL_DB_PATH = "/opt/MTools/.tools4me/"
LOCAL_DATA_PATH = "/opt/MTools/.data/"
Default_Config_URL = "https://raw.githubusercontent.com/manesec/tools4me/main/Script_Kali_Machine/config.json"

def CheckGithubAPIQuta():
    import requests
    Return_json = ""
    if CONFIG_JSON["API_TOKEN"].strip() != "":
        Return_json = requests.get("https://api.github.com/rate_limit",headers={"Authorization":"token %s" % (CONFIG_JSON["API_TOKEN"].strip())}).text
    else:
        Return_json = requests.get("https://api.github.com/rate_limit").text
    Return_json = json.loads(Return_json)
    Remaining = Return_json["rate"]["remaining"]
    Limit = Return_json["rate"]["limit"]
    Reset = (datetime.utcfromtimestamp(Return_json["rate"]["reset"]) - datetime.utcfromtimestamp(time.time())).seconds / 60
    print("[!] Github API: Remaining %s/%s, Reset in %s minutes later." % (Remaining,Limit,round(Reset,2)))

def UpdateFromGithub(URL,Locate,Branches):
    if not os.path.exists(Locate):
        os.system("git clone -b %s %s %s " % (Branches,URL,Locate))
    else:
        os.chdir(Locate)
        os.system("git pull origin %s || (git stash drop && git pull origin %s )" % (Branches,Branches))
        os.chdir("..")

def ReleasesFileSaveVersion(LName,Name,ID,UpdateAt):
    LFile = open(LOCAL_DB_PATH + "/" + LName,'w',encoding='utf-8')
    LFile.writelines(json.dumps({"name":Name,"id":ID,"updated_at":UpdateAt}))
    LFile.close()  

def ReleasesFileNeedUpdate(LName,Name,Id,UpdateAt) -> bool:
    if not os.path.exists(LOCAL_DB_PATH + "/" + LName):
        return True
    LFile = open(LOCAL_DB_PATH + "/" + LName,'r',encoding='utf-8')
    LJson = json.loads(LFile.read())
    LFile.close()
    if (LJson["name"]==Name) and (LJson["id"]==Id) and (LJson["updated_at"]==UpdateAt):
        return False
    else:
        return True

# Names -> List[re]
def ReleasesFileGetFromGithubRepo(URL,Names):
    Return_list = []
    print(" -  Searching Github Repo ...")
    import requests
    Return_json = json.loads(requests.get(URL).text)
    for f in Return_json["assets"]:
        for name in Names:
            if (re.search(name[0],f["name"])):
                print(" +  Found %s " % (f["name"]))
                Return_list.append([f["name"],f["id"],f["updated_at"],f['browser_download_url'],name[1]])
    if len(Return_list) == 0:
        print("[ERR] No found on github repo!")
        sys.exit(0)
    return Return_list

def WgetDownloadFile(url,local_path,quiet = False):
    if os.path.exists(local_path):
        os.remove(local_path)
    quiet = "--quiet" if quiet else ""
    os.system('wget "%s" %s -O "%s"' % (url,quiet,local_path))

# files -> lists = [["remote_path","local_path"]]
def ProjectGetFilesAndUpdate(repoaddr,branches,files):
    api_url = "https://api.github.com/repos/%s/git/trees/%s?recursive=1" % (repoaddr,branches)
    import requests
    Return_json = ""
    if CONFIG_JSON["API_TOKEN"].strip() != "":
        Return_json = requests.get(api_url,headers={"Authorization":"token %s" % (CONFIG_JSON["API_TOKEN"].strip())}).text
    else:
        Return_json = requests.get(api_url).text
    Return_json = json.loads(Return_json)["tree"]
    
    for afile in files:
        RemotePath,LocalPath = afile
        print(" *  Checking %s ..." % RemotePath)
        if os.path.exists(LocalPath):
            LocalPathSha = subprocess.getoutput("git hash-object %s" % (LocalPath))
            RemotePathSha = ""
            for RemoteFileObj in Return_json:
                if (RemoteFileObj["path"].strip() == RemotePath) : 
                    RemotePathSha = RemoteFileObj["sha"]
                    break
            if (RemotePathSha == ""):
                print("[ERR] No found on github repo!")
                sys.exit(0)
            if (LocalPathSha == RemotePathSha):
                print(" !  Already up to date.")
                continue
        print(" *  Updating %s ..." % (RemotePath))
        WgetDownloadFile("https://raw.githubusercontent.com/%s/%s/%s" % (repoaddr,branches,RemotePath),LocalPath,True)
        print(" +  Finish.")
        continue

if (os.getuid() != 0):
    print("Please run as ROOT !!")
    sys.exit(0)

if not os.path.exists("/opt/MTools"):
    os.mkdir("/opt/MTools")
os.chdir("/opt/MTools")

if not os.path.exists(LOCAL_DATA_PATH):
    os.mkdir(LOCAL_DATA_PATH)

if not os.path.exists(LOCAL_DB_PATH):
    os.mkdir(LOCAL_DB_PATH)

# [Pre-load]
# Maybe in next Versions.

# [check config files && Load it] 
if not os.path.exists("config.json"):
    print("[+] No config found! Downloading default conifg file ...")
    WgetDownloadFile(Default_Config_URL,"config.json")
    print("[!] Please edit /opt/MTools/config.json to select what additional packages you want to install.")
    print("    If not just run it again to be install.")
    sys.exit(0)
config_file_read_str = ""
begin_flag = False
with open('config.json','r',encoding='utf-8') as config_file_read:
    for line in config_file_read:
        line = line.strip()
        if line == "{":
            begin_flag = True
        if not begin_flag:
            continue
        if len(line)>0 and line[0] == "#":
            continue
        config_file_read_str += line + "\n"
CONFIG_JSON = json.loads(config_file_read_str)
for k in CONFIG_JSON.keys():
    if (CONFIG_JSON[k] == True):
        COUNTER_TOTAL += 1
print("[!] Loaded config file.")

CheckGithubAPIQuta()

# [check default env]
print(" :: Local environment :: ")
print("[>] Checking pip3 from apt ...")
os.system("apt update && apt install python3-pip")

print("[>] Checking pip3 Library: requests ...")
os.system("pip3 install requests")

#======================================================
# Update DB
#======================================================   
if CONFIG_JSON["Update_exploit_db"]:
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Exploit Databases ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    os.system("apt -y install exploitdb && searchsploit -u")

if CONFIG_JSON["Update_msf_db"]:
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking metasploit-framework ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    os.system("apt -y install metasploit-framework && msfdb reinit")

#======================================================
# Good Tools from apt
#======================================================   
if CONFIG_JSON["Install_Gobuster"]:
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Gobuster ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    os.system("apt -y install gobuster")

if CONFIG_JSON["Install_Feroxbuster"]:
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Feroxbuster ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    os.system("apt -y install feroxbuster")

if CONFIG_JSON["Install_Hashcat"]:
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Hashcat ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    os.system("apt -y install hashcat")

if CONFIG_JSON["Install_John"]:
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking John ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    os.system("apt -y install john")

if CONFIG_JSON["Install_Nikto"]:
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Nikto ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    os.system("apt -y install nikto")

if CONFIG_JSON["Install_ZAProxy"]:
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking ZAProxy ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
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

#======================================================
# Good Tools from pip
#======================================================    
if CONFIG_JSON["Install_PwncatCS"]:
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Pwncat-CS ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    os.system("pip3 install pwncat-cs")

#======================================================
# Some Useful Tools
#======================================================    
if CONFIG_JSON["Install_DBeaver"]:
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking DBeaver ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    LocalName = "DBeaver"
    name,id,update_at,download_url,LocalName = ReleasesFileGetFromGithubRepo("https://api.github.com/repos/dbeaver/dbeaver/releases/latest",[["dbeaver-ce_(.){0,}_amd64.deb",LocalName]])[0]
    if (ReleasesFileNeedUpdate(LocalName,name,id,update_at)):
        os.mkdir("tmp")
        os.chdir("tmp")
        print(" +  Downloading package ...")
        WgetDownloadFile(download_url,"dbeaver.deb")
        print(" +  Installing package ...")
        os.system("dpkg -i dbeaver.deb")
        ReleasesFileSaveVersion(LocalName,name,id,update_at)
        print(" +  Clearing up ...")
        os.chdir("..")
        os.system("rm -rf tmp")
        print(" !  Done.")
    else:
        print(" !  Already up to date.")

if CONFIG_JSON["Install_Marktext"]:
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Marktext ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    LocalName = "Marktext"
    name,id,update_at,download_url,LocalName = ReleasesFileGetFromGithubRepo("https://api.github.com/repos/marktext/marktext/releases/latest",[["(.){0,}-amd64.deb",LocalName]])[0]
    if (ReleasesFileNeedUpdate(LocalName,name,id,update_at)):
        os.mkdir("tmp")
        os.chdir("tmp")
        print(" +  Downloading package ...")
        WgetDownloadFile(download_url,"marktext.deb")
        print(" +  Installing package ...")
        os.system("dpkg -i marktext.deb")
        ReleasesFileSaveVersion(LocalName,name,id,update_at)
        print(" +  Clearing up ...")
        os.chdir("..")
        os.system("rm -rf tmp")
        print(" !  Done.")
    else:
        print(" !  Already up to date.")

#======================================================
# Tools
#======================================================    
if CONFIG_JSON["GET_tools4mane"]:
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking tools4mane ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/manesec/tools4mane.git","Tools4mane","main")

if CONFIG_JSON["GET_nmapAutomator"]:
    if not (os.path.exists("Tools")):
        os.mkdir("Tools")
    os.chdir("Tools")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking nmapAutomator.sh ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    files_lists = [
        ["nmapAutomator.sh","nmapAutomator.sh"]
    ]
    ProjectGetFilesAndUpdate("21y4d/nmapAutomator","master",files_lists)
    os.system("chmod 755 nmapAutomator.sh")
    os.chdir("..")

if CONFIG_JSON["GET_Godzilla"]:
    if not (os.path.exists("Tools")):
        os.mkdir("Tools")
    os.chdir("Tools")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Godzilla ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    LocalName = "Godzilla"
    name,id,update_at,download_url,LocalName = ReleasesFileGetFromGithubRepo("https://api.github.com/repos/BeichenDream/Godzilla/releases/latest",[["^godzilla\.jar$",LocalName]])[0]
    if (ReleasesFileNeedUpdate(LocalName,name,id,update_at) or (not os.path.exists("Godzilla.jar"))):
        print(" +  Downloading package ...")
        WgetDownloadFile(download_url,"Godzilla.jar")
        ReleasesFileSaveVersion(LocalName,name,id,update_at)
        print(" !  Done.")
    else:
        print(" !  Already up to date.")
    os.chdir("..")

if CONFIG_JSON["GET_Chisel"]:
    if not (os.path.exists("Tools")):
        os.mkdir("Tools")
    if not (os.path.exists("Tools/Chisel")):
        os.mkdir("Tools/Chisel")
    os.chdir("Tools/Chisel")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Chisel ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    download_files = [
        ["chisel_(.){0,}_linux_386\.gz","chisel_linux_386"],
        ["chisel_(.){0,}_linux_amd64\.gz","chisel_linux_amd64"],
        ["chisel_(.){0,}_windows_amd64\.gz","chisel_windows_amd64"],
        ["chisel_(.){0,}_windows_386\.gz","chisel_windows_386"]
    ]
    for name,id,update_at,download_url,LocalName in ReleasesFileGetFromGithubRepo("https://api.github.com/repos/jpillora/chisel/releases/latest",download_files):
        if (ReleasesFileNeedUpdate(LocalName,name,id,update_at) or (not os.path.exists(LocalName))):
            print(" +  Downloading package ...")
            WgetDownloadFile(download_url,LocalName+".gz",True)
            os.system("gzip -d %s" % (LocalName+".gz"))
            ReleasesFileSaveVersion(LocalName,name,id,update_at)
            print(" !  Done.")
        else:
            print(" !  Already up to date.")
    os.system("chmod u+x chisel_linux_386")
    os.system("chmod u+x chisel_linux_amd64")
    os.chdir("../..")

if CONFIG_JSON["Get_BlackArch_Webshell"]:
    if not (os.path.exists("Tools")):
        os.mkdir("Tools")
    os.chdir("Tools")
    if not (os.path.exists("Webshell")):
        os.mkdir("Webshell")
    os.chdir("Webshell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking BlackArch Webshell ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/BlackArch/webshells.git","BlackArch_Webshell","master")
    os.chdir("../..")
    
if CONFIG_JSON["Get_Big_Webshell"]:
    if not (os.path.exists("Tools")):
        os.mkdir("Tools")
    os.chdir("Tools")
    if not (os.path.exists("Webshell")):
        os.mkdir("Webshell")
    os.chdir("Webshell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking BlackArch Webshell ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/tennc/webshell.git","BigShellCollection","master")
    os.system("git submodule update --init --recursive")
    os.chdir("../..")


if CONFIG_JSON["Get_static_binaries"]:
    if not (os.path.exists("Tools")):
        os.mkdir("Tools")
    os.chdir("Tools")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking static-binaries ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/andrew-d/static-binaries.git","Static_binaries","master")
    os.chdir("..")
    
    
if CONFIG_JSON["Get_cupp"]:
    if not (os.path.exists("Tools")):
        os.mkdir("Tools")
    os.chdir("Tools")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking cupp ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/Mebus/cupp.git","Cupp","master")
    os.chdir("..")
    
if CONFIG_JSON["Get_krbrelayx"]:
    if not (os.path.exists("Tools")):
        os.mkdir("Tools")
    os.chdir("Tools")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Krbrelayx ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/dirkjanm/krbrelayx.git","Krbrelayx","master")
    os.chdir("..")

if CONFIG_JSON["Get_HackBrowserData"]:
    if not (os.path.exists("Tools")):
        os.mkdir("Tools")
    os.chdir("Tools")
    if not (os.path.exists("HackBrowserData")):
        os.mkdir("HackBrowserData")
    os.chdir("HackBrowserData")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking HackBrowserData ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    download_files = [
        ["^hack-browser-data--linux-386.zip$","hack-browser-data--linux-386"],
        ["^hack-browser-data--linux-amd64.zip$","hack-browser-data--linux-amd64"],
        ["^hack-browser-data--windows-32bit.zip$","hack-browser-data--windows-32bit.exe"],
        ["^hack-browser-data--windows-64bit.zip$","hack-browser-data--windows-64bit.exe"]
    ]
    for name,id,update_at,download_url,LocalName in ReleasesFileGetFromGithubRepo("https://api.github.com/repos/moonD4rk/HackBrowserData/releases/latest",download_files):
        if (ReleasesFileNeedUpdate(LocalName,name,id,update_at) or (not os.path.exists(LocalName))):
            print(" +  Downloading package ...")
            WgetDownloadFile(download_url,LocalName+".zip",True)
            os.system('unzip -o "%s"' % (LocalName + ".zip"))
            os.remove(LocalName + ".zip")
            ReleasesFileSaveVersion(LocalName,name,id,update_at)
            print(" !  Done.")
        else:
            print(" !  Already up to date.")
    os.chdir("../..")

#======================================================
# For Remote Windows
#======================================================    
if CONFIG_JSON["Get_BeRoot"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking beRoot ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    LocalName = "beRoot"
    name,id,update_at,download_url,LocalName = ReleasesFileGetFromGithubRepo("https://api.github.com/repos/AlessandroZ/BeRoot/releases/latest",[["^beRoot.zip$",LocalName]])[0]
    if (ReleasesFileNeedUpdate(LocalName,name,id,update_at) or (not os.path.exists("beRoot.exe"))):
        print(" +  Downloading package ...")
        WgetDownloadFile(download_url,"beRoot.zip",True)
        os.system("unzip beRoot.zip")
        os.remove("beRoot.zip")
        ReleasesFileSaveVersion(LocalName,name,id,update_at)
        print(" !  Done.")
    else:
        print(" !  Already up to date.")
    os.chdir("..")

if CONFIG_JSON["Get_Boodhound"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Boodhound ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    os.system("apt install -y neo4j")
    LocalName = "Boodhound"
    name,id,update_at,download_url,LocalName = ReleasesFileGetFromGithubRepo("https://api.github.com/repos/BloodHoundAD/BloodHound/releases/latest",[["^BloodHound-linux-x64\.zip$",LocalName]])[0]
    if (ReleasesFileNeedUpdate(LocalName,name,id,update_at) or (not os.path.exists("BloodHound-linux-x64"))):
        print(" +  Downloading package ...")
        WgetDownloadFile(download_url,"Boodhound.zip")
        os.system("unzip Boodhound.zip")
        os.remove("Boodhound.zip")
        ReleasesFileSaveVersion(LocalName,name,id,update_at)
        print(" !  Done.")
    else:
        print(" !  Already up to date.")
    os.chdir("..")

if CONFIG_JSON["Get_Gosecretsdump"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Gosecretsdump ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    LocalName = "Gosecretsdump"
    name,id,update_at,download_url,LocalName = ReleasesFileGetFromGithubRepo("https://api.github.com/repos/C-Sto/gosecretsdump/releases/latest",[["(.){0,}\.exe$",LocalName]])[0]
    if (ReleasesFileNeedUpdate(LocalName,name,id,update_at) or (not os.path.exists("Gosecretsdump.exe"))):
        print(" +  Downloading package ...")
        WgetDownloadFile(download_url,"Gosecretsdump.exe",True)
        ReleasesFileSaveVersion(LocalName,name,id,update_at)
        print(" !  Done.")
    else:
        print(" !  Already up to date.")
    os.chdir("..")

if CONFIG_JSON["Install_evil_winrm"]:
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking evil-winrm ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    os.system("apt install -y evil-winrm")

if CONFIG_JSON["Install_python3_impacket"]:
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking python3-impacket ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    os.system("apt install -y python3-impacket")

if CONFIG_JSON["Get_winPEAS"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    if not (os.path.exists("Windows/winPEAS")):
        os.mkdir("Windows/winPEAS")
    os.chdir("Windows/winPEAS")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking winPEAS ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    download_files = [
        ["winPEASany\.exe","winPEASany.exe"],
        ["winPEASx64\.exe","winPEASx64.exe"],
        ["winPEASx86\.exe","winPEASx86.exe"],
        ["winPEAS\.bat","winPEAS.bat"]
    ]
    for name,id,update_at,download_url,LocalName in ReleasesFileGetFromGithubRepo("https://api.github.com/repos/carlospolop/PEASS-ng/releases/latest",download_files):
        if (ReleasesFileNeedUpdate(LocalName,name,id,update_at) or (not os.path.exists(LocalName))):
            print(" +  Downloading package ...")
            WgetDownloadFile(download_url,LocalName,True)
            ReleasesFileSaveVersion(LocalName,name,id,update_at)
            print(" !  Done.")
        else:
            print(" !  Already up to date.")
    os.chdir("../..")

if CONFIG_JSON["Get_Mimikatz"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Mimikatz")):
        os.mkdir("Mimikatz")
    os.chdir("Mimikatz")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Mimikatz ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    LocalName = "Mimikatz"
    name,id,update_at,download_url,LocalName = ReleasesFileGetFromGithubRepo("https://api.github.com/repos/gentilkiwi/mimikatz/releases/latest",[["^mimikatz_trunk.zip$",LocalName]])[0]
    if (ReleasesFileNeedUpdate(LocalName,name,id,update_at) or (not os.path.exists("x64"))):
        print(" +  Downloading package ...")
        WgetDownloadFile(download_url,"mimikatz_trunk.zip",True)
        os.system("unzip mimikatz_trunk.zip")
        os.remove("mimikatz_trunk.zip")
        ReleasesFileSaveVersion(LocalName,name,id,update_at)
        print(" !  Done.")
    else:
        print(" !  Already up to date.")
    os.chdir("../..")

if CONFIG_JSON["Get_dev2null_tools"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("dev2null")):
        os.mkdir("dev2null")
    os.chdir("dev2null")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking dev2null tools set ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    tools = [
        ["https://github.com/dev-2null/ADIDNSRecords/releases/download/1.4/ADIDNSRecords.exe","ADIDNSRecords.exe"],
        ["https://github.com/dev-2null/KerberosRun/releases/download/1.0.0/KerberosRun.exe","KerberosRun.exe"],
        ["https://github.com/dev-2null/ADCollector/releases/download/Release/ADCollector.exe","ADCollector.exe"]
    ]
    for tool in tools:
        if not os.path.exists(tool[1]):
            print(" +  Downloading package ...")
            WgetDownloadFile(tool[0],tool[1],True)
    os.chdir("../..")

if CONFIG_JSON["Get_WinPwn"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("WinPwn")):
        os.mkdir("WinPwn")
    os.chdir("WinPwn")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking WinPwn ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    files_lists = [
        ["Obfus_SecurePS_WinPwn.ps1","Obfus_SecurePS_WinPwn.ps1"],
        ["Offline_WinPwn.ps1","Offline_WinPwn.ps1"],
        ["WinPwn.ps1","WinPwn.ps1"]
    ]
    ProjectGetFilesAndUpdate("S3cur3Th1sSh1t/WinPwn","master",files_lists)
    download_files = [
        ["WinPwn\.exe","WinPwn.exe"]
    ]
    for name,id,update_at,download_url,LocalName in ReleasesFileGetFromGithubRepo("https://api.github.com/repos/S3cur3Th1sSh1t/WinPwn/releases/latest",download_files):
        if (ReleasesFileNeedUpdate(LocalName,name,id,update_at) or (not os.path.exists(LocalName))):
            print(" +  Downloading package ...")
            WgetDownloadFile(download_url,LocalName,True)
            ReleasesFileSaveVersion(LocalName,name,id,update_at)
            print(" !  Done.")
        else:
            print(" !  Already up to date.")
    os.chdir("../..")

if CONFIG_JSON["Get_Chisel"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking JuicyPotato ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    download_files = [
        ["JuicyPotato\.exe","JuicyPotato.exe"],
    ]
    for name,id,update_at,download_url,LocalName in ReleasesFileGetFromGithubRepo("https://api.github.com/repos/ohpe/juicy-potato/releases/latest",download_files):
        if (ReleasesFileNeedUpdate(LocalName,name,id,update_at) or (not os.path.exists(LocalName))):
            print(" +  Downloading package ...")
            WgetDownloadFile(download_url,LocalName,True)
            ReleasesFileSaveVersion(LocalName,name,id,update_at)
            print(" !  Done.")
        else:
            print(" !  Already up to date.")
    os.chdir("..")

if CONFIG_JSON["Get_Lovely_Potato"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Lovely-Potato ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/TsukiCTF/Lovely-Potato.git","Lovely-Potato","master")
    os.chdir("..")
    
if CONFIG_JSON["Get_Kerbrute"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Kerbrute ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/TarlogicSecurity/kerbrute.git","Kerbrute","master")
    os.chdir("Kerbrute")
    os.system("pip3 install -r requirements.txt")
    os.chdir("../..")

if CONFIG_JSON["Get_SharpCollection"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking SharpCollection ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/Flangvik/SharpCollection.git","SharpCollection","master")
    os.chdir("..")

#======================================================
# Powershell Script for windows
#======================================================   
if CONFIG_JSON["Get_PowerSploit_master"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Get_PowerSploit master ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/PowerShellMafia/PowerSploit.git","PowerSploit_Master","master")
    os.chdir("../..")

if CONFIG_JSON["Get_PowerSploit_dev"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Get_PowerSploit dev ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/PowerShellMafia/PowerSploit.git","PowerSploit_Dev","dev")
    os.chdir("../..")

if CONFIG_JSON["Get_Nishang"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking nishang dev ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/samratashok/nishang.git","Nishang","master")
    os.chdir("../..")

if CONFIG_JSON["Get_RedTeamPowershellScripts"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking RedTeamPowershellScripts dev ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/Mr-Un1k0d3r/RedTeamPowershellScripts.git","RedTeamPowershellScripts","master")
    os.chdir("../..")

if CONFIG_JSON["Get_PowerShell_Suite"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking PowerShell-Suite ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/FuzzySecurity/PowerShell-Suite.git","PowerShell_Suite","master")
    os.chdir("../..")

if CONFIG_JSON["Get_ADACLScanner"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking ADACLScanner ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    LocalName = "ADACLScanner"
    name,id,update_at,download_url,LocalName = ReleasesFileGetFromGithubRepo("https://api.github.com/repos/canix1/ADACLScanner/releases/latest",[["ADACLScan.ps1",LocalName]])[0]
    if (ReleasesFileNeedUpdate(LocalName,name,id,update_at) or (not os.path.exists("ADACLScan.ps1")) ):
        print(" +  Downloading package ...")
        WgetDownloadFile(download_url,"ADACLScan.ps1",True)
        print(" !  Done.")
    else:
        print(" !  Already up to date.")
    os.chdir("../..")

if CONFIG_JSON["Get_PowerUpSQL"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking PowerUpSQL.ps1 ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    files_lists = [
        ["PowerUpSQL.ps1","PowerUpSQL.ps1"]
    ]
    ProjectGetFilesAndUpdate("NetSPI/PowerUpSQL","master",files_lists)
    os.chdir("../..")


if CONFIG_JSON["Get_NetSPIPowershell"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking NetSPI PowerShell ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/NetSPI/PowerShell.git","NetSPI_Powershell","master")
    os.chdir("../..")

if CONFIG_JSON["Get_ADModule"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Get_ADModule ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    files_lists = [
        ["Import-ActiveDirectory.ps1","Import-ActiveDirectory.ps1"]
    ]
    ProjectGetFilesAndUpdate("samratashok/ADModule","master",files_lists)
    os.chdir("../..")

if CONFIG_JSON["Get_Privesc"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Get_Privesc ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    files_lists = [
        ["privesc.ps1","privesc.ps1"]
    ]
    ProjectGetFilesAndUpdate("enjoiz/Privesc","master",files_lists)
    os.chdir("../..")

if CONFIG_JSON["Get_PowerShell_Obfuscator"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking PowerShell Obfuscator ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/danielbohannon/Invoke-Obfuscation.git","PowerShell_Obfuscator","master")
    os.chdir("../..")

if CONFIG_JSON["Get_ADLab"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking ADLab ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/xbufu/ADLab.git","ADLab","main")
    os.chdir("../..")
    
if CONFIG_JSON["Get_BadBlood"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking BadBlood ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/davidprowe/BadBlood.git","BadBlood","master")
    os.chdir("../..")

if CONFIG_JSON["Get_AdsiPS"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking AdsiPS ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/lazywinadmin/AdsiPS.git","AdsiPS","master")
    os.chdir("../..")


if CONFIG_JSON["Get_ADEssentials"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking ADEssentials ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/EvotecIT/ADEssentials.git","ADEssentials","master")
    os.chdir("../..")


if CONFIG_JSON["Get_Active_Directory_Scripts"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Active Directory Scripts Powershell ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/chadmcox/Active_Directory_Scripts.git","Active_Directory_Scripts","master")
    os.chdir("../..")

if CONFIG_JSON["Get_PowerSharpPack"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking PowerSharpPack ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/S3cur3Th1sSh1t/PowerSharpPack.git","PowerSharpPack","master")
    os.chdir("../..")

if CONFIG_JSON["Get_Vulnerable_AD"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking vulnerable-AD ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    files_lists = [
        ["vulnad.ps1","vulnad.ps1"]
    ]
    ProjectGetFilesAndUpdate("WazeHell/vulnerable-AD","master",files_lists)
    os.chdir("../..")
    
if CONFIG_JSON["Get_PSHTML_AD_Report"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking PSHTML-AD ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    files_lists = [
        ["PSHTML-AD.ps1","PSHTML-AD.ps1"]
    ]
    ProjectGetFilesAndUpdate("bwya77/PSHTML-AD-Report","master",files_lists)
    os.chdir("../..")
    
if CONFIG_JSON["Get_adPEAS"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking adPEAS ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    files_lists = [
        ["adPEAS.ps1","adPEAS.ps1"],
        ["adPEAS-Light.ps1","adPEAS-Light.ps1"], 
    ]
    ProjectGetFilesAndUpdate("61106960/adPEAS","main",files_lists)
    os.chdir("../..")
    
if CONFIG_JSON["Get_puckiestyle_Powershell"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking puckiestyle Powershell ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/puckiestyle/powershell.git","Puckiestyle_Powershell","master")
    os.chdir("../..")
    
if CONFIG_JSON["Get_sagarv26_Powershell"]:
    if not (os.path.exists("Windows")):
        os.mkdir("Windows")
    os.chdir("Windows")
    if not (os.path.exists("Powershell")):
        os.mkdir("Powershell")
    os.chdir("Powershell")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking sagarv26 Powershell ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/sagarv26/powershell.git","Sagarv26_Powershell","master")
    os.chdir("../..")

#======================================================
# Linux
#======================================================    
if CONFIG_JSON["Get_pspy"]:
    if not (os.path.exists("Linux")):
        os.mkdir("Linux")
    os.chdir("Linux")
    if not (os.path.exists("Pspy")):
        os.mkdir("Pspy")
    os.chdir("Pspy")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Pspy ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    download_files = [
        ["^pspy32$","pspy32"],
        ["^pspy32s$","pspy32s"],
        ["^pspy64$","pspy64"],
        ["^pspy64s$","pspy64s"]
    ]
    for name,id,update_at,download_url,LocalName in ReleasesFileGetFromGithubRepo("https://api.github.com/repos/DominicBreuker/pspy/releases/latest",download_files):
        if (ReleasesFileNeedUpdate(LocalName,name,id,update_at) or (not os.path.exists(LocalName))):
            print(" +  Downloading package ...")
            WgetDownloadFile(download_url,LocalName,True)
            ReleasesFileSaveVersion(LocalName,name,id,update_at)
            print(" !  Done.")
        else:
            print(" !  Already up to date.")
    os.chdir("../..")
    
if CONFIG_JSON["Get_linPEAS"]:
    if not (os.path.exists("Linux")):
        os.mkdir("Linux")
    os.chdir("Linux")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking linPEAS ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    download_files = [
        ["linpeas.sh","linpeas.sh"],
    ]
    for name,id,update_at,download_url,LocalName in ReleasesFileGetFromGithubRepo("https://api.github.com/repos/carlospolop/PEASS-ng/releases/latest",download_files):
        if (ReleasesFileNeedUpdate(LocalName,name,id,update_at) or (not os.path.exists(LocalName))):
            print(" +  Downloading package ...")
            WgetDownloadFile(download_url,LocalName,True)
            ReleasesFileSaveVersion(LocalName,name,id,update_at)
            print(" !  Done.")
        else:
            print(" !  Already up to date.")
    os.chdir("..")
    
if CONFIG_JSON["Get_LinEnum"]:
    if not (os.path.exists("Linux")):
        os.mkdir("Linux")
    os.chdir("Linux")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking LinEnum ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    download_files = [
        ["LinEnum.sh","LinEnum.sh"],
    ]
    ProjectGetFilesAndUpdate("rebootuser/LinEnum","master",download_files)
    os.chdir("..")    
    
if CONFIG_JSON["Get_LSE"]:
    if not (os.path.exists("Linux")):
        os.mkdir("Linux")
    os.chdir("Linux")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking linux-smart-enumeration ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    download_files = [
        ["lse.sh","lse.sh"],
    ]
    ProjectGetFilesAndUpdate("diego-treitos/linux-smart-enumeration","master",download_files)
    os.chdir("..")    
    
if CONFIG_JSON["Get_sudo_killer"]:
    if not (os.path.exists("Linux")):
        os.mkdir("Linux")
    os.chdir("Linux")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking SUDO_KILLER ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/TH3xACE/SUDO_KILLER.git","SUDO_KILLER","master")
    os.chdir("..")

if CONFIG_JSON["Get_unix_privesc_check"]:
    if not (os.path.exists("Linux")):
        os.mkdir("Linux")
    os.chdir("Linux")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Unix_privesc_check ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/pentestmonkey/unix-privesc-check.git","Unix_privesc_check","master")
    os.chdir("..")

#======================================================
# Wordlists
#======================================================    
if CONFIG_JSON["Get_secLists"]:
    if not (os.path.exists("Wordlists")):
        os.mkdir("Wordlists")
    os.chdir("Wordlists")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking secLists ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/danielmiessler/SecLists.git","secLists","master")
    os.chdir("..")
    
if CONFIG_JSON["Get_Auto_Wordlists"]:
    if not (os.path.exists("Wordlists")):
        os.mkdir("Wordlists")
    os.chdir("Wordlists")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Auto_Wordlists ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/carlospolop/Auto_Wordlists.git","Auto_Wordlists","main")
    os.chdir("..")
    
if CONFIG_JSON["Get_DOC"]:
    if not (os.path.exists("Wordlists")):
        os.mkdir("Wordlists")
    os.chdir("Wordlists")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Dictionary-Of-Pentesting ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/insightglacier/Dictionary-Of-Pentesting.git","Dictionary-Of-Pentesting","master")
    os.chdir("..")
    
if CONFIG_JSON["Get_Rockyou"]:
    if not (os.path.exists("Wordlists")):
        os.mkdir("Wordlists")
    os.chdir("Wordlists")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Rockyou ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    if not (os.path.exists('rockyou.txt')):
        WgetDownloadFile("https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt","rockyou.txt")
    os.chdir("..")

if CONFIG_JSON["Get_kkrypt0nn_Wordlists"]:
    if not (os.path.exists("Wordlists")):
        os.mkdir("Wordlists")
    os.chdir("Wordlists")
    COUNTER_RUNNING += 1
    print("[%s/%s >] Checking Dictionary-Of-Pentesting ..." % (COUNTER_RUNNING,COUNTER_TOTAL))
    UpdateFromGithub("https://github.com/kkrypt0nn/Wordlists.git","Kkrypt0nn_Wordlists","master")
    os.chdir("..")

CheckGithubAPIQuta()

os.system("chmod 755 -R .")
print("-------------------------- Total ------------------------------")
os.system("du -h --max-depth=1 .")
print("\nDone! -- by manesec.")
