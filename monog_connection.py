from pymongo import MongoClient
# mongo_url="mongodb+srv://salmankhh8:RZRBZ45knXBwnSw1@cluster0.fvlhn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# mongo_url="mongodb+srv://salmankhh8:RZRBZ45knXBwnSw1@cluster0.4pl6u.mongodb.net/"

mongo_url = uri = "mongodb+srv://salmankhh8:RZRBZ45knXBwnSw1@cluster0.4pl6u.mongodb.net/"
def connect_to_mongo(mongo_url, db_name):
    try:
        # Create a client instance
        client = MongoClient(mongo_url)

        # Connect to the database
        db = client[db_name]

        # Check connection by listing collections
        collections = db.list_collection_names()
        print(f"Connected to MongoDB! Collections in '{db_name}': {collections}")

        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
    
database = connect_to_mongo(mongo_url,"compile_craf_v2")


if database is not None:
    # Example: Access a collection
    collection = database["auth_user"]

    # Example: Insert a document
    document = {"name": "John", "age": 30}
    result = collection.insert_one(document)
    print(f"Document inserted with ID: {result.inserted_id}")


# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# # uri = "mongodb+srv://salmankhh8:RZRBZ45knXBwnSw1@cluster0.4pl6u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# uri = "mongodb+srv://salmankhh8:RZRBZ45knXBwnSw1@cluster0.4pl6u.mongodb.net/"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.complile_carf_v2.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

