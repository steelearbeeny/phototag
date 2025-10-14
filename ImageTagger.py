#import argparse
import numpy as np
import random

import torch
import json

from PIL import Image
from ram.models import tag2text
from ram import inference_tag2text as inference
from ram import get_transform
from Logger import *

class ImageTagger:
    def __init__(self):
        mn="ImageTagger::ImageTagger"
        Log.Info(mn,"In Constructor")
        
        pytorchmodel='/opt/pretrained/tag2text_swin_14m.pth'
        imagesize=384
        threshold=0.68

        #device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.device=torch.device('cpu')
        self.transform = get_transform(image_size=imagesize)

        Log.Info(mn,"Device and transform set")

        # delete some tags that may disturb captioning
        # 127: "quarter"; 2961: "back", 3351: "two"; 3265: "three"; 3338: "four"; 3355: "five"; 3359: "one"
        delete_tag_index = [127,2961, 3351, 3265, 3338, 3355, 3359]
        self.model = tag2text(pretrained=pytorchmodel,
                         image_size=imagesize,
                         vit='swin_b',
                         delete_tag_index=delete_tag_index)
        self.model.threshold = threshold  # threshold for tagging

        Log.Info(mn,"Model created")
        
        self.model.eval()

        Log.Info(mn,"Model evaluated")

        self.model = self.model.to(self.device)
        Log.Info(mn,"Done")

    def InferenceTest(self):
        mn="ImageTagger::InferenceTest"
        inputImage = '/home/arbeeny/recognize-anything/images/demo/demo1.jpg'
 
        errorMessage=""
        tagArray=[]
        caption=""

        Log.Info(mn,"Method Entered")

        try:
        
            image = self.transform(Image.open(inputImage)).unsqueeze(0).to(self.device)

            Log.Info(mn,"Image transformed")

            res = inference(image, self.model, "")
            #print("Model Identified Tags: ", res[0])
            #print("User Specified Tags: ", res[1])
            #print("Image Caption: ", res[2])

            Log.Info(mn,"Inference complete")
            tagArray=res[0].split(' | ')
            caption=res[2]
            Log.Info(mn,tagArray);

        except Exception as ex:
            Log.Info(mn,f"EXCEPTION: {ex}")
            errorMessage=str(ex)

        #print(res)
        rv = {
            "tags" : tagArray,
            "caption" : caption,
            "errorMessage" : errorMessage
        }


        jsonString = json.dumps(rv,indent=4)
        Log.Info(mn,jsonString)
        return rv;


    def Inference(self, inputImage):
        mn="ImageTagger::Inference"
     
        errorMessage=""
        tagArray=[]
        caption=""

        Log.Info(mn,"Method Entered")

        try:
        
            image = self.transform(inputImage).unsqueeze(0).to(self.device)

            Log.Info(mn,"Image transformed")

            res = inference(image, self.model, "")
            #print("Model Identified Tags: ", res[0])
            #print("User Specified Tags: ", res[1])
            #print("Image Caption: ", res[2])

            Log.Info(mn,"Inference complete")
            tagArray=res[0].split(' | ')
            caption=res[2]
            Log.Info(mn,tagArray);

        except Exception as ex:
            Log.Info(mn,f"EXCEPTION: {ex}")
            errorMessage=str(ex)

        #print(res)
        rv = {
            "tags" : tagArray,
            "caption" : caption,
            "errorMessage" : errorMessage
        }


        jsonString = json.dumps(rv,indent=4)
        Log.Info(mn,jsonString)
        return rv;

        
        
