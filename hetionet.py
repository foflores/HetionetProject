from neo4j import Neo4jDb

def main():
    neo = Neo4jDb()
    neo.create()
    
if __name__ == "__main__":
    main()

