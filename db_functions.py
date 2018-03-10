import pymysql

def get_connection() :
	hostname = "cis450.c5rvqqjl9c91.us-east-1.rds.amazonaws.com"
	username = "cis450"
	password = "cis450team40"
	database = "project"

        print("connecting to database...")
        myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database )
        return myConnection

def close(myConnection):
        print("Closing connection")
        myConnection.close();

# Simple routine to run a query on a database and print the results:
def doQuery( conn, query) :
        cur = conn.cursor()
        try:
                cur.execute(query)
        except pymysql.Error as e:
                print ("An error has occurred ", e)
                conn.rollback()
        else:
                conn.commit()

def doQueryResults( conn, query) :
        cur = conn.cursor()
        try:
                cur.execute(query)
        except pymysql.Error as e:
                print ("An error has occurred ", e)
                conn.rollback()
                return None
        else:
                conn.commit()
                if cur.rowcount == 0:
                        return None
                return cur.fetchall()
