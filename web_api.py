from bottle import route, run, template, post, get, request
import os.path
import sqlite3
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "greek.db")
con = sqlite3.connect(db_path)
cur = con.cursor()

@route('/')
def search():
    html = "<h2> Enter Your Requirements </h2>"
    html += '''
        <form action = "/listall" method = "post">
            God Name*: <input name = "godname" type="text" />
            Love Interests(>=): <input name = "love_interests" type="text" />
            <input value = "Search!" type = "submit" />
        </form>
    '''
    return html

@post('/listall')
def listall():
    html = "<td><a href=\"/insertgod" + "\">Insert New God</a> </td>"
    html+="<br>"
    html += "<h2> Gods </h2> <br /> <table>"
    godname = request.forms.get('godname')
    love_interests = request.forms.get('love_interests')
    html+="<td> <b>God ID</b></td> <td> <b>Name</b></td> <td> <b>Update/View God Details</b></td> <td> <b>Delete God</b></td> <td> <b>Show Hero Relation</b> </td> <td> <b>Add Hero Relation</b> </td>"
    if love_interests=="":
        for row in cur.execute("select count(*) from god where name like '%{0}%'".format(godname)):
            if row[0]==0:
                return "<td><a href=\"/insertgod" + "\">Insert New God</a> </td> <br> <br> No Matches Found. </br> return to main <a href = \"/\">page</a>"

        for row in cur.execute("select god_id,name from god where name like '%{0}%' limit 20".format(godname)):
            html += "<tr>"
            for cell in row:
                html += "<td>" + str(cell) + "</td>"
            html += "<td><a href=\"/updatetemp/" + str(row[0]) + "\">Update/View Me</a> </td>"
            html += "<td><a href=\"/delete/" + str(row[0]) + "\">Delete Me</a> </td>"
            html += "<td><a href=\"/secondrelation/" + str(row[0]) + "\">Show Heroes</a> </td>"
            html += "<td><a href=\"/insertsecondrelationtemp/" + str(row[0]) + "\">Insert Heroes</a> </td>  </tr>"
        html += "</table>"
    else:
        if not love_interests.isnumeric():
            return "<td><a href=\"/insertgod" + "\">Insert New God</a> </td> <br> <br> Invalid Entry. Love Interests Should Be an Integer. </br> return to main <a href = \"/\">page</a>"
        for row in cur.execute("select count(*) from god where name like '%{0}%' and love_interests>={1}".format(godname,love_interests)):
            if row[0]==0:
                return "<td><a href=\"/insertgod" + "\">Insert New God</a> </td> <br> <br> No Matches Found. </br> return to main <a href = \"/\">page</a>"

        for row in cur.execute("select god_id,name from god where name like '%{0}%' and love_interests>={1} limit 20".format(godname,love_interests)):
            html += "<tr>"
            for cell in row:
                html += "<td>" + str(cell) + "</td>"
            html += "<td><a href=\"/updatetemp/" + str(row[0]) + "\">Update/View Me</a> </td> "
            html += "<td><a href=\"/delete/" + str(row[0]) + "\">Delete Me</a> </td>"
            html += "<td><a href=\"/secondrelation/" + str(row[0]) + "\">Show Heroes</a> </td>"
            html += "<td><a href=\"/insertsecondrelationtemp/" + str(row[0]) + "\">Insert Heroes</a> </td>  </tr>"
        html += "</table>"   
    return html

@route('/insertgod')
def insertgod():
    html = '''
        <form action = "/insert" method = "post">
            god id: <input name = "god_id" type="text" />
            god name: <input name = "godname" type="text" />
            weapon: <input name = "weapon" type="text" />
            love_interests: <input name = "love_interests" type="text" />
            location: <input name = "location" type="text" />
            <input value = "Insert!" type = "submit" />
        </form>
    '''
    return html

