from flask import Flask, request, jsonify, render_template, url_for, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(host="127.0.0.1", user="root", password="Bavni@15#10", database="indus_API")

@app.route("/set", methods=["post"])
def set():
    logtime = request.form["logtime"]
    power_supply = int(request.form["power_supply"])
    print(logtime, power_supply)

    if not logtime or not power_supply:
        return jsonify({'error': 'Logtime and Power Supply Parameters are required'})

    try:
        cursor = db.cursor()
        cursor.execute("SELECT p{}_setvalue, logtime FROM mps_data WHERE logtime=%s".format(power_supply), (logtime,))
        results = cursor.fetchall()
        print(results)

        data = []
        for row in results:
            data.append({'Logtime': row[1], 'Set Value': row[0], 'Power Supply Number': power_supply})
            
        cursor.close()
        db.close()

        if not data:
            return jsonify({'error': 'No Results Found'})

        return jsonify({'data': data})
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)})


@app.route("/value", methods=["POST"])
def value():
    start_logtime = request.form.get("start_logtime")
    end_logtime = request.form.get("end_logtime")
    power_supply = int(request.form["power_supply"])
    print(start_logtime, end_logtime, power_supply)

    if not start_logtime or not end_logtime or not power_supply:
        return jsonify({'error': 'Starting Logtime, Ending Logtime and Power Supply parameters are required'})
    try:
        cursor = db.cursor()
        cursor.execute("SELECT logtime as Starting_Logtime, logtime as Ending_Logtime, p{}_setvalue as Set_Value FROM mps_data WHERE logtime BETWEEN %s AND %s".format(power_supply), (start_logtime, end_logtime))
        results = cursor.fetchall()
        print(results)
        
        data = []
        for row in results:
            data.append({'Logtime': row[0],'Set Value': row[2], 'Power Supply Number': power_supply})
        cursor.close()
        if not data:
            return jsonify({'error': 'No Results Found'})
        return jsonify({'data': data})

    except mysql.connector.Error as error:
        return jsonify({'error': str(error)})

if __name__=="__main__":
    app.run(debug=True)    