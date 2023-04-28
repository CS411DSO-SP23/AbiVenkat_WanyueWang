import pymongo
from pymongo import MongoClient
import pandas as pd
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

def delete_faculty(name):
    faculty = {"faculty_name": name}
    favorites.delete_many(faculty)

def get_favorites():
    return pd.DataFrame(list(favorites.find())).iloc[:, 1:]

