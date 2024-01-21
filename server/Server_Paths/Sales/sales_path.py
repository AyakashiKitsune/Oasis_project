from flask import Blueprint, request
from packages.sql.sql_controller import Database
Sales_path = Blueprint("Sales_path",__name__)


@Sales_path.route("/")
def home():
    return ""

@Sales_path.route('/get_sales/<date>',methods=['GET'])
def get_sales(date):
    wholesale = request.args.get("wholesale") # 1 - 0
    if wholesale == "true": # 1
        res = Database().readSalesOnDate(YYYYMMDD=date,wholesale=True)
    else:
        res = Database().readSalesOnDate(YYYYMMDD=date)
    return res

@Sales_path.route('/get_sales/<fromdate>/<todate>',methods=['GET'])
def get_sales_between(fromdate,todate):
    wholesale = request.args.get("wholesale") # 1 - 0
    if wholesale == "true": # 1
        res = Database().readSalesBetweendates(fromdate=fromdate,todate=todate,wholesale=True)
    else:
        res = Database().readSalesBetweendates(fromdate=fromdate,todate=todate)
    return res

@Sales_path.route('/predict_wholesales/<duration>',methods=['GET'])
def predict_wholesales(duration):
    
    
    return ""

@Sales_path.route('/predict_sales/<product>',methods=['GET'])
def predict_sales_of_product():
    return ""