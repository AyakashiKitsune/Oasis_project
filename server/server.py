import os
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import tensorflow as tf

class Constants:
    supported_data = ['csv','xls']
    UPLOAD_FOLDER = os.getcwd() +  '/uploads/'
    MODELS = os.getcwd() +  '/datamodels/'
    DATABASE = os.getcwd() + '/database/'

class Setup:
    response = [
        'message', # choice of 2 get database by [!fetch through api!, from file, create new]
        'file'
    ]
    
    def from_file_db(file):
        format = file.split('.')[-1]
        if format in Constants.supported_data:
            # if supported, scrape all , run model 
            
            pass
        else:
            # if not reject, send error response
            pass

    def create_new_db(sales_tablename, inventory_tablename):
        pass
        
        

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = Constants.UPLOAD_FOLDER

@app.route('/setup/create_database',methods=['POST'])
def setup_create_datebase():
    datas = request.get_json()
    table_name = datas['name_db'] 
    sales = datas['name_sales'] 
    inventory = datas['name_inventory']
    
    Setup.create_new_db(
        sales_tablename=sales,
        inventory_tablename=inventory)
    
    return jsonify({'message' : 'table is created'})

@app.route('/setup/send_existing',methods=['POST'])
def setup_send_existing():
    file = request.files['file']
    file.save(Constants.UPLOAD_FOLDER + secure_filename(file.filename))
    return jsonify({
        'name': file.filename,
        'message' : 'file saved'
    })



@app.route('/sales',methods=['GET'])
def specific_sales_date():
    return ""
    
if __name__ == '__main__':
    app.run(debug=True)