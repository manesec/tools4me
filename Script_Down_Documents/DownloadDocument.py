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
                           Version: 20220301
                https://github.com/manesec/tools4me
---------------------------------------------------------------""")
def UpdateFromGithub(URL,Locate,Branches):
    if not os.path.exists(Locate):
        os.system("git clone -b %s %s %s " % (Branches,URL,Locate))
    else:
        os.chdir(Locate)
        os.system("git pull origin %s" % (Branches))
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

os.chdir("..")
# -----------------------------------------------------

print("[*] Making Read-only Permission.")
os.system("chmod 755 -R /opt/MDoc")

os.system("du -h --max-depth=1")

print("[!] All Document in /opt/MDoc ")
print("Done! by Mane.")