import DynamoDB_calls as db

table = db.getTable()
db.insertItem(table, "myCode","hi my name is Jack")
res = db.getItem(table, "myCode")
if res is None:
    print ("Error")
else:
    print(res["description"])
