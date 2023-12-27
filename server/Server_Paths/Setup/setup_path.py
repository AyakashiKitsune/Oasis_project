from flask import Blueprint,request,jsonify
from werkzeug.utils import secure_filename
from packages.sql.sql_controller import Database

Setup_path = Blueprint("Setup_path",__name__)

@Setup_path.route("/")
def home():
    return "home setup"

@Setup_path.route('/create_database',methods=['POST','GET'])
def setup_create_datebase(db : Database,):
    
    return "createdb"
    

@Setup_path.route('/send_existing',methods=['POST'])
def setup_send_existing(Constants):
    file = request.files['file']
    file.save(Constants.UPLOAD_FOLDER + secure_filename(file.filename))
    return jsonify({
        'name': file.filename,
        'message' : 'file saved'
    })
    