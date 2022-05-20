import os
import sys
import requests
import math
import cloudinary
import cloudinary.uploader
import cloudinary.api
import time
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, session, request, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from helpers import login_required, check_email, get_dis, allowed_file, make_square, apology, get_song
from pathlib import Path
from dotenv import load_dotenv
from cloudinary.utils import cloudinary_url
from PIL import Image, ImageOps
from bleach import Cleaner
from bleach.linkifier import LinkifyFilter
from functools import partial

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# # Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
# Configure cloudinary sdk to upload and delete images

db = SQL("sqlite:///lost.db")
load_dotenv()
cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    
    num = request.args.get("page")
    check = True

    if not num:
        num = 1
        check = False

    if check:
        if not num.isnumeric():
            return apology("NO NO")
    
    rows_2 = db.execute("SELECT seq FROM sqlite_sequence WHERE name='posts'")
    rows_3 = db.execute("SELECT seq FROM sqlite_sequence WHERE name='deleted'")

    page_num = math.ceil((rows_2[0]['seq']-rows_3[0]['seq'])/12)

    if int(num)<1 or int(num)>page_num:
        return apology("Lol out of index")

    rows = db.execute("SELECT id, title, caption, district, image, date FROM posts ORDER BY id DESC LIMIT 12 OFFSET ?", (int(num)-1)*12)

    for i in rows:
        
        if i['image'] == "NULL":
            i['image'] = "static/icon.png"

        else:
            my = i['image'].split("upload")
            i['image'] = my[0] + "upload/c_scale,w_200" + my[1] + "upload" + my[2]
        
        i['post_link'] = "/ads?khoj=" + str(i['id'])
       
        date_time_str = i['date']
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
        i['date']  = date_time_obj.strftime("%d/%m/%y")



    return render_template("index.html", row=rows, num=page_num)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Where's the username..?", 'error')
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Where's the password..?", 'error')
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid user or password.", 'error')
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Login successful.!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")
        error = {}

        if not username:
            error["error"] = "No Username!"
            return jsonify(error)
        

        elif len(username.strip())<6 or len(username.strip())>12:
            error["error"] = "Invalid username"
            return jsonify(error)

        elif not email:
            error["error"] = "Must provide email..!"
            return jsonify(error)

        elif not check_email(email.strip()):
            error["error"] = "Invalid Email"
            return jsonify(error)
        
        elif not password:
            error["error"] = "Must provide password..!"
            return jsonify(error)
        
        elif len(password)<8 or len(password) >20:
            error["error"] = "Invalid Password"
            return jsonify(error)

        elif not confirm or confirm != password:
            error["error"] = "Passwords don't match..!"
            return jsonify(error)

        rows = db.execute("SELECT username FROM users WHERE username = ?", username.strip())

        if len(rows)!=0:
            error["error"] = "User Already exists..!"
            return jsonify(error)
        
        rows2 = db.execute("SELECT email FROM users WHERE email = ?", email.strip())

        if len(rows2)!=0:
            error["error"] = "Email Already exists..!"
            return jsonify(error)
        
        date = datetime.now().strftime("%d/%m/%y %H:%M:%S")

        db.execute("INSERT INTO users (username, hash, email, date) VALUES(?, ?, ?, ?)", username.strip(), generate_password_hash(password), email.strip(), date)

        error["error"] = "Registered..!"
        return jsonify(error)

    else:
        return render_template("register.html")



