from flask import Flask, render_template, request, redirect, url_for, session
import random, time


app=Flask(__name__)
app.secret_key = "supersecretkey"
server_start_time = str(time.time())
@app.route("/")
def index():
    if "table" not in session or session.get("server_start_time") != server_start_time:
        table=set_table()
        session["table"]=table
        session["server_start_time"]=server_start_time
    else:
        table=session["table"]
    return render_template("index.html", table=table)

@app.route("/reset")
def reset():
    session.pop("table", None)
    return redirect(url_for("index"))

@app.route("/move/<dir>")
def move(dir):
    table=session["table"]
    table_copy = [r[:] for r in table]
    if dir=="left":
        table=left_drag(table)
    if dir=="right":
        table=right_drag(table)
    if dir=="up":
        table=up_drag(table)
    if dir=="down":
        table=down_drag(table)

    if table!=table_copy:
        start_state(table)
    session["table"]=table
    if end(table): 
        return render_template("end.html", table=table)
    return redirect(url_for("index"))

def start_state(table):
    count=0
    while True:
        x=random.randint(0,3)
        y=random.randint(0,3)
        if table[x][y] == 0:
            table[x][y]=random.choice([2,4])
            count=count+1
        if count==1:
            break

def set_table():
    table=[[0 for i in range(4)] for j in range(4)]
    start_state(table)
    start_state(table)
    return table

def l_movement(r):
    r_compressed=[x for x in r if x!=0]
    n=len(r_compressed)
    i=0
    while i<n-1:
        if(r_compressed[i] == r_compressed[i+1]):
            r_compressed[i]=r_compressed[i]+r_compressed[i+1]
            r_compressed[i+1]=0
            i=i+2
        else:
            i=i+1
    
    r_compressed_1=[y for y in r_compressed if y!=0]
    while len(r_compressed_1)<len(r):
        r_compressed_1.append(0)
    
    return r_compressed_1
def r_movement(r):
    r_updated=l_movement(r[::-1])[::-1]
    return r_updated

def left_drag(table):
    table_updated=[l_movement(r) for r in table]
    return table_updated

def right_drag(table):
    table_updated=[r_movement(r) for r in table]
    return table_updated

def down_drag(table):
    table_transposed = [list(row) for row in zip(*table)]

    table_updated=[r_movement(r) for r in table_transposed]
    return [list(row) for row in zip(*table_updated)]

def up_drag(table):
    table_transposed = [list(row) for row in zip(*table)]

    table_updated=[l_movement(r) for r in table_transposed]
    return [list(row) for row in zip(*table_updated)]

def end(table):
    if any(0 in r for r in table):
        return False
    for x in range(0,4):
        for y in range(0,4):
            if x<3 and table[x][y]==table[x+1][y]:
                return False
            if y<3 and table[x][y]==table[x][y+1]:
                return False
    return True

if __name__ == "__main__":
    app.run(debug=True)