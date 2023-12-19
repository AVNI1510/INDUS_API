from flask import Flask, request, jsonify, render_template,url_for, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(host="127.0.0.1", user="root", password="Bavni@15#10", database="indus_API")

@app.route("/output", methods=["post"])
def output():
    logtime = request.form["logtime"]
    print(logtime)

    if not logtime:
        return jsonify({'error': 'Logtime parameters are required'})

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM beam_data WHERE logtime=%s", (logtime,))
        results = cursor.fetchall()
        print(results)

        data = []
        for row in results:
            data.append({'logtime': row[0], 'beam_current': row[1], 'beam_energy': row[2]})
            dict={}
            dict['key']=data

            cursor.close()
            db.close()

            if not data:
                return jsonify({'error': 'No results found'})

            return jsonify(dict)
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)})

@app.route("/diff", methods=["POST"])
def diff():
    start_logtime = request.form.get("start_logtime")
    end_logtime = request.form.get("end_logtime")
    print(start_logtime, end_logtime)

    if not start_logtime or not end_logtime:
        return jsonify({'error': 'Start Logtime and End Logtime parameters are required'})

    try:
        cursor = db.cursor()
        cursor.execute("SELECT logtime as `Starting Logtime`, beam_current, beam_energy FROM beam_data WHERE logtime BETWEEN %s AND %s", (start_logtime, end_logtime))
        results = cursor.fetchall()
        print(results)

        data = []
        for row in results:
            data.append({'logtime': row[0], 'beam_current': row[1], 'beam_energy': row[2]})

        cursor.close()

        if not data:
            return jsonify({'error': 'No results found'})

        return jsonify({'data': data})
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)})

if __name__ == "__main__":
    app.run(debug=True)