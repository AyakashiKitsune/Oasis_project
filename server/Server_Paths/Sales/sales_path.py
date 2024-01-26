import select
from flask import Blueprint, jsonify, request
from packages.sql.sql_controller import Database
from packages.machine_learn_libs.sold_items_tomorrow import wholesales_prediction
Sales_path = Blueprint("Sales_path",__name__)


@Sales_path.route("/")
def home():
    return ""

@Sales_path.route("/overview",methods= ['GET'])
def overview():
    fourteen_days_wholesales,seven_days_wholesales,sold_count_product,total_sales_year,total_sold_year = Database().overview_query()
    return {
        "fourteen_days_wholesales" : fourteen_days_wholesales ,
        "seven_days_wholesales" : seven_days_wholesales ,
        "sold_count_product" : sold_count_product,
        "total_sales_year" : total_sales_year ,
        "total_sold_year" : total_sold_year  
    } 

@Sales_path.route('/recent_date',methods=['GET'])
def recent_date():
    res,res1 = Database().recent_date()
    return {
        'min_date' : res1,
        'max_date' : res
    }

@Sales_path.route('/get_sales/<date>',methods=['GET'])
def get_sales(date):
    wholesale = request.args.get("wholesale") # 1 - 0
    if wholesale == "true": # 1
        res = Database().readSalesOnDate(YYYYMMDD=date,wholesale=True)
    else:
        res = Database().readSalesOnDate(YYYYMMDD=date)
    return res

@Sales_path.route('/get_recent_sales',methods=['GET'])
def get_recent_sales():
    wholesale = request.args.get("wholesale") # 1 - 0
    if wholesale == "true": # 1
        res = Database().readSalesRecent(wholesale=True)
    else:
        res = Database().readSalesRecent()
    return res

@Sales_path.route('/get_sales/<fromdate>/<todate>',methods=['GET'])
def get_sales_between(fromdate,todate):
    wholesale = request.args.get("wholesale") # 1 - 0
    if wholesale == "true": # 1
        res = Database().readSalesBetweendates(fromdate=fromdate,todate=todate,wholesale=True)
    else:
        res = Database().readSalesBetweendates(fromdate=fromdate,todate=todate)
    return res

@Sales_path.route('/predict_wholesales',methods=['POST'])
def predict_wholesales():
    json = request.json
    res = wholesales_prediction(json['duration'])
    return res

@Sales_path.route('/predict_sales/<product>',methods=['GET'])
def predict_sales_of_product():
    return ""