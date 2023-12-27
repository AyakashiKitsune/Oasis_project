from flask import Blueprint

Sales_path = Blueprint("Sales_path",__name__)


@Sales_path.route("/")
def home():
    return "home Sales_path"

@Sales_path.route('/get_sales_on_date',methods=['GET'])
def get_sales_on_date():
    return ""