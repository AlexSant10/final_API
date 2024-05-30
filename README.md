# Proyecto Rick and Morty API con MongoDB y Neo4J

Este proyecto usa la API de Rick and Monty con los datos en una base de MongoDB y Neo4J. El objetivo es realizar consultas interesantes.

Clonaremos el repositorio 

```
git clone git@github.com:ANDIRIOUS/final_API

```

Ahora se corre lo siguiente

```
docker-compose build
docker-compose up -d

```


El proceso tomará algo de tiempo por wait-for-ir.sh

En el caso de Mongo se tiene que abrir otra terminal para hacer las consultas.

Vamos a probar las siguientes

Personajes con más episodios

```
db.characters.aggregate([ { $unwind: "$episode"}, 
{$group: { _id: "$name", uniqueEpisodes: { $addToSet: "$episode" } } }, 
{ $project: { name: "$_id", episodeCount: { $size: "$uniqueEpisodes" } } }, 
{ $sort: { episodeCount: -1 } }, { $limit: 3}] ).pretty()

```

Episodios con más personajes
```
db.episodes.aggregate([ { $unwind: "$characters" }, 
{ $group: { _id: { episode: "$episode", name: "$name" }, uniqueCharacters: { $addToSet: "$characters" } } }, 
{ $project: { episode: "$_id.episode", name: "$_id.name", characterCount: { $size: "$uniqueCharacters" } } }, 
{ $sort: { characterCount: -1 } }, 
{ $limit: 3}] ).pretty()
```
Promedio de episodios por temporada

```
db.characters.aggregate([ { $project: { name: 1, episodeCount: 
{ $size: "$episode" } } }, 
{ $group: { _id: null, avgEpisodes: 
{ $avg: "$episodeCount" } } }] )

```
Promedio de episodios de un personaje

```
db.episodes.aggregate([ { $project: { name: 1, numCharacters:
 { $size: "$characters" } } }, 
{ $group: { _id: null, totalEpisodes: { $sum: 1 },
 totalCharacters: { $sum: "$numCharacters" } } }, 
{ $project: { _id: 0, averageCharactersPerEpisode: 
{ $divide: ["$totalCharacters", "$totalEpisodes"] } } }] )
```
Por otro lado, las consuktas que podemos hacer en Neo4J son:

Número de personajes y de personaje nuevos por cada temporada
```
MATCH (c:Character)-[:APPEARS_IN]->(e:Episode)
WITH c, e, substring(e.episode, 0, 3) AS season 
WITH season, collect(DISTINCT c.id) AS characters_per_season
RETURN season, size(characters_per_season) AS unique_character_count
ORDER BY unique_character_count DESC
```

Número de especies promedio por episodio en cada temporada:
```
MATCH (c:Character)-[:APPEARS_IN]->(e:Episode)
WITH c, e, substring(e.episode, 0, 3) AS season 
WITH season, e, c.species AS species, COUNT(DISTINCT c.id) AS species_count_per_episode
WITH season, e.id AS episode_id, COLLECT(DISTINCT species) AS species_list
WITH season, episode_id, SIZE(species_list) AS species_diversity
RETURN season, AVG(species_diversity) AS avg_species_diversity_per_episode
ORDER BY season
```

Número de ubicaciones distintas en cada temporada:
```
MATCH (c:Character)-[:APPEARS_IN]->(e:Episode)
MATCH (c)-[:LIVES_IN]->(l:Location)
WITH e, substring(e.episode, 1, 3) AS season, l
WITH season, e, COUNT(DISTINCT l) AS num_locations
WITH season, COUNT(DISTINCT e) AS num_episodes, SUM(num_locations) AS total_locations
RETURN season, total_locations
ORDER BY season
```

