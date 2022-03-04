import os
import sys

print("""
 ▄▀▀▄ ▄▀▄  ▄▀▀█▄   ▄▀▀▄ ▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▄▄▄▄  
█  █ ▀  █ ▐ ▄▀ ▀▄ █  █ █ █ ▐  ▄▀   ▐ █ █   ▐ ▐  ▄▀   ▐ █ █    ▌ 
▐  █    █   █▄▄▄█ ▐  █  ▀█   █▄▄▄▄▄     ▀▄     █▄▄▄▄▄  ▐ █      
  █    █   ▄▀   █   █   █    █    ▌  ▀▄   █    █    ▌    █      
▄▀   ▄▀   █   ▄▀  ▄▀   █    ▄▀▄▄▄▄    █▀▀▀    ▄▀▄▄▄▄    ▄▀▄▄▄▄▀ 
█    █    ▐   ▐   █    ▐    █    ▐    ▐       █    ▐   █     ▐  
▐    ▐            ▐         ▐                 ▐        ▐     
        Download Documents on your system - Tools4me by Mane.
                           Version: 20220302
                https://github.com/manesec/tools4me
---------------------------------------------------------------""")
def UpdateFromGithub(URL,Locate,Branches):
    if not os.path.exists(Locate):
        os.system("git clone -b %s %s %s " % (Branches,URL,Locate))
    else:
        os.chdir(Locate)
        os.system("git pull origin %s || (git stash drop && git pull origin %s )" % (Branches,Branches))
        os.chdir("..")


if (os.getuid() != 0):
    print("Please run as ROOT !!")
    sys.exit(0)

if not os.path.exists("/opt/MDoc"):
    os.mkdir("/opt/MDoc")
os.chdir("/opt/MDoc")

#######################################################
# Main Book
#######################################################
print("[>] Getting Hacktricks ...")
UpdateFromGithub("https://github.com/carlospolop/hacktricks.git","Hacktricks","master")

print("[>] Getting PayloadsAllTheThings ...")
UpdateFromGithub("https://github.com/swisskyrepo/PayloadsAllTheThings.git","PayloadsAllTheThings","master")

print("[>] Getting Privilege Escalation Workshop ...")
UpdateFromGithub("https://github.com/sagishahar/lpeworkshop.git","lpeworkshop","master")


#######################################################
# CheatSheet
#######################################################
if not os.path.exists("CheatSheet"):
    os.mkdir("CheatSheet")
os.chdir("CheatSheet")

print("[>] Getting Cheat Sheet Active Directory ...")
UpdateFromGithub("https://github.com/drak3hft7/Cheat-Sheet---Active-Directory.git","Cheat_Sheet_Active_Directory","main")

print("[>] Getting Active Directory Exploitation Cheat Sheet ...")
UpdateFromGithub("https://github.com/S1ckB0y1337/Active-Directory-Exploitation-Cheat-Sheet.git","Active_Directory_Exploitation_Cheat_Sheet","master")

print("[>] Getting Awesome RedTeam Cheatsheet ...")
UpdateFromGithub("https://github.com/RistBS/Awesome-RedTeam-Cheatsheet","Awesome_RedTeam_Cheatsheet","master")

print("[>] Getting Linux Command Cheatsheet ...")
UpdateFromGithub("https://github.com/inetum-peru/cheatsheet.git","Linux_Command","develop")

print("[>] Getting Programming Language Cheatsheet ...")
UpdateFromGithub("https://github.com/darkmatter18/cheatsheet.git","Programming_Language","master")

print("[>] Getting Big Programming Language Cheatsheet ...")
UpdateFromGithub("https://github.com/JonnyBanana/Huge-Collection-of-CheatSheet.git","Big_Programming_Language","master")

print("[>] Getting Offensive Reverse Shell Cheat Sheet ...")
UpdateFromGithub("https://github.com/d4t4s3c/Offensive-Reverse-Shell-Cheat-Sheet.git","Offensive_Reverse_Shell_Cheat_Sheet","master")

print("[>] Getting Simple Pentesting Cheatsheet ...")
UpdateFromGithub("https://github.com/ac3mcl0ud/Pentesting.git","Simple_Pentesting_Cheatsheet","main")

print("[>] Getting PHP LFI RCE Cheatsheet ...")
UpdateFromGithub("https://github.com/RoqueNight/LFI---RCE-Cheat-Sheet.git","PHP_LFI_RCE_Cheatsheet","master")

print("[>] Getting Active-Directory-Exploitation-Cheat-Sheet ...")
UpdateFromGithub("https://github.com/Integration-IT/Active-Directory-Exploitation-Cheat-Sheet","Active-Directory-Exploitation-Cheat-Sheet","master")

os.chdir("..")
#######################################################
# Tools List
#######################################################
if not os.path.exists("ToolsList"):
    os.mkdir("ToolsList")
os.chdir("ToolsList")

print("[>] Getting awesome-php-security ...")
UpdateFromGithub("https://github.com/guardrailsio/awesome-php-security.git","awesome_php_security","master")

os.chdir("..")
# -----------------------------------------------------

print("[*] Making Read-only Permission.")
os.system("chmod 755 -R /opt/MDoc")

os.system("du -h --max-depth=1")

print("[!] All Document in /opt/MDoc ")
print(" -  If have error just run it again, it will automatic fix.") 
print("Done! by Mane.")