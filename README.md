<div align="center">
	<a href="https://www.github.com/foflores10/hetionetproject">
		<img src="images/hetionet.png" width="80" height="80">
	</a>
	<h3>Hetionet Project</h3>
</div>

## About The Project
- Fall 2020
- CSCI 493.71
- Project 1

## Getting Started
### Dependencies
- Python 3.9
- JDK 11
- Mongodb 4.4
- Neo4j 4.2
- Py2neo 2020.1
- Pymongo 3.11

### Installation


1. Neo4j Setup
	- Open `neo4j.py`
	- Look under `def __init__ (neo)`
	- Check `user` and `password` are correct for your server
	- Change `neo.path_####` with the proper locations for data
	- Make sure neo4j server is started

2. Mongodb Setup
	- Open `models.py`
	- Make sure `mongo_uri` is correct for your server
	- Make sure mongodb server is started
