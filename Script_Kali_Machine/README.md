# Script: tools4me for kali linux to machine

Quick to install tools on kali linux system for **attack machine** only.

**Machine Tools = MTools**

[Change Log](https://github.com/manesec/tools4me/blob/main/Script_Kali_Machine/CHANGE.md)

## Install

```bash
rm -rf ~/MTools; mkdir ~/MTools && cd ~/MTools && curl https://raw.githubusercontent.com/manesec/tools4me/main/Script_Kali_Machine/DownloadTools.py | python3
```

**If you need to update the tools just run it again!**

If you want to modify just **download it** in `~/MTools` , **edit it** and **run it**.

```bash
rm -rf ~/MTools; mkdir ~/MTools && cd ~/MTools && wget https://raw.githubusercontent.com/manesec/tools4me/main/Script_Kali_Machine/DownloadTools.py
vim DownloadTools.py
python3 DownloadTools.py
```

**You can submit the issues if you running failed.**

## Test on

Kali 2021

## Size

**Total `3.4 GByte` in `~/MTools` .**

```bash
340K    ./Tools4mane
60M     ./Tools
2.5G    ./Wordlists
818M    ./Windows
63M     ./Linux
23M     ./Additions
3.4G    .
```

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
+ [feroxbuster](https://github.com/epi052/feroxbuster)

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
+ [AD Module](https://github.com/samratashok/ADModule)
+ [SharpCollection](https://github.com/Flangvik/SharpCollection)
+ [NetSPI PowerShell](https://github.com/NetSPI/PowerShell)
+ [SharpView](https://github.com/tevora-threat/SharpView)
+ [BeRoot](https://github.com/AlessandroZ/BeRoot)
+ [Privesc](https://github.com/enjoiz/Privesc)
+ [PowerUpSQL](https://github.com/NetSPI/PowerUpSQL)
+ [ADCollector](https://github.com/dev-2null/ADCollector)
+ [WinPwn](https://github.com/S3cur3Th1sSh1t/WinPwn)

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

+ [HackBrowserData](https://github.com/moonD4rk/HackBrowserData)
+ **Optional**: [Webshell](https://github.com/tennc/webshell)