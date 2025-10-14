from flask import jsonify

class WebResult:
    def __init__(self, returnCode, returnCode2, message):
        self.returnCode=returnCode
        self.returnCode2=returnCode2
        self.message=message

    def set(self, returnCode, returnCode2, message):
        self.returnCode=returnCode
        self.returnCode2=returnCode2
        self.message=message

    def setMessage(self,msg):
        self.message=msg;


    def ToDictionary(self):
        rv = {"returnCode" : self.returnCode,
              "returnCode2" : self.returnCode2,
              "message": self.message}
        return rv    

    def ToJSON(self):
        rv = self.ToDictionary()
        return jsonify(rv)
    
        
    
