from flask import Blueprint,request,jsonify


from werkzeug.utils import secure_filename


Inventory_path = Blueprint("Inventory_path",__name__)

@Inventory_path.route("/")
def home():
    return "home Inventory_path"

@Inventory_path.route('/get_sales/<date>',methods=['POST'])
def get_inventory(date):
    pass

@Inventory_path.route('/predict_sales/<duration>',methods=['POST'])
def predict_inventory(duration):
    pass

@Inventory_path.route('/predict_sales/<product>/<duration>',methods=['POST'])
def analyze_sale_notsale_product(duration): 
    pass