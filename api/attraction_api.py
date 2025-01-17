import sys,os
from flask import *
sys.path.append("..")
from sql import  mysql_select
import mysql.connector
from dotenv import load_dotenv

## 資料庫敏感性資料
load_dotenv()

# api路由
appAttraction = Blueprint('attraction_api', __name__)

@appAttraction.route('/attractions')
def attractions():
	if request.args.get('page'):
		page = request.args.get('page')
		page=int(page)
		index = page * 12
		next_page_JSON = page + 1
		if request.args.get('keyword'):
			keyword =request.args.get('keyword')
			attraction_JSON = mysql_select(f"SELECT * FROM attraction WHERE name LIKE '%{keyword}%' LIMIT {index},12")
			next_list= mysql_select(f"SELECT * FROM attraction WHERE name LIKE '%{keyword}%' LIMIT {index + 12}, 12")
			if len(next_list) == 0:
				next_page_JSON = None
			data = {"nextPage": next_page_JSON,"data": attraction_JSON}
			return jsonify(data)
		else:
			attraction_JSON = mysql_select(f"SELECT * FROM attraction LIMIT {index}, 12")
			next_list = mysql_select(f"SELECT * FROM attraction LIMIT {index + 12}, 12")
			print("目前頁面:",page)
			if index+1<320:
				print("起始ID:",index+1)
			if len(next_list) == 0:
				next_page_JSON = None
			data = {"nextPage": next_page_JSON,"data": attraction_JSON}
			return jsonify(data)
	return {"error": True,"message": "伺服器內部錯誤"}, 500

@appAttraction.route('/attraction/<int:ID>')
def api_attraction(ID):
	if ID:
		conn = conn=mysql.connector.connect(host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),password=os.getenv("SERVER_PASSWORD"), database = "taipei",charset = "utf8",auth_plugin='mysql_native_password')
		cursor = conn.cursor()
		cursor.execute(f"SELECT * FROM attraction where id={ID}")
		data = cursor.fetchone()
		if data:
			attraction = {"data": dict(zip(cursor.column_names, data))}
			attraction['data']['images'] = json.loads(data[9])
			
			return attraction
		return jsonify({ "error": True, "message": "景點編號不正確" })
	
	return jsonify({ "error": True, "message": "伺服器內部錯誤" })


# 調整目錄導向。
# 
# from sql import cursor, conn , mysql_select
# from os.path import dirname,abspath
# directory=dirname(dirname(abspath(__file__)))
# sys.path.append(directory)