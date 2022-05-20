#CREATE TABLE posts (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, usrid INTEGER NOT NULL, title TEXT NOT NULL, caption TEXT NOT NULL, info TEXT NOT NULL, district TEXT NOT NULL, detail TEXT NOT NULL, image TEXT, date DATETIME NOT NULL, FOREIGN KEY(usrid) REFERENCES users(id));
# CREATE UNIQUE INDEX pid ON posts(id);
# CREATE UNIQUE INDEX pdate ON posts(date);
#select seq from sqlite_sequence where name="posts";
import os
import sys
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, session, request, url_for
from datetime import datetime
import math

db = SQL("sqlite:///lost.db")
usrid = 1

date = datetime.now().strftime("%d/%m/%y %H:%M:%S")
# image = "NULL"

print(date)
#db.execute("INSERT INTO posts (usrid, title, caption, info, district, detail, image, date) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", usrid, "A title", "A caption", "01772488663", "Rajshahi", "Some detail", image, date)

rows_2 = db.execute("INSERT INTO up_images (pid, usrid, public_id,  signature, deleted) VALUES (?, ?, ?, ?, ?)", 13, 1, date)
# page_num = math.ceil(rows_2[0]['COUNT(id)']/12)

# for i in rows:
#     if i['image'] == "NULL":
#         i['image'] = "static/no-image.png"

#     else:
#         my = i['image'].split("upload")
#         i['image'] = my[0] + "upload/c_scale,w_200" + my[1] + "upload" + my[2]


print(rows_2)

# CREATE TABLE deleted (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, pid INTEGER NOT NULL, usrid INTEGER NOT NULL);

# # print(page_num)
# #sdfsdfs
# 1|1|1
# 2|13|1

# CREATE TABLE deleted (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, pid INTEGER NOT NULL, usrid INTEGER NOT NULL, date DATETIME NOT NULL);
# CREATE UNIQUE INDEX post_id ON deleted(pid);