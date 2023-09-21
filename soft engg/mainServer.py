
#imports
import os
from flask import Flask, render_template, url_for, request, jsonify
from mydb import mydb

app = Flask(__name__)
db = mydb()

@app.route('/')
def start():
    # print("test2")
    return render_template('strt.html')

@app.route('/about')
def about():
    return render_template('abt.html')

@app.route('/main')
def main():
    return render_template('eqt.html')

@app.route('/update', methods = ['POST', 'GET'])
def update():
    global db
    if request.method == "POST":
        data = request.get_json()
        if len(data["boxNo"]) == 0:
            r = db.getall()
            print(r)
            return jsonify(r)
        elif len(data["boxNo"]) == 1:
            l1, l2 = db.getOne(data["boxNo"][0], data["value"])
            return jsonify([l1, l2])
        elif len(data["boxNo"]) == 2:
            print("values: ", type(data["boxNo"][0]), type(data["boxNo"][1]), data["value"][0], data["value"][1])
            r1, r2, r3, r4 = db.getTwo(data["boxNo"][0], data["boxNo"][1], data["value"][0], data["value"][1])
            return jsonify([r1, r2, r3, r4])

if __name__ == '__main__':
    
    # print("test")
    app.run()
