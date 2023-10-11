import json, os, random

class users:
    def __init__(self) -> None:
        self.cocs = {}

    def check_user(self, user, pas) -> bool:
        #* we add the test here to nulify the test user that is used as an example
        print(user, pas)
       
        #* check if the user is in the system
        if user+".json" not in os.listdir("files/data/user"):
            print("not real")
            #* if there not then we can return false
            return False
        else:

            print("pas chk")
            #* check the password of the user
            js = json.loads(open("files/data/user/"+user+".json", "r").read())

            if js["pas"] == pas:
                return True
            
        return False
    
    #* creats a "random" coockie for the user
    def create_coc(self, user) -> str:
        x = ""
        for i in range(0, 10):
            x += str(random.randint(0, 9))
        self.cocs[user] = x

        self.save_users_coc(x, user)
        return x
    
    #* checks the auth of the user
    def chk_coc(self, user, coc) -> bool:
        if self.chk_coc_file(user, coc):
            return True
        elif user not in self.cocs:
            return False
        elif self.cocs[user] == coc:
            return True
        else:
            return False
    def chk_coc_file(self, user, coc):
        if user+".json" not in os.listdir("files/data/user"):
            return False
        
        js = json.loads(open("files/data/user/"+user+".json", "r").read())
        if js["coc"] == coc:
            return True
        else:
            return False
        
    def check_user_cock_auth(self, request) -> bool:
        if "user" and "auth" in request.cookies:

            usr = request.cookies.get("user")
            pas = request.cookies.get("auth")
            
            if self.chk_coc(usr, pas):
                return True
            
        return False
    
    #* add percistance to the program
    def save_users_coc(self, coc, user) -> None:
        js = json.loads(open("files/data/user/"+user+".json", "r").read())
        js["coc"] = coc

        file = open("files/data/user/"+user+".json", "w")
        file.write(json.dumps(js, indent=4))
        file.close()
