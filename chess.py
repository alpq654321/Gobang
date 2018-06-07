#利用p存储当前在线玩家，利用X，Y，Z存储下棋的情况，Dict存储请求对战，Dict2存储是否正在对战，Dict3表示拒绝信息，Dict4表示接受信息
X = {}
Y = {}
Z = {}
p = []
Dict = {}
Dict2 = {}
Dict3 = {}
Dict4 = {}
from flask import Flask,render_template,request
app=Flask(__name__)
import sqlite3
@app.route("/register",methods=['POST'])
def register():  #注册用户，存入数据库中，如果已被注册提示给客户端
	username = request.form.get('username', '')
	password = request.form.get('password', '')
	dbConn = sqlite3.connect('match.db')
	data = dbConn.execute("select username, password from tbMatch")
	FLAG = 0
	for i in data:
		if i[0]==username:
			FLAG=1
	from flask import jsonify
	if FLAG == 1:
		return jsonify("该用户已被注册！！")
	dbConn.execute('''insert into tbMatch
						  (username,password)
						  values('{}','{}')'''.format(username,password))
	dbConn.commit()
	return jsonify("注册成功！！请登录！！")
	
@app.route("/submit",methods=['POST']) #登录用户，检查是否有用户，密码是否正确
def submit():
	username = request.form.get('username', '')
	password = request.form.get('password', '')
	dbConn = sqlite3.connect('match.db')
	data = dbConn.execute("select username, password from tbMatch")
	FLAG = 0
	for i in data:
		if i[0]==username:
			FLAG=1
	from flask import jsonify
	if FLAG == 0:
		return jsonify("没有该用户名！！")
	data = dbConn.execute("select username, password from tbMatch")
	FLAG = 0
	for i in data:
		if (i[0]==username) and (i[1]!=password):
			FLAG=1
	if FLAG == 1:
		return jsonify("密码错误！！")
	p.append(username)
	X[username] = [1]
	Y[username] = [20]
	Z[username] = [20]
	return jsonify("ojbk")
	
@app.route('/loginInfo',methods=['get','post']) #获取已登录的用户的用户名并在客户端显示
def loginInfo():
	global p
	loginStr=''
	loginList=[]
	for item in p:
		loginList.append(item)
		loginStr=','.join(loginList)
	return loginStr
	
@app.route('/inform',methods=['get','post']) #利用Dict获取所有对战请求
def inform():

	loginStr=''
	loginList=[]
	for i in Dict:
		if Dict[i]!="":
			loginList.append(i)
			loginStr=','.join(loginList)
			loginList.append(Dict[i])
			loginStr=','.join(loginList)
	return loginStr

@app.route("/confirm",methods=['POST']) #接受本次对战请求，存入Dict2和Dict4中，清空Dict
def confirm():  
	from flask import jsonify
	first = request.form.get('first', '')
	second = request.form.get('second', '')
	Dict[first]=""
	Dict2[first]=second
	Dict4[first]=second
	return jsonify("")

@app.route("/refuse",methods=['POST']) #拒绝本次对战请求，存入Dict3，清空Dict
def refuse():  
	from flask import jsonify
	first = request.form.get('first', '')
	second = request.form.get('second', '')
	Dict3[first]=second
	Dict[first]=""
	return jsonify("")
	
@app.route("/invite",methods=['POST']) #邀请对方和自己打，此时需要判断对方是否正在游戏或者正在被邀请
def invite():
	first = request.form.get('first', '')
	second = request.form.get('second', '')
	FLAG= False;
	if (second in Dict) and (Dict[second]!=""): FLAG=True
	if (second in Dict2) and (Dict2[second]!=""): FLAG=True
	for i in Dict:
		if Dict[i]==second: FLAG=True
	for i in Dict2:
		if Dict2[i]==second: FLAG=True
	from flask import jsonify
	if FLAG==True:
		return jsonify("NO！！")
	Dict[first]=second
	return jsonify("对方正在思考要不要和你打")
	
@app.route('/accept/<info>',methods=['get','post']) #判断对方是否接受请求
def accept(info):
	from flask import jsonify
	for i in Dict4:
		if Dict4[i]==info:
			return jsonify(i)
	if info in Dict4:
		return jsonify(Dict4[info])
	else:
		return jsonify("")
	

@app.route('/wrong',methods=['get','post']) #判断对方是否拒绝请求
def wrong():

	loginStr=''
	loginList=[]
	for i in Dict3:
		if Dict3[i]!="":
			loginList.append(i)
			loginStr=','.join(loginList)
			loginList.append(Dict3[i])
			loginStr=','.join(loginList)
	return loginStr
				
@app.route("/acceptafter",methods=['POST']) #接受请求后清空Dict4
def acceptafter():
	first = request.form.get('first', '')
	second = request.form.get('second', '')
	Dict4[first]=""
	from flask import jsonify
	return jsonify("")

@app.route("/wrongafter",methods=['POST']) #拒绝请求后清空Dict3
def wrongafter():
	first = request.form.get('first', '')
	second = request.form.get('second', '')
	Dict3[first]=""
	from flask import jsonify
	return jsonify("")
	

	

@app.route("/black/<info>")  #开始游戏！黑方，告知前端对战双方分别是谁
def black(info):
	user=info.split('_')[0]
	user2=info.split('_')[1]
	return render_template("game.html",text="1",user_name="'"+user+"'",en_emy="'"+user2+"'")

@app.route("/white/<info>") #白方
def white(info):
	user=info.split('_')[0]
	user2=info.split('_')[1]
	return render_template("game.html",text="0",user_name="'"+user+"'",en_emy="'"+user2+"'")
	
@app.route('/who/<username>',methods=['get','post']) #告诉客户端上一步是谁下的，以及位置在哪里
def who(username):
	loginStr=''
	loginList=[]
	loginList.append(str(X[username][len(X[username])-1]))
	loginStr=','.join(loginList)
	loginList.append(str(Y[username][len(Y[username])-1]))
	loginStr=','.join(loginList)
	loginList.append(str(Z[username][len(Z[username])-1]))
	loginStr=','.join(loginList)
	return loginStr

@app.route("/next",methods=['POST'])  #客户端告诉服务器它下在哪里了
def next():
	user1=request.form.get('user1','')
	user2=request.form.get('user2','')
	X[user1].append(request.form.get('who', ''))
	Y[user1].append(request.form.get('X', ''))
	Z[user1].append(request.form.get('Y', ''))
	X[user2].append(request.form.get('who', ''))
	Y[user2].append(request.form.get('X', ''))
	Z[user2].append(request.form.get('Y', ''))
	
	from flask import jsonify
	return jsonify("ojbk")

@app.route("/finish",methods=['POST']) #结束这个游戏时双方退出登录，以及清空Dict2
def finish():
	username=request.form.get('username', '')
	if username in Dict2: Dict2[username]=""
	for i in Dict2:
		if Dict2[i]==username:
			Dict2[i]=""
	global p
	q=[]
	for i in p:
		if i!=username:
			q.append(i)
	p=q
	from flask import jsonify
	return jsonify("ojbk")
	
@app.route("/")
def root():
	return render_template("chess.html")
		
if __name__=="__main__":
	app.run(host="0.0.0.0",port=8000,debug=True)