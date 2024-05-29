import requests
import pymongo
from neo4j import GraphDatabase

# Conexión a MongoDB
mongo_client = pymongo.MongoClient("mongodb://mongodb:27017/")
mongo_db = mongo_client["rick_morty"]
characters_collection = mongo_db["characters"]
locations_collection = mongo_db["locations"]
episodes_collection = mongo_db["episodes"]

# Conexión a Neo4j
neo4j_driver = GraphDatabase.driver("bolt://neo4j_db:7687", auth=("neo4j", "test1234"))

def fetch_all(endpoint):
    items = []
    url = f"https://rickandmortyapi.com/api/{endpoint}"
    while url:
        response = requests.get(url)
        data = response.json()
        items.extend(data["results"])
        url = data["info"]["next"]
    return items

def save_to_mongo(collection, items):
    collection.insert_many(items)

def save_characters_to_neo4j(characters):
    with neo4j_driver.session() as session:
        for character in characters:
            session.run(
                "MERGE (c:Character {id: $id, name: $name, status: $status, species: $species})",
                id=character["id"],
                name=character["name"],
                status=character["status"],
                species=character["species"]
            )

def save_locations_to_neo4j(locations):
    with neo4j_driver.session() as session:
        for location in locations:
            session.run(
                "MERGE (l:Location {id: $id, name: $name, type: $type, dimension: $dimension})",
                id=location["id"],
                name=location["name"],
                type=location["type"],
                dimension=location["dimension"]
            )
            for resident_url in location["residents"]:
                resident_id = int(resident_url.split("/")[-1])
                session.run(
                    "MATCH (l:Location {id: $location_id}), (c:Character {id: $resident_id}) "
                    "MERGE (c)-[:LIVES_IN]->(l)",
                    location_id=location["id"],
                    resident_id=resident_id
                )

def save_episodes_to_neo4j(episodes):
    with neo4j_driver.session() as session:
        for episode in episodes:
            session.run(
                "MERGE (e:Episode {id: $id, name: $name, air_date: $air_date, episode: $episode})",
                id=episode["id"],
                name=episode["name"],
                air_date=episode["air_date"],
                episode=episode["episode"]
            )
            for character_url in episode["characters"]:
                character_id = int(character_url.split("/")[-1])
                session.run(
                    "MATCH (e:Episode {id: $episode_id}), (c:Character {id: $character_id}) "
                    "MERGE (c)-[:APPEARS_IN]->(e)",
                    episode_id=episode["id"],
                    character_id=character_id
                )

if __name__ == "__main__":
    # Fetch data from API
    characters = fetch_all("character")
    locations = fetch_all("location")
    episodes = fetch_all("episode")
    
    # Save data to MongoDB
    save_to_mongo(characters_collection, characters)
    save_to_mongo(locations_collection, locations)
    save_to_mongo(episodes_collection, episodes)

    # Save data to Neo4j
    save_characters_to_neo4j(characters)
    save_locations_to_neo4j(locations)
    save_episodes_to_neo4j(episodes)
    
    print("Data imported successfully!")
