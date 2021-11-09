<div align="center">
	<a href="https://www.github.com/foflores10/hetionetproject">
		<img src="https://media.foflores.com/projects/hetionetproject/icon.png" width=128>
	</a>
	<h3>Hetionet Project</h3>
	<p>Created by: Favian Flores and MD Uddin</p>
</div>

## About The Project

[Hetionet](het.io) is a network of biomedical knowledge assembled from a variety of databases. It combines information into a single resource and allows researchers to formulate insights based on the data.

This project aims to recreate Hetionet using MongoDB and Neo4J databases to learn the importance of proper database design when working with big data.

## Getting Started

### Dependencies

- Python 3.9
- JDK 11
- Mongodb 4.4
- Neo4j 4.2
- Py2neo 2020.1
- Pymongo 3.11

### Installation

- Neo4j Setup
	1. Open `neo4j.py`
	2. Look under `def __init__ (neo)`
	3. Check `user` and `password` are correct for your server
	4. Change `neo.path_####` with the proper locations for data
	5. Make sure neo4j server is started

- Mongodb Setup
	1. Open `models.py`
	2. Make sure `mongo_uri` is correct for your server
	3. Make sure mongodb server is started
