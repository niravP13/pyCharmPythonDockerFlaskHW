from typing import Dict, List
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'sheet'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Grades Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM sheet')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, marks=result)


@app.route('/stats', methods=['GET'])
def charts_view():
    legend = 'Number of students with this Grade'
    labels = []
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT grade FROM sheet group by grade')
    for temp in cursor.fetchall():
        labels.append(list(temp.values())[0])
    labels = [i.replace('"', '') for i in labels]
    values = []
    values.append(0)
    cursor.execute('SELECT COUNT(*) FROM sheet group by grade')
    for temp in cursor.fetchall():
        values.append(list(temp.values())[0])
    result = cursor.fetchall()
    return render_template('chart.html', title='Home', player=result, student_labels=labels,
                           student_legend=legend,
                           student_values=values)


@app.route('/view/<string:lname>', methods=['GET'])
def record_view(lname):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM sheet WHERE lname=%s', lname)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', points=result[0])


@app.route('/edit/<string:lname>', methods=['GET'])
def form_edit_get(lname):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM sheet WHERE lname=%s', lname)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', points=result[0])


@app.route('/edit/<string:lname>', methods=['POST'])
def form_update_post(lname):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('lname'), request.form.get('fname'), request.form.get('ssn'),
                 request.form.get('test1'), request.form.get('test2'),
                 request.form.get('test3'), request.form.get('test4'), request.form.get('final'),
                 request.form.get('grade'), lname)
    sql_update_query = """UPDATE sheet t SET t.lname = %s, t.fname = %s, t.ssn = %s, t.test1 = 
    %s, t.test2 = %s, t.test3 = %s, t.test4 = %s, t.final = %s, t.grade = %s WHERE t.lname = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/marks/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Name Form')


@app.route('/marks/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('lname'), request.form.get('fname'), request.form.get('ssn'),
                 request.form.get('test1'), request.form.get('test2'),
                 request.form.get('test3'), request.form.get('test4'), request.form.get('final'),
                 request.form.get('grade'))
    sql_insert_query = """INSERT INTO sheet (lname,fname,ssn,test1,test2,test3,test4,final,grade) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<string:lname>', methods=['POST'])
def form_delete_post(lname):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM sheet WHERE lname = %s """
    cursor.execute(sql_delete_query, lname)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/marks', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM sheet')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/marks/<string:lname>', methods=['GET'])
def api_retrieve(lname) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM sheet WHERE lname=%s', lname)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/marks/<string:lname>', methods=['PUT'])
def api_edit(lname) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['lname'], content['fname'], content['ssn'],
                 content['test1'], content['test2'],
                 content['test3'], content['test4'], content['final'],
                 content['grade'],lname)
    sql_update_query = """UPDATE sheet t SET t.lname = %s, t.fname = %s, t.ssn = %s, t.test1 = 
        %s, t.test2 = %s, t.test3 = %s, t.test4 = %s, t.final = %s, t.grade = %s WHERE t.lname = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/marks', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['lname'], content['fname'], content['ssn'],
                 content['test1'], content['test2'],
                 content['test3'], content['test4'], content['final'],
                 request.form.get('grade'))
    sql_insert_query = """INSERT INTO sheet (lname,fname,ssn,test1,test2,test3,test4,final,grade) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/marks/<string:lname>', methods=['DELETE'])
def api_delete(lname) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM sheet WHERE lname = %s """
    cursor.execute(sql_delete_query, lname)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
