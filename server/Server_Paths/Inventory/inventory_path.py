from flask import Blueprint,request,jsonify


from werkzeug.utils import secure_filename


Inventory_path = Blueprint("Inventory_path",__name__)

@Inventory_path.route("/")
def home():
    return "home Inventory_path"