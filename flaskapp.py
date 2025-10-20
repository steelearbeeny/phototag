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
from pillow_heif import register_heif_opener
from FaceProcessor import *


mn="flaskapp::main"

flaskInstance = Flask(__name__)

Log.Info(mn,"Method Entered")

tagger = ImageTagger()
register_heif_opener()

UPLOAD_FOLDER='/opt/uploadtemp'
VALID_IMAGES=['JPEG','JPG','PNG','GIF','MPO','HEIF' ]

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


def getimage(request):
    mn="flaskapp::getimage"
    Log.Info(mn,f"Method Entered {request}")
    #Log.Info(mn,request.get_data(cache=False))
    #Log.Info(mn,dict(request.form))
    
    rv = WebResult(0,0,"")

    #Log.Info(mn,"a")

    try:

       if request.method != 'POST':
           Log.Info(mn,"Invalid method")
           rv.returnCode=1
           rv.message="Invalid Method"
           return rv.ToDictionary()

       #Log.Info(mn,"b")

       if 'file' not in request.files:
           Log.Info(mn,"No file posted")
           rv.returnCode=1
           rv.message="No file posted"
           #print(rv.message)
           return rv.ToDictionary()

       #Log.Info(mn,"1")


       file=request.files['file']
       if file.filename == '':
           Log.Info(mn,"Inavlid filename")
           rv.returnCode=1
           rv.message="Invalid filename"
           return rv.ToDictionary()

       #Log.Info(mn,"2")

    
       #Log.Info(mn,"3")
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
       return rv.ToDictionary()

    newDict=rv.ToDictionary()
    newDict["image"]=img
    return newDict


def gettags(img):
    mn="flaskapp::gettags"

    Log.Info(mn,"Starting Inference")
    tags=tagger.Inference(img)
    #tags.update(rv.ToDictionary())
    #newFileName=str(uuid.uuid4())
    #file.save(os.path.join(UPLOAD_FOLDER, newFileName))
    Log.Info(mn,f"File tagged {tags}")
    #rv.message=f"File tagger {tags}"
    return tags   

@flaskInstance.route('/inference', methods = ['POST'])
def inference():
    mn="flaskapp::inference"
    Log.Info(mn,f"Method Entered {request}")
    rv = WebResult(0,0,"")

    caption=0
    face=0
    #Log.Info(mn,"a")
    #Check for the form variables

    if 'userid' not in request.form:
       Log.Info(mn,"Missing userid")
       rv.returnCode=1
       rv.message="Missing userid"
       #print(rv.message)
       return rv.ToDictionary()

    userid=request.form['userid']

    if 'uniqueid' not in request.form:
       Log.Info(mn,"Missing uniqueid")
       rv.returnCode=1
       rv.message="Missing uniqueid"
       #print(rv.message)
       return rv.ToDictionary()

    if 'guid' not in request.form:
       Log.Info(mn,"Missing guid")
       rv.returnCode=1
       rv.message="Missing guid"
       return rv.ToDictionary()

    guid=request.form['guid']

    if 'name' not in request.form:
       Log.Info(mn,"Missing filename")
       rv.returnCode=1
       rv.message="Missing filename"
       return rv.ToDictionary()

    filename=request.form['name']


    uniqueid=request.form['uniqueid']

    if 'captionswitch' in request.form:
       caption=int(request.form['captionswitch'])

    if 'facialswitch' in request.form:
       face=int(request.form['facialswitch'])


    imgrv=getimage(request)
    if imgrv["returnCode"] != 0:
       if "image" in imgrv:
          del imgrv["image"]

       Log.Info(mn,imgrv)
       return imgrv

    img=imgrv["image"]
    tags = {}

    Log.Info(mn,f"Caption {caption} face {face}");

    try:

       if caption==1:
          tags=gettags(img)
          tags.update(rv.ToDictionary())
          Log.Info(mn,f"File tagged {tags}")

       args = {"guid" : guid, "userid" : userid, "uniqueid" : uniqueid, "filename" : filename}


       if face==1:
          #faceArray=FaceProcessor.ToFaceArray(img)
          faceCoords=FaceProcessor.GetLocations(img, args)
          tags.update({"facedata" : faceCoords})
          Log.Info(mn,f"Updated Face Data {tags}");

    except Exception as ex:
       Log.Info(mn,f"EXCEPTION: {str(ex)}")
       rv.message=str(ex)
       rv.returnCode=1
       #img.close()
       tags.update(rv.ToDictionary())       
       

    return tags
    

@flaskInstance.route('/faces', methods = ['POST'])
def faces():
    mn="flaskapp::faces"
    Log.Info(mn,f"Method Entered {request}")
    rv = WebResult(0,0,"")

    #Log.Info(mn,"a")

    imgrv=getimage(request)
    if imgrv["returnCode"] != 0:
       if "image" in imgrv:
          del imgrv["image"]

       Log.Info(mn,imgrv)
       return imgrv

    img=imgrv["image"]

    faceArray=FaceProcessor.ToFaceArray(img)
    faceCoords=FaceProcessor.GetLocations(faceArray)

    #tags.update(rv.ToDictionary())
    Log.Info(mn,f"Faces {faceCoords}")
    return faceCoords
    


#
#This allows you to run it from python flaskapp.py
#however the modle __init__ wount get called
#
if __name__ == '__main__':
    Log.Info(mn,"About to run")
    flaskInstance.run()
