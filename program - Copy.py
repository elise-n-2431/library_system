import sqlite3
from flask import Flask, Response, render_template, abort, g, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash  

app= Flask(__name__)
#adding in a line here

DATABASE = 'db/library.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():

  return render_template("main1.html")

@app.route("/route")
def route():
  return render_template("route1.html")

@app.route("/catalogue")
def catalogue():
  cursor=get_db().cursor()
  sql1="SELECT * FROM Book"
  cursor.execute(sql1)
  results=cursor.fetchall()
  sql2="SELECT BookID FROM MiddleTable"
  cursor.execute(sql2)
  match=cursor.fetchall()
  return render_template("catalogue.html",results=results,match=match)

@app.route("/book/<int:id>")
def book(id):
  cursor=get_db().cursor()
  sql1="SELECT * FROM Book WHERE ID=?"
  cursor.execute(sql1,(id,))
  results=cursor.fetchall()[0]
  return render_template("book.html",id=id,results=results)

@app.route("/login", methods=['POST'])
def issuebook():
  book=request.form['book']
  number=request.form['number']
  username=request.form['username']
  password=request.form['password']
  password=str(password)
  number=str(number)
  cursor=get_db().cursor()
  sql="SELECT Password FROM Student WHERE ID=?"
  cursor.execute(sql,(username,))
  results=cursor.fetchall()
  for item in results:
    thing=check_password_hash(item[0],password)
    if thing==True:
      sql2="INSERT INTO MiddleTable(StudentID,BookID) VALUES(?,?)"
      cursor.execute(sql2,(username,number))
      sql3="UPDATE Book SET Avaliable=1 WHERE ID=?"
      cursor.execute(sql3,(number))
      get_db().commit()
      return render_template("success.html",book=book)
    else:
      return render_template("failure.html", number=number)
  return render_template("failure.html", number=number)

if __name__ == "__main__":
  app.run(debug=True)