@app.route("/post", methods=["POST", "GET"])
@login_required
def post():

    if request.method == "POST":

        file = request.files['file']
        title = request.form.get('title')
        caption = request.form.get('caption')
        info = request.form.get('info')
        district = request.form.get('district')
        details = request.form.get('subject')
        error = {}

        if not title:
            error["error"] = "Invalid title"
            return jsonify(error)

        if len(title.strip())>18:
            error["error"] = "Title out of range"
            return jsonify(error)

        if not caption:
            error["error"] = "Invalid Caption"
            return jsonify(error)
        
        if len(caption.strip())>140:
            error["error"] = "Caption out of range"
            return jsonify(error)

        if not info:
            error["error"] = "Invalid info"
            return jsonify(error)
        
        if len(info.strip())>50:
            error["error"] = "Contact out of range"
            return jsonify(error)
        
        if not district or district not in get_dis():
            error["error"] = "Invalid district"
            return jsonify(error)
        
        if not details:
            error["error"] = "Please add some details."
            return jsonify(error)
        
        if len(details.strip())<10:
            error["error"] = "Please add some details."
            return jsonify(error)
        

        if not file:
            fileurl = "NULL"

        else:
                    
            if file.filename == '':
                error["error"] = "No filename"
                return jsonify(error)
            
            if not allowed_file(file.filename):
                error["error"] = "File errror"
                return jsonify(error)


            file.seek(0, os.SEEK_END)
            file_length = file.tell()
            file.seek(0, 0)

            if file_length>7340032:
                error["error"] = "Invalid file size"
                return jsonify(error)

            UPLOAD_FOLDER = 'static/uploads/' + str(session["user_id"]) + "/"
        
            Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fileurl = UPLOAD_FOLDER + filename
            
            rows = db.execute("SELECT seq FROM sqlite_sequence WHERE name='posts'")
            
            
            pubfile = UPLOAD_FOLDER + str(session['user_id']) + "_" + str((rows[0]['seq'])+1)
            
            try:
                test_image = Image.open(fileurl)
                test_image = ImageOps.exif_transpose(test_image)
                new_image = make_square(test_image)
                new_image.save(fileurl, "JPEG", optimize = True, quality = 10)
                
                # print(pubfile)
                
                upload_result = cloudinary.uploader.upload(fileurl, public_id = pubfile)

                os.remove(fileurl)
                # print(upload_result)
                
                fileurl = upload_result['secure_url']
            
            except:
                fileurl = "NULL"

        date = datetime.now().strftime("%d/%m/%y %H:%M:%S")

        db.execute("INSERT INTO posts (usrid, title, caption, info, district, detail, image, date) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], title.strip(), caption.strip(), info.strip(), district.strip(), details.strip(), fileurl, date)

        error["error"] = "Success"
        return jsonify(error)
    
    else:

        return render_template("post.html", districts=get_dis())

@app.route("/del_post", methods=["POST", "GET"])
@login_required
def del_post():

    if request.method == "POST":

        pid = request.form.get('pid')
        error = {}

        if not pid:
            return apology("No No")
        
        if not pid.isnumeric():
            return apology("NO NO")

        rows = db.execute("SELECT usrid, image FROM posts WHERE id=?", pid)

        if not rows:
            return apology("Post not found")

        else:
            
            
            if rows[0]['usrid']==session['user_id']:
                
                date = datetime.now().strftime("%d/%m/%y %H:%M:%S")

                if rows[0]['image']!="NULL":
                    
                    public_id = 'static/uploads/' + str(session["user_id"]) + "/" + str(session['user_id']) + "_" + str(pid)
                    cloudinary.uploader.destroy(public_id)

                db.execute("INSERT INTO deleted (pid, usrid, date) VALUES (?, ?, ?)", pid, session['user_id'], date)
                rows_2 = db.execute("DELETE FROM posts WHERE id = ?", pid)

                error["error"] = "Success"
                return jsonify(error)
            
            else:
                error["error"] = "You Do not own it."
                return jsonify(error)
        
    else:
        return apology("Hell No")




@app.route("/ads", methods = ["GET"])
def ads():
    
    num = request.args.get("khoj")

    if not num:
        return apology("Must give post id")

    if not num.isnumeric():
        return apology("NO NO")

    rows_2 = db.execute("SELECT seq FROM sqlite_sequence WHERE name='posts'")
    post_num = rows_2[0]['seq']

    if int(num)<1 or int(num)>post_num:
        return apology("Index out of range")
    
    rows = db.execute("SELECT * FROM posts WHERE id=?", num)
    
    if not rows:
        return apology("No ad here")

    if rows[0]['image'] == "NULL":
        rows[0]['image'] = "static/icon.png"

    else:
        rows[0]['better_image'] = rows[0]['image']
        my = rows[0]['image'].split("upload")
        rows[0]['image'] = my[0] + "upload/c_scale,w_461" + my[1] + "upload" + my[2]
    
    cleaner = Cleaner(tags=[], filters=[LinkifyFilter])

    
    rows[0]['info'] = cleaner.clean(rows[0]['info'])
    rows[0]['detail'] = cleaner.clean(rows[0]['detail'])
    
    date_time_obj = datetime.strptime(rows[0]['date'], '%d/%m/%y %H:%M:%S')
    rows[0]['date']  = date_time_obj.strftime("%d/%m/%y")

    return render_template("ads.html", info=rows[0])

@app.route("/my_ads", methods=["GET"])
@login_required
def my_index():
    
    num = request.args.get("page")
    check = True

    if not num:
        num = 1
        check = False

    if check:
        if not num.isnumeric():
            return apology("NO NO")
    
    rows_2 = db.execute("SELECT COUNT(id) FROM posts WHERE usrid=?", session["user_id"])
    page_num = math.ceil(rows_2[0]['COUNT(id)']/12)

    if page_num==0:
        return apology("You have no posts")

    if int(num)<1 or int(num)>page_num:
        return apology("Lol out of index")

    rows = db.execute("SELECT id, title, caption, district, image, date FROM posts WHERE usrid=? ORDER BY id DESC LIMIT 12 OFFSET ?", session["user_id"], (int(num)-1)*12)

    for i in rows:
        
        if i['image'] == "NULL":
            i['image'] = "static/icon.png"

        else:
            my = i['image'].split("upload")
            i['image'] = my[0] + "upload/c_scale,w_200" + my[1] + "upload" + my[2]
        
        i['post_link'] = "/ads?khoj=" + str(i['id'])
       
        date_time_str = i['date']
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
        i['date']  = date_time_obj.strftime("%d/%m/%y")

    usr_name = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])

    return render_template("my_index.html", row=rows, num=page_num, usr=usr_name[0])

@app.route("/about", methods=["GET"])
def about():

    return render_template("about.html")

@app.route("/search", methods=["GET"])
@login_required
def search():

    song = get_song()

    return render_template("search.html", song=song)

@app.route("/riddler", methods=["GET"])
def riddler():

    return render_template("riddler.html")


@app.route("/jerry", methods=["GET", "POST"])
def jerry():

    if request.method=="POST":
        usr = request.form.get('rat')

        if not usr:
            return apology("No input")

        usr = usr.strip().lower()
        error = {}

        if usr != "mir jafar":
            error['message'] = "WRONG WRONG WRONG !!!"
            return jsonify(error)
        
       
        error['message'] = "Congrats to you for solving the puzzle. Text me this screenshot on telegram and I will add your name to the leaderboard.😎"
        return jsonify(error)
    else:
        return render_template("jerry.html")
