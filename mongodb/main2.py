from pymongo import MongoClient


url='mongodb+srv://suriya_mdb:su2ri00ya4@cluster0.0xezgdx.mongodb.net/?appName=Cluster0'

client=MongoClient(url)

db=client['first_database']
user=db['users']



def add_user(data):
    user.insert_one(data)
    return 'insert successfuly'

def delete_user(data):
    user.delete_one(data)
    return 'delete successfuly'

def find_user(name):
    data=user.find_one({"username":name})
    return data

print(find_user(name='suriya'))



