from select import select
from flask import Blueprint,request,jsonify
from sqlalchemy import text
from werkzeug.utils import secure_filename
from packages.sql.sql_controller import database,Database
from packages.utils.utils import Constants
from packages.machine_learn_libs.Unitable import auto_column_test_predict

Setup_path = Blueprint("Setup_path",__name__)

@Setup_path.route("/")
def home():
    return "home setup"

@Setup_path.route('/create_database',methods=['POST'])
def setup_create_datebase():

    return "createdb"

@Setup_path.route('/send_existing',methods=['POST'])
def setup_send_existing():
    file = request.files['file']
    if file:
        file.save(Constants.UPLOAD_FOLDER + secure_filename(file.filename))
    return jsonify({
        'name': file.filename,
        'message' : 'file saved'
    }),200

@Setup_path.route('/csv_to_sql',methods=['POST'])
def setup_csv_to_sql():
    res = request.json
    filename = res['filename']
    nullcolumns = database.importTable(filename)
    if nullcolumns:
        return nullcolumns
    return jsonify({
        'message' : "ok",
        "nulls": 0
    })

@Setup_path.route('/predict_columns',methods=['GET'])
def setup_predict_columns():
    column_list = database.custom_command("""SELECT column_name
                            FROM information_schema.columns
                            WHERE table_schema = 'OasisBase' 
                            AND table_name = 'original_table';
                            """).scalars()
    # res are list[] of columns
    predicted_columns = auto_column_test_predict(column_list)
    # keys inside ^^^
    # 'key_column'
    # 'values'
    keys = [item['values'][0]['old'] for item in predicted_columns]
    query_sample = database.session.execute(text("""SELECT {} FROM original_table limit 10""".format(*keys))).fetchall()
    for i in query_sample:
        print(i)
    return jsonify([{'column' : keys[i],'samples' : [x[i] for x in query_sample]} for i in range(len(keys))])



    