import pymysql
from flask import Flask,render_template,redirect,url_for,session,request
app=Flask(__name__)
app.secret_key='hedge'
@app.route('/',methods=['POST','get'])
def index():
    try:
        if session['user_id']:
            return redirect(url_for('welcome'))
    except (KeyError):
        conn=pymysql.connect(user='root',password='',host='localhost',db='users')
        cur=conn.cursor()
        if request.method=='POST':
            user=request.form['username']
            passw=request.form['password']
            sqlsignup=("insert into users(username,password) values(%s,%s)")
            cur.execute(sqlsignup,(user,passw))
            session['user_id']=user
            return redirect(url_for('welcome'))
        conn.close()
    return render_template('index.html')
@app.route('/welcome')
def welcome():
    conn=pymysql.connect(user='root',password='',host='localhost',db='users')
    cur=conn.cursor()
    user=session['user_id']
    welcome="select * from accounts where user=%s"
    cur.execute(welcome,(user))
    a=cur.fetchall()
    lis=[0]*len(a)
    for i in range(len(a)):
        lis[i]=a[i][1]
    conn.close
    return render_template('welcome.html',lis=lis)
@app.route('/login',methods=['POST','get'])
def login():
    try:
        if session['user_id']:
            return redirect(url_for('welcome'))
    except (KeyError):
        conn=pymysql.connect(user='root',password='',host='localhost',db='users')
        cur=conn.cursor()

        if request.method=='POST':
            user=request.form['username']
            passw=request.form['password']
            logincheck="select username,password from users where username=%s and password=%s"
            a=cur.execute(logincheck,(user,passw))
            l=cur.fetchone()
            if l[0]==user and l[1]==passw:
                session['user_id']=user
                return redirect(url_for('welcome'))
            else:
                return redirect(url_for('login'))

 
        conn.close()           
    return render_template('login.html')

            

@app.route('/expand/<acc>')
def exp(acc):
    user=session['user_id']
    conn=pymysql.connect(user='root',password='',host='localhost',db='users')
    cur=conn.cursor()
    expan="select account,username,password from accounts where user=%s and account=%s"
    cur.execute(expan,(user,acc))
    fe=cur.fetchone()
    usern=fe[1]
    passwor=fe[2]
    
    
    conn.close()
    return render_template('expand.html',acc=acc,usern=usern,passwor=passwor)
    
@app.route('/add',methods=['POST','GET'])
def add():
    conn=pymysql.connect(user='root',password='',host='localhost',db='users')
    cur=conn.cursor()
    if request.method=='POST':
        user=session['user_id']
        account=request.form['account_name']
        username=request.form['username']
        password=request.form['password']
        addacc="insert into accounts values(%s,%s,%s,%s)"
        cur.execute(addacc,(user,account,username,password))
        conn.close()
        return redirect(url_for('welcome'))
    return render_template('addon.html')
@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect(url_for('login'))

@app.route('/delete/<acc>')
def delete(acc):
    try:
        uid=session['user_id']
        conn=pymysql.connect(user='root',password='',host='localhost',db='users')
        cur=conn.cursor()
        sqldel='update accounts set user=null,password=null,username=null,account=null where user=%s and account=%s'
        cur.execute(sqldel,(uid,acc))
        return redirect(url_for('welcome'))
    except (Keyerror):
        return redirect(url_for('/login'))
    

if __name__=='__main__':
    app.run()
