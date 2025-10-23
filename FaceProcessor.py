import face_recognition
import json
import numpy as np
from Logger import *
from PIL import Image
import os
import uuid
import io
import pickle
from DataAccess import *
import traceback


class FaceProcessor:


    FACE_DATA_DIR='/opt/faces'
  
    @staticmethod
    def ToFaceArray(image):
        mn="FaceProcessor::ToFaceArray"
        Log.Info(mn,"In Method")

        #convert to numpy array
        #if image.mode:
        #    im = image.convert(mode)
        #else:
        #    im=image

        if image.mode != "RGB":
            im=image.convert("RGB")
        else:
            im=image;


        return np.array(im)

    @staticmethod
    def GetLocations(img, args):
        mn="FaceProcessor::GetLocations"

        Log.Info(mn,f"Method Entered {args}")

        try:      

            faceArray=FaceProcessor.ToFaceArray(img)

      
            conn=DataAccess()

        
            face = face_recognition.face_locations(faceArray)
            Log.Info(mn,f"{len(face)} Faces Detected")
            faceCoords=[]
            
            top=0
            left=0
            bottom=0
            right=0

            i=1

            Log.Info(mn,face)

        

            for f in face:    
                top=f[0]
                right=f[1]
                bottom=f[2]
                left=f[3]

                Log.Info(mn,f"FACE {i}: UL ({left},{top}) LR ({right},{bottom}) WH ({right-left},{bottom-top})")

                #Pillow crops image with left, top, right, bottom
                #faces come in: top right bottom left order

                basepath=f"{FaceProcessor.FACE_DATA_DIR}/{args['userid']}/{args['uniqueid']}/faces"

                os.makedirs(basepath, exist_ok=True)
                


                enc=face_recognition.face_encodings(faceArray,[f],1,"small")



                filename=f"{basepath}/{args['userid']}_{args['uniqueid']}_{args['guid']}_face{i}_{args['filename']}"
            
                cropped = img.crop((left, top, right, bottom))

                cropped.save(filename)

                croppedArray = io.BytesIO()
                cropped.save(croppedArray, format="JPEG")
                croppedBytes=croppedArray.getvalue()

                print("Cropped")
                print(croppedBytes)

                npfilename, npext=os.path.splitext(filename)

                npfilename=npfilename + '.npy'

                
                np.save(npfilename,enc)

                encBytes=pickle.dumps(enc)

                print("ENC")
                print(encBytes)

                faceCoords.append({
                                    "facenum" : i,
                                    "left" : left,
                                    "top" : top ,
                                    "right" : right,
                                    "bottom" : bottom,
                                    "facefile" : filename,
                                    "encfile" : npfilename})


                #enc=face_recognition.face_encodings(image,[f],1,"small")
                #print("ENC",enc)
                #enc=face_recognition.face_encodings(image)
                #print("ENC ALL",enc)

                faceguid=str(uuid.uuid4())

                sqlstr="INSERT INTO userjobitemface " \
                    "(userid, jobid, itemid, faceguid, facenum, " \
                    "processingstatuscode, processingstatusmessage, " \
                    "facefilename, faceencodingfilename, facecoordinatestlbr, " \
                    "facethumbnail, faceencoding, modtime) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)"

                
                parms=(args["userid"],
                       args["uniqueid"],
                       args["guid"],
                       faceguid,
                       i,
                       0,
                       "SUCCESS",
                       filename,
                       npfilename,
                       [top,left,bottom,right],
                       psycopg2.Binary(croppedBytes),
                       encBytes)
                       
                conn.ExecuteUpdate(sqlstr,parms)
                



                i=i+1


            Log.Info(mn,f"faceCorrds {faceCoords}")
            return faceCoords
            
        except Exception as ex:
            Log.Info(mn,f"EXCEPTION: {str(ex)}")
            trc=traceback.format_exc()
            Log.Info(mn,trc)
            raise
        finally:
            conn.Close()

       
