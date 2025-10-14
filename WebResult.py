from flask import jsonify

class WebResult:
    def __init__(self, returnValue, returnValue2, message):
        self.returnValue=returnValue
        self.returnValue2=returnValue2
        self.message=message

    def set(self, returnValue, returnValue2, message):
        self.returnValue=returnValue
        self.returnValue2=returnValue2
        self.message=message

    def setMessage(self,msg):
        self.message=msg;

    def ToJSON(self):
        rv = {"returnValue" : self.returnValue,
              "returnValue2" : self.returnValue2,
              "message": self.message}
        return jsonify(rv)
    
        
    
