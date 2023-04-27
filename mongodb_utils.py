import pymongo
from pymongo import MongoClient
# from bson.objectid import ObjectId

client = MongoClient("localhost", 27017, maxPoolSize=50)
db = client["academicworld"]
faculty = db["faculty"]
publications = db["publications"]
favorites = db["favorites"]

def get_faculty():
    print(publications.count_documents({}))
    print( faculty.count_documents({}))

def insert_faculty(name, note=""):
    query = { "name" : name}
    faculty_data = faculty.find_one(query)

    data = { 
        "faculty_name": faculty_data["name"], 
        "position": faculty_data["position"],
        "researchInterest": faculty_data["researchInterest"],
        "university" : faculty_data["affiliation"]["name"],
        "note": note
        }
    
    entry = favorites.insert_one(data)
    return entry.inserted_id

# def update_favorites(id, note):
#     faculty = {'_id': ObjectId(id)}
#     new_note = { "$set":  {"note": note} }
#     favorites.update_one(faculty, new_note)

def delete_faculty(name):
    faculty = {"faculty_name": name}
    favorites.delete_many(faculty)

def get_favorites():
    return favorites.find()

# inserted1 = insert_favorites("William Punch", "Professor at MSU")
# inserted2 = insert_favorites('Balzer, Stephanie', "Note about stephanie")
# inserted3 = insert_favorites('Beckmann, Nathan', "Nathan is cool")
# inserted4 = insert_favorites('Niloufar Salehi')
# inserted5 = insert_favorites('Agarwal, Yuvraj', "Professor from india")
# update_favorites("Abi Venkat", "This is the new note")
# delete_faculty("William Punch")
# delete_faculty('Balzer, Stephanie')
# delete_faculty('Beckmann, Nathan')
# delete_faculty('Niloufar Salehi')
# delete_faculty('Agarwal, Yuvraj')


# print(list(get_favorites()))

# for x in favorites.find():
#     print(x)