@post('/insert')
def insert():
    god_id = request.forms.get('god_id')
    godname = request.forms.get('godname')
    weapon = request.forms.get('weapon')
    love_interests = request.forms.get('love_interests')
    location=request.forms.get('location')
    try:
        if not god_id.isnumeric() or not love_interests.isnumeric():
            return "Invalid Entry. No Entry Made. God ID and Love Interests Should Be Integer. </br> return to main <a href = \"/\">page</a>"
        elif god_id=="" or godname=="" or weapon=="" or love_interests=="" or location=="":
            return "Invalid Entry. No Entry Made. Please Fill All Entries.</br> return to main <a href = \"/\">page</a>"    
        else:
            cur.execute("insert into god values ({0}, '{1}', '{2}', {3},'{4}')".format(god_id, godname, weapon, love_interests,location))
            con.commit()
            return "God "+god_id +  " inserted </br> return to main <a href = \"/\">page</a>"
    except (sqlite3.IntegrityError):
        return "Invalid Entry. No Entry Made. God ID Already Exists. </br> return to main <a href = \"/\">page</a>"

@route('/updatetemp/<god_id>')
def updatetemp(god_id):
    html = "<h2> View/Update God </h2> <br /> <table>"
    html+="<td> <b>God ID</b></td> <td> <b>Name</b></td> <td> <b>Weapon</b></td> <td> <b>Love Interests</b></td> <td> <b>Location</b> </td>"
    for row in cur.execute("select * from god where god_id={0} limit 20".format(god_id)):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
    html += "</table>" 
    html+="<br>"
    route="/update/{0}".format(god_id)
    html += '''
        <form action = '{0}' method = "post">
            Weapon: <input name = "weapon" type="integer" />
            Love Interests: <input name = "love_interests" type="text" />
            Location: <input name = "location" type="text" />
            <input value = "Update!" type = "submit" />
        </form>
    '''.format(route)
    return html

@post('/update/<god_id>')
def update(god_id):
    weapon = request.forms.get('weapon')
    love_interests = request.forms.get('love_interests')
    location = request.forms.get('location')
    if weapon=='' and love_interests!='' and location!='':
        if not love_interests.isnumeric():
            return "Invalid Entry. No Updates Made. Love Interests Should Be Integer. </br> return to main <a href = \"/\">page</a>"
        cur.execute("update god set love_interests={0},location_name='{1}' where god_id={2}".format(love_interests ,location,god_id))  
    elif love_interests=='' and weapon!='' and location!='':
        cur.execute("update god set weapon='{0}',location_name='{1}' where god_id={2}".format(weapon,location,god_id)) 
    elif location=='' and love_interests!='' and weapon!='':
        if not love_interests.isnumeric():
            return "Invalid Entry. No Updates Made. Love Interests Should Be Integer. </br> return to main <a href = \"/\">page</a>"
        cur.execute("update god set weapon='{0}',love_interests={1} where god_id={2}".format(weapon, love_interests ,god_id))
    elif weapon=='' and love_interests=='' and location!='':
        cur.execute("update god set location_name='{0}' where god_id={1}".format(location,god_id))
    elif weapon=='' and location=='' and love_interests!='':
        if not love_interests.isnumeric():
            return "Invalid Entry. No Updates Made. Love Interests Should Be Integer. </br> return to main <a href = \"/\">page</a>"
        cur.execute("update god set love_interests={0} where god_id={1}".format(love_interests,god_id))
    elif location=='' and love_interests=='' and weapon!='':
        cur.execute("update god set weapon='{0}' where god_id={1}".format(weapon,god_id))
    elif weapon=='' and love_interests=='' and location=='':
        return "No Updates Made. No Data Was Entered. </br> return to main <a href = \"/\">page</a>"
    else:
        if not love_interests.isnumeric():
            return "Invalid Entry. No Updates Made. Love Interests Should Be Integer. </br> return to main <a href = \"/\">page</a>"
        cur.execute("update god set weapon='{0}',love_interests={1},location_name='{2}' where god_id={3}".format(weapon, love_interests ,location,god_id))

    con.commit()
    return "God ID "+god_id +  " Updated </br> return to main <a href = \"/\">page</a>"

@route('/delete/<god_id>')
def delete(god_id):
    cur.execute("delete from god where god_id = "+ str(god_id))
    con.commit()
    return "God "+god_id + " Deleted </br> return to main <a href = \"/\">page</a>"

