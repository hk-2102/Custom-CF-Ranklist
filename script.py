import requests, bs4, json
import os,subprocess
import sqlite3,schedule,time

cursor = sqlite3.connect('ranklist.db',check_same_thread=False)

cursor2 = sqlite3.connect('ranklist.db',check_same_thread=False)

def update():
    print("updating")
    pset = []
    tmp3 = cursor.execute('''Select * from problems''')
    while True:
        pname = tmp3.fetchone()
        if pname == None:
            break
        pset.append(pname[1])
    tmp = cursor.execute('''SELECT * from handles''')
    while True:
        handle = tmp.fetchone()
        if handle == None:
            break
        cursor2.execute('''update handles set solved = 0 where handle = '%s' '''%(handle[0]))

    tmp = cursor.execute('''Select * from problems''')
    while True:
        problem = tmp.fetchone()
        if problem == None:
            break
        cursor2.execute('''update problems set solved = 0 where name = '%s'; ''' %(problem[1]))
        
    tmp = cursor.execute('''SELECT handle from handles''')
    while True:
        handle = tmp.fetchone()
        probstatus = dict()
        if handle == None:
            break
        try:
            url = "https://codeforces.com/api/user.status?handle=%s" %(handle[0])
            sub1 = requests.get(url)
            sub = json.loads(sub1.text)
            if sub['status'] != "OK":
                continue
            for stat in sub['result']:
                if stat['verdict'] == "OK":
                    probstatus[stat['problem']['name']] = True

            for x in probstatus:
                if probstatus[x] == True and x in pset:
                    qry = '''select * from problems where name = "%s" ''' %(x)
                    tmp2 = cursor2.execute(qry)
                    if tmp2.fetchone() != None:
                        try:
                            qry = '''update handles set solved = solved+1 where handle = "%s" ''' %(handle[0])
                            cursor2.execute(qry)
                        except:
                            print("not possible here")
                        try:
                            qry = '''update problems set solved = solved+1 where name = "%s" ''' %(x)
                            cursor2.execute(qry)
                        except:
                            print("not possible here")
            print("done %s" %(handle))
        except:
            print("skipping %s" %(handle))

    cursor.commit()
    cursor2.commit()
    print("done update")

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
update()
