import requests
import os
import json
from git import Repo

class update_handle:
    def __init__(self) -> None:
        pass
    def update_check(self, cur_version):
        js = json.loads(requests.get("https://raw.githubusercontent.com/buffkermitisagod/File_Cloud/main/config.json").text)
        git_version = js["server"]["version"]

        if int(git_version.replace("v", "")) > int(cur_version.replace("v", "")):
            print("[!] new version out!")
            print("current ("+cur_version+") < github ("+git_version+")")
            print("[!] Downloading new version now...")
            self.download_new()
    def download_new(self):
        print("[+] downloading github repo...")
        os.mkdir("download")
        Repo.clone_from("https://github.com/buffkermitisagod/File_Cloud", "download")

        print("[+] transfering user's and there files")
        
        x = len(os.listdir("files/data/user"))
        c = 0
        for i in os.listdir("files/data/user"):
            print(" [json ", end="")
            print("("+str(c),"/"+str(x)+") -> ", i, end="")
            file = open("download/files/data/user/"+i, "x+")
            file.write(open("files/data/users/"+i, "r").read())
            file.close()
            print("Done] ", end="")

            print(" [files ", end="")
            os.mkdir("download/files/user_"+i.replace(".json", ""))
            os.system("mv files/user_"+i.replace(".json", "")+"download/files/user_"+i.replace(".json", ""))
            print("Done] ", end="")

            print(" [User Done] ")

            c += 1
        
        print("[+] extracting new program")
        os.system("mv download/ .")
        print("[DONE] Please type 'python3 main.py' to relaunch the program :)")

