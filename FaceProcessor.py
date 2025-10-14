import face_recognition
import json
import numpy as np
from Logger import *


class FaceProcessor:
  
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
    def GetLocations(faceArray):
        mn="FaceProcessor::GetLocations"
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

            faceCoords.append({"facenum" : i, "left" : left, "top" : top , "right" : right, "bottom" : bottom})


            #enc=face_recognition.face_encodings(image,[f],1,"small")
            #print("ENC",enc)
            #enc=face_recognition.face_encodings(image)
            #print("ENC ALL",enc)


            i=i+1


        Log.Info(mn,f"faceCorrds {faceCoords}")
        return faceCoords
