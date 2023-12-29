# import requests
# import base64
# url = 'http://127.0.0.1:5000/'
# destination = f'{url}setup'

data = {
    "message" : "do something",
    'error' : "something went wrong"
}

# response = requests.post(destination,json=data,)
# print(response)

from sqlalchemy import text
from packages.sql import sql_controller

db = sql_controller.Database()
res = db.session.execute(text("""SELECT label,name FROM original_table limit 10;""")).fetchall()
print([x for x in res[0]])


# def line_analysis(lines):
#     chopped = [line.replace('\n','').split(',') for line in lines]
#     return chopped

# def prettified_word(words):
#     return [word.replace('(','').replace(')','') for word in[word.replace(' ','_') if ' ' in word else word for word in words]]

# from datetime import datetime

# def is_date(string):
#     formats_to_check = [
#         "%Y-%m-%d",  # YYYY-MM-DD
#         "%Y/%m/%d",  # YYYY/MM/DD
#         "%m/%d/%Y",  # MM/DD/YYYY
#         "%d-%m-%Y",  # DD-MM-YYYY
#         # Add more formats as needed
#     ]
#     for fmt in formats_to_check:
#         try:
#             datetime.strptime(string, fmt)
#             return True
#         except ValueError:
#             pass
#     return False
# with open('newlongIowaLiqourfixed.csv') as input_file:
#     head = [next(input_file) for _ in range(2)]
#     head = line_analysis(head)
#     columns = prettified_word(head[0])
#     data = head[1]
#     date = [is_date(i) for i in data]
#     print(date.index(True))
#     print(columns)
    


# # import subprocess
# # test = subprocess.Popen(["ls","-l"], stdout=subprocess.PIPE)
# # output = test.communicate()[0]
# # print(output)

# # from subprocess import call
# # call(["mkdir","chunked"])
# # call(["split","--verbose","-l","50000","newlongIowaLiqourfixed.csv", "chunked/"])

# # print(columns)