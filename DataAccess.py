import psycopg2
from Logger import *




class DataAccess:
    def __init__(self):
        mn="DataAccess::DataAccess"
        Log.Info(mn,"In Constructor")

        try:
            self.conn=psycopg2.connect(
                host="192.168.163.128",
                database="photocloud",
                user="postgres",
                password="password"
            )

        except Exception as ex:
            Log.Info(mn,f"Exception {str(ex)}")
            self.conn=None
            raise


    def GetRowSet(self,sqlstr,parmlist):
        mn="DataAccess::GetRowSet"
        Log.Info(mn,"In Method")

        try:
            cur=self.conn.cursor()
            cur.execute(sqlstr,parmlist)
            rows=cur.fetchall()
            return rows
        except Exception as ex:
            Log.Info(mn,f"EXCEPTION {str(ex)}")
            raise
        finally:
            if cur is not None:
                cur.close()


    def ExecuteUpdate(self,sqlstr,parmlist):
        mn="DataAccess::ExecuteUpdate"
        Log.Info(mn,"In Method")

        try:
            Log.Info(mn,f"{sqlstr} {str(parmlist)}")
            cur=self.conn.cursor()
            cur.execute(sqlstr,parmlist)
            rows=cur.rowcount
            self.conn.commit()
            return rows
        except Exception as ex:
            Log.Info(mn,f"EXCEPTION {str(ex)}")
            Log.Info(mn,"Transaction rolledback")
            Log.Info(mn,sqlstr + " " + str(parmlist))
            self.conn.rollback()
            raise
        finally:
            if cur is not None:
                cur.close()


    def Close(self):
        if self.conn is not None:
            self.conn.close()       


    def __del__(self):
        mn="DataAccess::~DataAccess"
        #Log.Info(mn,"In Destructor")
        print(f"{mn} - In Destructor")
        if self.conn is not None:
            self.conn.close()




                
            
                     
