import json, os, random
from datetime import datetime

class file_handler:
    def __init__(self) -> None:
        pass

    def list_files(self) -> str:
        files = ""

        files = os.listdir("files")
        files.remove("data")
        
        file = "@".join(files)
        return file
    
    def list_files_in_dir(self, dir):
        file = os.listdir("files/"+dir)
        for i in range(0, len(file)):
            file[i] = "files/"+dir+"@"+file[i]
        return "#".join(file)


    def validate_file_path(self, path) -> bool:
        if os.path.isfile(path):
            return True
        return False
    
    #* file handle, file share shit
    def create_link(self, file, paswd):
        js = self.read_file_share()
        while True:
            code = ""
            for i in range(0, 20):
                code += str(random.randint(0, 9))
            if code not in js:
                break
        #* save code
        file = file.replace("@", "")
        file = file.replace("_", "/")

        #* timestamp stuff
        now = datetime.now()

        js[code] = {"file": file, "accses": 0}

        self.save_file_share(js)

        return code

    def scan_link(self, paswd, url_key):    
        js = self.read_file_share()

        if url_key in js:
            if js["accses"] == 0:
                js["accses"] += 1
                self.save_file_share(js)
                return js["file"][url_key]
            else:
                return "404"
        else:
            return "404"

    #* misc for this section
    def read_file_share(self) -> json:
        return json.loads(open("files/data/file_share.json", "r").read())
    
    def save_file_share(self, data):
        file = open("files/data/file_share.json", "w")
        file.write(json.dumps(data, indent=4))
        file.close()

    def delete_file_share(self, url) -> bool:
        js = self.read_file_share()

        if url in js:
            js.pop(url)
            return True
        else:
            return False
        