@route('/secondrelation/<god_id>')
def secondrelation(god_id):
    html = "<h2> Related Heroes </h2> <br /> <table>"
    for row in cur.execute ("select count(*) from hero where master_id={0}".format(god_id)):
        if row[0]==0:
            return "No Heroes Related to God "+str(god_id)+ "</br> return to main <a href = \"/\">page</a>"
    html+="<td> <b>Hero ID</b></td> <td> <b>Hero Name</b></td> <td> <b>Status(1=Dead,0=Alive)</b></td><td> <b>Trials</b></td> <td> <b>Body Count</b></td> <td> <b>Occupation</b> </td> <td> <b>Location</b> </td> <td> <b>Master ID</b> </td>"
    for row in cur.execute("select * from hero where master_id = {0} limit 20".format(god_id)):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
    html += "</table>"
    return html

@route('/insertsecondrelationtemp/<god_id>')
def insertytemp(god_id):
    html=""
    for row in cur.execute("select count (*) from hero where master_id != {0}".format(god_id)):
        if row[0]!=0:
            html += "<h2> Heroes Not Linked to God {0} </h2> <br /> <table>".format(god_id)
            html+="<td> <b>Hero ID</b></td> <td> <b>Hero Name</b></td> <td> <b>Status(1=Dead,0=Alive)</b></td><td> <b>Trials</b></td> <td> <b>Body Count</b></td> <td> <b>Occupation</b> </td> <td> <b>Location</b> </td> <td> <b>Master ID</b> </td> <td> <b>Link?</b> </td>"
            for row in cur.execute("select * from hero where master_id != {0} limit 20".format(god_id)):
                html += "<tr>"
                for cell in row:
                    html += "<td>" + str(cell) + "</td>"
                html += "<td><a href=\"/link/" + str(row[0]) +"/"+str(god_id)+ "\">Link?</a> </td>  </tr>"
            html += "</table>"
    html +="<br>"
    html += "<h2> Insert and Link New Hero to God {0} </h2>".format(god_id)
    route="/insertsecondrelation/{0}".format(god_id)
    html += '''
    <form action = '{0}' method = "post">
        Hero ID: <input name = "hero_id" type="text" />
        Name: <input name = "hero_name" type="text" />
        Status: <input name = "status" type="text" />
        Trials: <input name = "trials" type="text" />
        Body Count: <input name = "body_count" type="text" />
        Occupation: <input name = "occupation" type="text" />
        Location: <input name = "location" type="text" />
        <input value = "Insert and Link Hero!" type = "submit" />
    </form>
    '''.format(route)
    return html

@route('/link/<hero_id>/<god_id>')
def link(hero_id,god_id):
    cur.execute("update hero set master_id={0} where hero_id={1}".format(god_id,hero_id))
    con.commit()
    return "Hero "+str(hero_id) +  " Linked to God " + str(god_id)+" </br> return to main <a href = \"/\">page</a>"

@post('/insertsecondrelation/<god_id>')
def inserty(god_id):
    hero_id = request.forms.get('hero_id')
    hero_name = request.forms.get('hero_name')
    status = request.forms.get('status')
    trials = request.forms.get('trials')
    body_count = request.forms.get('body_count')
    occupation = request.forms.get('occupation')  
    location = request.forms.get('location')
    try:
        if hero_id=="" or hero_name=="" or status=="" or trials=="" or body_count=="" or occupation=="" or location=="":
            return "Invalid Entry. No Entry Made. Please Fill All Entries. </br> return to main <a href = \"/\">page</a>"
        if status!="0" and status!="1":
            return "Invalid Entry. No Entry Made. Status Should Only Be 0 or 1. </br> return to main <a href = \"/\">page</a>"
        if not hero_id.isnumeric() or not body_count.isnumeric() or not trials.isnumeric(): 
            return "Invalid Entry. No Entry Made. Please Make Sure Trials, Body Count and Hero ID Are Integers. </br> return to main <a href = \"/\">page</a>"
        cur.execute("insert into hero values ({0}, '{1}',{2},{3},{4},'{5}','{6}',{7})".format(hero_id, hero_name,status,trials,body_count,occupation,location,god_id))
        con.commit()
        return hero_name +  " linked to God " + str(god_id)+" </br> return to main <a href = \"/\">page</a>"
    except (sqlite3.IntegrityError):
        return "Invalid Entry. No Entry Made. Hero ID Already Exists. </br> return to main <a href = \"/\">page</a>"

run(host='localhost', port=8080, debug = True)