
from flask import Flask, jsonify, request
from Logger import *

flaskInstance = Flask(__name__)

@flaskInstance.route('/')
def hello_world():
   mn="flaskapp::hello_world"
   Log.Info(mn,"Method Entered")
   return 'Hello World'


@flaskInstance.route('/inference', methods = ['POST'] )
def test():
   mn="flaskapp::test"
   Log.Info(mn,"Method Entered")
   Log.Info(mn,f"Method Entered {request}")
   Log.Info(mn,request.get_data())
   for header, value in request.headers.items():
       print(f"HDR: {header}: {value}")
   
   #Log.Info(mn,dict(request.form))
   if 'file' not in request.files:
       Log.Info(mn,"No file posted")

   for key, value in request.form.items():
       print(f"Form field: {key}, Value: {value}")

   

   #Log.Info(mn,rv)
   return "OK"


#
#This allows you to run it from python flaskapp.py
#however the modle __init__ wount get called
#
if __name__ == '__main__':
    print("About to Run")
    flaskInstance.run()

