import requests, bs4
import os,subprocess
import sqlite3,schedule,time
import json
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
            data = obj['result'][0]
            rating = 0
            if 'maxRating' in data:
                rating = data['maxRating']
            qry = "update handles set rating = %d where handle = '%s'" %(rating, handle)
            cursor.execute(qry)
            cursor.commit()
            print(handle + " already registered")
        else:
            data = obj['result'][0]
            rating = 0
            if  'maxRating' in data:
                rating = data['maxRating']
            qry = "insert into handles values ('%s',%d,0)" %(handle, rating)
            print(handle)
            cursor.execute(qry)
            cursor.commit()
    print(handles)
    print(len(handles))

    qry = "select * from handles"
    tmp = cursor.execute(qry)

    tmp = tmp.fetchall()

    print(tmp)


work()

