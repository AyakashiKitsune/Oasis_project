from flask import Flask

from Server_Paths.Sales.sales_path import Sales_path
from Server_Paths.Inventory.inventory_path import Inventory_path
from Server_Paths.Setup.setup_path import Setup_path
from packages.utils.utils import Constants 

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = Constants.UPLOAD_FOLDER

app.register_blueprint(Sales_path,url_prefix= "/sales",)
app.register_blueprint(Inventory_path,url_prefix= "/inventory")
app.register_blueprint(Setup_path,url_prefix= "/setup")

if __name__ == '__main__':
    app.run(debug=True)