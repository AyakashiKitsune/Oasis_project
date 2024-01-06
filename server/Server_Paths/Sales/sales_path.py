from flask import Blueprint
from packages.sql.sql_controller import Database
Sales_path = Blueprint("Sales_path",__name__)


@Sales_path.route("/")
def home():
    return ""

@Sales_path.route('/get_sales/<date>',methods=['POST'])
def get_sales(date):
    res = Database().readSalesOnDate(YYYYMMDD=date)
    return {
        [
           item.to_dict() for item in res
        ]
    }

@Sales_path.route('/get_sales/<fromdate>/<todate>',methods=['POST'])
def get_sales_between(fromdate,todate):
    res = Database().readSalesBetweendates(fromdate=fromdate,todate=todate)
    return {
        [
           item.to_dict() for item in res
        ]
    }

@Sales_path.route('/predict_sales/<duration>',methods=['POST'])
def predict_sales(duration):
    return ""

@Sales_path.route('/predict_sales/<product>/<duration>',methods=['POST'])
def predict_sales_of_product(duration):
    return ""