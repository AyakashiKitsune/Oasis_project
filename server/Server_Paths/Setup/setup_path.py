from select import select
from flask import Blueprint,request,jsonify
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
    # 'actual_column_name' 
    # 'actual_encoded' 
    # 'predicted' 
    # 'predicted_decoded' 
    # 'predicted_decoded_str' 
    
    return jsonify(predicted_columns)



    