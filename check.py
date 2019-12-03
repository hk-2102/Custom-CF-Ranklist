import requests,schedule,sqlite3,json
from operator import itemgetter
from flask import Flask,render_template,session,request,redirect,url_for,flash
import os
import multiprocessing
import time

app = Flask(__name__)

cursor = sqlite3.connect('all_problems.db',check_same_thread=False)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS problems(
        ProblemID varchar(10) PRIMARY KEY,
        problemsetName varchar(255),
        name varchar(255),
        rating int,
        points int,
        link varchar(255)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tags(
        ProblemID varchar(10),
        tags varchar(255)
    );
''')

qry = "select * from problems where name like 'New%'"
tmp = cursor.execute(qry)

for i in range(0, 1):
    problem = tmp.fetchone()
    print(problem)