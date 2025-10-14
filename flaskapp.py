#run with
#python3.8 flaskapp.py
#NOT
#flask  --app flaskapp.py run

from flask import Flask, jsonify, request
#from phototag import *
#from phototag.LogDir.LogClass import Log
from Logger import *
from ImageTagger import *
import uuid
import os
import io
from WebResult import *
from PIL import Image


mn="flaskapp::main"

flaskInstance = Flask(__name__)

Log.Info(mn,"Method Entered")

tagger = ImageTagger()

UPLOAD_FOLDER='/opt/uploadtemp'
VALID_IMAGES=['JPEG','JPG','PNG','GIF','MPO']

@flaskInstance.route('/')
def hello_world():
   mn="flaskapp::hello_world"
   Log.Info(mn,"Method Entered")
   return 'Hello World'


@flaskInstance.route('/test')
def test():
   mn="flaskapp::test"
   Log.Info(mn,"Method Entered")
   rv=tagger.InferenceTest()
   Log.Info(mn,rv)
   return jsonify(rv)


@flaskInstance.route('/inference', methods = ['POST'])
def inference():
    mn="flaskapp::inference"
    Log.Info(mn,f"Method Entered {request}")
    rv = WebResult(0,0,"")

    Log.Info(mn,"a")

    try:

       if request.method != 'POST':
           Log.Info(mn,"Invalid method")
           rv.returnCode=1
           rv.message="Invalid Method"
           return rv.ToJSON()

       Log.Info(mn,"b")

       if 'file' not in request.files:
           Log.Info(mn,"No file posted")
           rv.returnCode=1
           rv.message="No file posted"
           print(rv.message)
           return rv.ToJSON()

       Log.Info(mn,"1")


       file=request.files['file']
       if file.filename == '':
           Log.Info(mn,"Inavlid filename")
           rv.returnCode=1
           rv.message="Invalid filename"
           return rv.ToJSON()

       Log.Info(mn,"2")

    
       Log.Info(mn,"3")
       imageData=file.read()
       imageStream=io.BytesIO(imageData)
       img=Image.open(imageStream)
       Log.Info(mn,f"{img.format} {img.mode} {img.width} {img.height}")

       if img.format not in VALID_IMAGES:
          raise Exception('Invalid image type')

       if img.width < 10 or img.height < 10:
          raise Exception("Invalid image dimensions")
       
    except Exception as ex:
       Log.Info(mn,f"EXCEPTION: {ex}")
       rv.message=str(ex)
       rv.returnCode=1
       #img.close()
       return rv.ToJSON()

    Log.Info(mn,"Starting Inference")
    tags=tagger.Inference(img)
    tags.update(rv.ToDictionary())
    #newFileName=str(uuid.uuid4())
    #file.save(os.path.join(UPLOAD_FOLDER, newFileName))
    Log.Info(mn,f"File tagged {tags}")
    rv.message=f"File tagger {tags}"
    return tags
    



#
#This allows you to run it from python flaskapp.py
#however the modle __init__ wount get called
#
if __name__ == '__main__':
    Log.Info(mn,"About to run")
    flaskInstance.run()
