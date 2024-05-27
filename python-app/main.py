import requests
import pymongo
from neo4j import GraphDatabase

# Conexión a MongoDB
mongo_client = pymongo.MongoClient("mongodb://mongodb:27017/")
mongo_db = mongo_client["rick_morty"]
mongo_collection = mongo_db["characters"]

# Conexión a Neo4j
neo4j_driver = GraphDatabase.driver("bolt://neo4j_db:7687", auth=("neo4j", "test1234"))

def fetch_all_characters():
    characters = []
    url = "https://rickandmortyapi.com/api/character"
    while url:
        response = requests.get(url)
        data = response.json()
        characters.extend(data["results"])
        url = data["info"]["next"]  # Update the URL to the next page
    return characters

def save_to_mongo(characters):
    mongo_collection.insert_many(characters)

def save_to_neo4j(characters):
    with neo4j_driver.session() as session:
        for character in characters:
            session.run(
                "MERGE (c:Character {id: $id, name: $name, status: $status, species: $species})",
                id=character["id"],
                name=character["name"],
                status=character["status"],
                species=character["species"]
            )

if __name__ == "__main__":
    characters = fetch_all_characters()
    save_to_mongo(characters)
    save_to_neo4j(characters)
    print("Data imported successfully!")
