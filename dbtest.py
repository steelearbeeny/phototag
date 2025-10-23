import psycopg2
from DataAccess import *


try:

        dataAccess=DataAccess()

        rows=dataAccess.ExecuteUpdate("INSERT INTO SERVICE (SERVICEID) VALUES (%s)",(1000,))

        print(rows)
        
        
        rows=dataAccess.GetRowSet("SELECT * FROM SERVICE WHERE SERVICEID=%s",(1000,))


        for r in rows:
                print(r[0])

except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")

