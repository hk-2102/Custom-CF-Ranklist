import requests, bs4, json
import os,subprocess
import sqlite3,schedule,time

cursor = sqlite3.connect('ranklist.db',check_same_thread=False)


def work():
    response = requests.get('http://iitindoreranklist.herokuapp.com/?')
    souped = bs4.BeautifulSoup(response.text)

    handle_elements = souped.select('#handle')
    handles = []

    for element in handle_elements:
        handles.append(element.getText())

    for handle in handles:
        url = "https://codeforces.com/api/user.info?handles=%s" %handle
        temp = requests.get(url)
        obj = json.loads(temp.text)
        handle = handle.replace("'", "/'")
        qry = "select * from handles where handle = '%s'" %handle
        tmp = cursor.execute(qry)
        if tmp.fetchone() != None:
            error = "Account is already registered"
        else:
            data = obj['result'][0]
            qry = "insert into handles values ('%s',%d,0)" %(handle, data['rating'])
            cursor.execute(qry)
            cursor.commit()
    print(handles)
    print(len(handles))

    qry = "select * from handles"
    tmp = cursor.execute(qry)

    tmp = tmp.fetchall()

    print(tmp)


work()
