from flask import Blueprint,request,jsonify


from werkzeug.utils import secure_filename


Inventory_path = Blueprint("Inventory_path",__name__)

@Inventory_path.route("/")
def home():
    return "home Inventory_path"

@Inventory_path.route('/get_inventory/',methods=['GET'])
def get_inventory():
    pass

@Inventory_path.route('/savekill/<product>',methods=['GET'])
def analyze_savekill_product(product): 
    pass