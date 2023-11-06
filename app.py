from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import csv
import os


app = Flask(__name__)


@app.route('/', methods=['GET'])

def hello():
    return "Hello Flask!"


@app.route('/location/', methods=['GET'])
def search_location():
    search = request.args.get('search')
    print("search::::::::**********", search)
    db_path = os.environ.get("DATABASE_URL")
    with sqlite3.connect(db_path) as location:
        cursor = location.cursor()
        cursor.execute(f'SELECT DISTINCT zc.code, zc.city, zc.lat, zc.lon, st.name as state_name, coun.name as country_name FROM zipcodes zc INNER JOIN states st \
                       ON zc.state_id=st.id INNER JOIN countries coun ON coun.id=st.country_id INNER JOIN counties cout ON cout.state_id=st.id\
                       WHERE zc.city LIKE "%{search}%" or st.name LIKE "%{search}%" or coun.name LIKE "%{search}%"')
        row_headers=[x[0] for x in cursor.description]
        rv = cursor.fetchall()
        json_data=[]
        for result in rv:
                json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)
    
  

if __name__ == '__main__':
    app.run()

# New addition for testing