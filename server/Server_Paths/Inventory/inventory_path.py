from flask import Blueprint,request,jsonify
from packages.machine_learn_libs.savekillanalysis import analyze_savekilling,analyze_stocking

from werkzeug.utils import secure_filename


Inventory_path = Blueprint("Inventory_path",__name__)

@Inventory_path.route("/")
def home():
    return "home Inventory_path"

@Inventory_path.route('/get_inventory/',methods=['GET'])
def get_inventory():
    return ""

@Inventory_path.route('/savekill',methods=['GET'])
def analyze_savekill(): 
    return analyze_savekilling()

@Inventory_path.route('/stock_analysis',methods=['GET'])
def analyze_stocks(): 
    return analyze_stocking()