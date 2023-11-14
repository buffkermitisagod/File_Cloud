from flask import *
import logging, os, sys

#* local imports
from mod.users import users
from mod.file_hand import file_handler
from mod.setups import setup

#* setup chk
runner = setup()
runner.run()

config = runner.return_config()

#* set the app up
"""log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)"""

app = Flask(__name__)
use = users()
files = file_handler()


#* program boot
# todo # check if it's the first boot of the program
# todo # also check for a -s flag to enter a new setup phase
# todo # read config
# todo # parse it all to a class (make it easier)


if "-s" in sys.argv:
    runner.run()
if "-u" in sys.argv:
    print("u")
    runner.users()

print("""
\x1B[2J\x1B[1;1H
████████████████████████████████████████████████
█▄ ▄▄ █▄ ▄█▄ ▄███▄ ▄▄ ███ █ █ ▄▄ █▄ ▀█▀ ▄█▄ ▄▄ █
██ ▄████ ███ ██▀██ ▄█▀███ ▄ █ ██ ██ █▄█ ███ ▄█▀█
█▄▄▄███▄▄▄█▄▄▄▄▄█▄▄▄▄▄███▄█▄█▄▄▄▄█▄▄▄█▄▄▄█▄▄▄▄▄█ """+config["version"]+"""

-s -> run setup
-u -> run user add

http://"""+config["ip"]+""":"""+str(config["port"])+"""
""")


#* the flask app & code

@app.route("/")
def index():
    #* check if the user is already logged in, if they are
    #* we will send them to the dashbourd
    #* if not or thier coockie is invalid we will let them login
    if use.check_user_cock_auth(request):
            return render_template("dash.html")

    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    #* get the data from the request
    usr = request.form["user"]
    pas =  request.form["pass"]

    #* make sure the details 

    if use.check_user(usr, pas):
        #* set the users data
        #! the coockies should have a TTL but for now we will leave them as is
        resp = make_response(render_template('dash.html'))
        resp.set_cookie('user', usr)
        resp.set_cookie('auth', use.create_coc(usr))

        return resp
    
    return redirect("/")  

@app.route("/file_list")
def file_lister():
    if use.check_user_cock_auth(request):
        # todo # use a file_handler class to list all the files
        #* example file list (file_one.txt@file_two.txt@file_three.txt)
        #* or for a file within a folder it will look like this
        #* (file_one;/path/to/file@file_two)
        return files.list_files()
    
    return redirect("/")

#* dir list
@app.route("/dir_list/<dir>")
def list_dir(dir):
    if use.check_user_cock_auth(request):
        #* send html page for it
        return render_template("dash_dir.html")

    return redirect("/")

@app.route("/dir/<dir>")
def dir_handle(dir):
    if use.check_user_cock_auth(request):
        print("files -> ", file_handler.list_files_in_dir(dir, dir))
        return file_handler.list_files_in_dir(dir, dir)      

    return redirect("/")



#* allows the users to upload a file to the server
@app.route("/files_upld/<dir_location>")
def files_upld(dir_location):
     #* auth check
     if use.check_user_cock_auth(request):
        return render_template("upload_new.html", dir=dir_location)
     
     return redirect("/")
@app.route("/upload_file/<dir_location>", methods=["POST"])
def files_save_on(dir_location):
    #* auth check
    if use.check_user_cock_auth(request):
        #* get the details of the upload
        file_name = request.form["file_name"]
        
        #* get the folder
        folder = "files/"+dir_location+"/"

        #* get the file object
        file = request.files['file_shiz']

        file.save(folder+file_name)    

    return redirect("/")


#* sends the requested file to the clients
@app.route("/files_down/files/<file_location>")
def file_send_user(file_location):
    if use.check_user_cock_auth(request):
         #* construct the full file request
         full = "files/"+str(file_location).replace("@", "/")
         #* extra input sanatizeation just for peace of mind
         full = full.replace("\n", "")

         if files.validate_file_path(full):
              return send_file(full, as_attachment=True)
         else:
              return 'File Not ('+full+') Found! Please Go To The Dash <a href="/">here</a>'
         
    return redirect("/")

#* file deletion
@app.route("/delete/files/<file_location>")
def file_delete(file_location):
    if use.check_user_cock_auth(request):
        file_name = file_location.replace("@", "/")
        file_name = "files/"+file_name
        
        #* get the file path
        os.remove(file_name)
        return redirect("/")

    return redirect("/")


#* File sharing functions
@app.route("/create_share/<file>")
def show_code(file):
    if use.check_user_cock_auth(request):
        code = files.create_link(file, 0)
        return "your code is -> "+code+", the url -> /file_share/"+code+" for the file -> "+file
    
    return redirect("/")

@app.route('/file_share/<code>')
def method_name(code):
    chk = files.scan_link(0, code)
    if chk == "404":
        return render_template("404.html")
    else:
        return send_file(chk, as_attachment=True)
    


app.run(port=config["port"], host=config["ip"])
"""
# todo # create time limmit to the file share function (KINDA DONE)
# todo # add a config                                  (DONE)

# todo # add setup function                            (DONE)
# todo # add a delete file function                    (DONE)

# todo # css the shit out of it                        (KINDA DONE)                   
# todo # allow users to create and delete dirs

# todo # allow for the upload file to have the current dir the user is in to make it easier for the user to upload a file (DONE)
# todo # clean the code 

"""


"""

    <div class=".new_upload">
        <a href="files_upld"><button>Upload new file</button></a>
    </div>

"""
