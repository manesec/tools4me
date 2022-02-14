# tools4me for kali linux machine

Quick to install tools on kali linux system for **attack machine** only.

[Change Log](https://github.com/manesec/tools4me/blob/main/Kali_Machine/CHANGE.md)

## Install

```bash
rm -rf ~/Tools; mkdir ~/Tools && cd ~/Tools && curl https://raw.githubusercontent.com/manesec/tools4me/main/Kali_Machine/DownloadTools.py | python3
```

**If you need to update the tools just run it again!**

If you want to modify just **download it** in `~/Tools` , **edit it** and **run it**.

```bash
rm -rf ~/Tools; mkdir ~/Tools && cd ~/Tools && wget https://raw.githubusercontent.com/manesec/tools4me/main/Kali_Machine/DownloadTools.py
vim DownloadTools.py
python3 DownloadTools.py
```

## Test on

Kali 2021

## Size

**Total `3.5 GByte` in `~/Tools` .**

```bash
240K    ./Tools4mane
179M    ./Tools
2.5G    ./Wordlists
785M    ./Windows
37M     ./Linux
96M     ./Additions
3.5G    .
```

## Optional

When you need to change the optional installation, edit the source before run. 

## Include Tools

**Command Tools**

+ [pwncat-cs](https://github.com/calebstewart/pwncat)
+ **Optional**: [zaproxy](https://github.com/zaproxy/zaproxy)
+ [gobuster](https://github.com/OJ/gobuster)
+ [hashcat full version](https://hashcat.net/hashcat/)
+ [neo4j](https://neo4j.com/)
+ [exploitdb full version](https://www.exploit-db.com/)
+ [nikto](https://github.com/sullo/nikto)
+ [DBeaver](https://dbeaver.io/download/)

**Linux**

+ [unix-privesc-check](https://github.com/pentestmonkey/unix-privesc-check)
+ [SUDO_KILLER](https://github.com/TH3xACE/SUDO_KILLER)
+ [LinEnum](https://github.com/rebootuser/LinEnum)
+ [LinPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS)
+ [linux-smart-enumeration](https://github.com/diego-treitos/linux-smart-enumeration)
+ [pspy](https://github.com/DominicBreuker/pspy)

**Windows**

+ [BloodHound](https://github.com/BloodHoundAD/BloodHound)
+ [evil-winrm](https://github.com/Hackplayers/evil-winrm)
+ [impacket](https://github.com/SecureAuthCorp/impacket)
+ [nishang](https://github.com/samratashok/nishang)
+ [WinPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/winPEAS)
+ [PowerSploit](https://github.com/PowerShellMafia/PowerSploit): dev and master
+ [mimikatz](https://github.com/gentilkiwi/mimikatz)
+ [juicy-potato](https://github.com/ohpe/juicy-potato)
+ [Lovely-Potato](https://github.com/TsukiCTF/Lovely-Potato)
+ [kerbrute](https://github.com/TarlogicSecurity/kerbrute)
+ [PoshADCS](https://github.com/cfalta/PoshADCS)
+ [ADModule](https://github.com/samratashok/ADModule)
+ [SharpCollection](https://github.com/Flangvik/SharpCollection)

**WordLists**

+ [Seclists](https://github.com/danielmiessler/SecLists)
+ [Rockyou.txt](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt)
+ **Optional**: [Dictionary-Of-Pentesting](https://github.com/insightglacier/Dictionary-Of-Pentesting)

**Tools**

+ [Godzilla](https://github.com/BeichenDream/Godzilla)
+ [nmapAutomator](https://github.com/21y4d/nmapAutomator)
+ [Behinder](https://github.com/rebeyond/Behinder)
+ [Chisel](https://github.com/jpillora/chisel)
+ [tools4mane](https://github.com/manesec/tools4mane)

**Additions**

+ [BeRoot](https://github.com/AlessandroZ/BeRoot)
+ [HackBrowserData](https://github.com/moonD4rk/HackBrowserData)
+ **Optional**: [Webshell](https://github.com/tennc/webshell)