import pymongo

connectionAtlas = "mongodb+srv://WristWonders:root@wristwonderscluster.ri89dpv.mongodb.net/admin?authSource=admin&replicaSet=atlas-f0zukj-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"

client = pymongo.MongoClient(connectionAtlas)

db = client["WristWondersDataBase_Dev"]
collection = db["Productos"]

total_documentos = collection.count_documents({})

print(f"Total de documentos en la colección 'productos': {total_documentos}")

for documento in collection.find():
    print(documento)

# for documento in collection.find_one({"Nom_Prod":"WS-1100H-2AV"}):
#     print(documento)
