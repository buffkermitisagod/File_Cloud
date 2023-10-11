import json, os


class setup:
    def __init__(self) -> None:
        self.stat = {
            "port": " ",
            "ip": " ",
            "users": " "
        }
        self.config = {
            "setup": {
                "setup_status": True
            },
            "server": {
                "port": 8080,
                "ip": "127.0.0.1",
                "version": "V0.1",
            }
        }
    def run(self):
        if json.loads(open("config.json", "r").read())["setup"]["setup_status"] == False:
            self.print_menu()
            self.port()
            self.ip()
            self.users()

            file = open("config.json", "w")
            file.write(json.dumps(self.config, indent=4))
            file.close()
        else:
            pass
    
    def print_menu(self):
        print("""
\x1B[2J\x1B[1;1H
                    [CONFIG]      
        Welcome to the file home startup
            
        Setup:
            ["""+self.stat["port"]+"""] port - """, self.config["server"]["port"],"""
            ["""+self.stat["ip"]+"""] ip - """+self.config["server"]["ip"]+"""
            ["""+self.stat["users"]+"""] users

        """)
    def port(self):
        run = True
        while run:
            port = input("Please enter a port to run on (999 - 9999) : ")
            try:
                if int(port) < 999:
                    print("are you sure? this will require root preivliges? ")
                    chk = input("[Y/N] : ")
                    if chk.lower() == "y" or "yes":
                        run = False
                        self.config["server"]["port"] = int(port)
                elif int(port) > 9999:
                    print("Must be below 9999!")
                else:
                    run = False
                    self.config["server"]["port"] = int(port)
            except ValueError:
                print("Must be a number!")
        
        self.stat["port"] = "X"
    def ip(self):
        self.print_menu()

        run = True
        while run:
            ip = input("1) no internet [127.0.0.1]\n2) internet [0.0.0.0]\n -> ")
            if ip == "1":
                run = False
                self.stat["ip"] = "X"
                self.config["server"]["ip"] = "127.0.0.1"
            elif ip == "2":
                run = False
                self.stat["ip"] = "X"
                self.config["server"]["ip"] = "0.0.0.0"
            else:
                print("please enter an option")
    def users(self):
        self.print_menu()
        
        run = True
        while run:
            print("User maker (this will repeat until you type 'quit')")
            name = input("Please enter username: ")
            if name == "quit":
                print("Setup complete!")
                print("starting...")
                run = False
            elif name in os.listdir("files/data/user"):
                print("name already in use!")
            else:
                pas = input("Please enter password: ")
                js = {
                    "pas": pas,
                    "coc": ""
                }
                file = open("files/data/user/"+name+".json", "x+")
                file.write(json.dumps(js, indent=4))
                file.close()
            
    def return_config(self):
        return json.loads(open("config.json", "r").read())["server"]

