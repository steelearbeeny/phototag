from datetime import datetime

class Log:

    @staticmethod
    def Info(mn,msg):
        now = datetime.now()
        formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print(formatted_date_time,mn,msg)

        
