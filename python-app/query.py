import pymongo
from neo4j import GraphDatabase

# Conexión a MongoDB
mongo_client = pymongo.MongoClient("mongodb://mongodb:27017/")
mongo_db = mongo_client["rick_morty"]
mongo_collection = mongo_db["characters"]

# Conexión a Neo4j
neo4j_driver = GraphDatabase.driver("bolt://neo4j_db:7687", auth=("neo4j", "test1234"))

# Consultas a MongoDB
def find_character_in_mongo(name):
    character = mongo_collection.find_one({"name": name})
    return character

def count_characters_in_mongo():
    count = mongo_collection.count_documents({})
    return count

# Consultas a Neo4j
def find_character_in_neo4j(name):
    query = """
    MATCH (c:Character {name: $name})
    RETURN c
    """
    with neo4j_driver.session() as session:
        result = session.run(query, name=name)
        return result.single()

def count_characters_in_neo4j():
    query = """
    MATCH (c:Character)
    RETURN count(c) AS count
    """
    with neo4j_driver.session() as session:
        result = session.run(query)
        return result.single()["count"]

if __name__ == "__main__":
    # Ejemplo de consultas en MongoDB
    character_name = "Rick Sanchez"
    character_mongo = find_character_in_mongo(character_name)
    print(f"Character found in MongoDB: {character_mongo}")

    character_count_mongo = count_characters_in_mongo()
    print(f"Total characters in MongoDB: {character_count_mongo}")

    # Ejemplo de consultas en Neo4j
    character_neo4j = find_character_in_neo4j(character_name)
    print(f"Character found in Neo4j: {character_neo4j}")

    character_count_neo4j = count_characters_in_neo4j()
    print(f"Total characters in Neo4j: {character_count_neo4j}")
