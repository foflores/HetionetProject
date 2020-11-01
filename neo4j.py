import os
import re
from py2neo import Graph

class Neo4jDb():
    def __init__(neo):
        #Modify these lines to reflect database login information, data location, and neo4j import folder
        neo.graph = Graph(user="neo4j", password="password")
        neo.path_nodes = "data/nodes_test.tsv"
        neo.path_edges = "data/edges_test.tsv"
        neo.path_import = "/usr/local/Cellar/neo4j/4.1.3/libexec/import"
        #Do not modify
        neo.nodes = []
        neo.edges = []

    def clear(neo):
        #Clear database and neo4j import folder to prepare for data loading
        input = "MATCH (n) DETACH DELETE n"
        neo.graph.run(input)
        if len(os.listdir(neo.path_import)) > 0:
            input = f"rm -r {neo.path_import}/*"
            os.system(input)
        input = "CALL db.constraints"
        constraints = neo.graph.run(input).data()
        for constraint in constraints:
            name = constraint['name']
            input = f"DROP CONSTRAINT {name}"
            neo.graph.run(input)
        
    
    def analyze_data(neo):
        #Finds the names of all node and edge types
        with open (neo.path_nodes, 'r') as file:
            for line in file:
                if line == 'id\tname\tkind\n':
                    continue
                data = re.split('\t|\n', line)
                if neo.nodes.count(data[2]) == 0:
                   neo.nodes.append(data[2])
        
        with open (neo.path_edges, 'r') as file:
            for line in file:
                if line == 'source\tmetaedge\ttarget\n':
                    continue
                data = re.split('\t|\n', line)
                if (neo.edges.count(data[1]) == 0):
                    neo.edges.append(data[1])
        
    def load_nodes(neo):
        #Splits node data file by type, places them in neo4j import folder, and imports to database
        for node in neo.nodes:
            input = f"grep '{node}' {neo.path_nodes} >> {neo.path_import}/{node}.tsv"
            os.system(input)
            input = f"CREATE CONSTRAINT ON (n:{node}) ASSERT (n.id) is UNIQUE"
            neo.graph.run(input)
            input = f"""USING PERIODIC COMMIT 500
            LOAD CSV FROM 'file:///{node}.tsv' AS row
            FIELDTERMINATOR '\u0009'
            CREATE (:{node} {{id: row[0], name: row[1]}})"""
            neo.graph.run(input)
            
    def load_edges(neo):
        #Splits edge data file by type, places them in neo4j import folder, and imports to database
        for edge in neo.edges:
            edge_no_symbol = edge
            relationship = edge_no_symbol[1]
            source = "";
            target = "";
            if edge_no_symbol.count("r>") != 0:
                edge_no_symbol = edge_no_symbol.replace("r>", "z")
            for node in neo.nodes:
                if edge[0] == node[0]:
                    source = node
                if edge[len(edge)-1] == node[0]:
                    target = node
            system = f"grep '{edge}' {neo.path_edges} >> {neo.path_import}/{edge_no_symbol}.tsv"
            os.system(system)
            input = f"""USING PERIODIC COMMIT 500
            LOAD CSV FROM 'file:///{edge_no_symbol}.tsv' AS row FIELDTERMINATOR '\u0009'
            MATCH (a:{source} {{id:row[0]}})
            MATCH (b:{target} {{id:row[2]}})
            CREATE (a)-[:{relationship}]->(b)"""
            neo.graph.run(input)
            
    def query_neo(neo, disease):
        #Querys the database looking for all drugs that correspond to the given Query #2 and prints to terminal
        final_output = set()
        input = f"""MATCH (a:Compound)-[:r]-(b:Compound)-[:u]->(c:Gene)<-[:d]-(d:Anatomy)<-[:l]-(e:Disease {{name:'{disease}'}})
        WHERE NOT (a)-[:t]->(e)
        RETURN DISTINCT a.name"""
        output = neo.graph.run(input).data()
        for x in output:
            final_output.add(x['a.name'])
            
        input =f"""MATCH (b:Compound)-[:u]->(c:Gene)<-[:d]-(d:Anatomy)<-[:l]-(e:Disease {{name:'{disease}'}})
        WHERE NOT (b)-[:t]->(e)
        RETURN DISTINCT b.name"""
        output = neo.graph.run(input).data()
        for x in output:
            final_output.add(x['b.name'])
            
        input = f"""MATCH (a:Compound)-[:r]-(b:Compound)-[:d]->(c:Gene)<-[:u]-(d:Anatomy)<-[:l]-(e:Disease {{name:'{disease}'}})
        WHERE NOT (a)-[:t]->(e)
        RETURN DISTINCT a.name"""
        output = neo.graph.run(input).data()
        for x in output:
            final_output.add(x['a.name'])
            
        input = f"""MATCH (b:Compound)-[:d]->(c:Gene)<-[:u]-(d:Anatomy)<-[:l]-(e:Disease {{name:'{disease}'}})
        WHERE NOT (b)-[:t]->(e)
        RETURN DISTINCT b.name"""
        output = neo.graph.run(input).data()
        for x in output:
            final_output.add(x['b.name'])
    
        if (len(final_output) == 0):
            print ("\nNo drugs found")
        else:
            print (f"\nThese drugs will treat {disease}: ")
            for output in final_output:
                print ("\t", output)
        
    def create(neo):
        #Runs all steps in the creation of the database
        neo.clear()
        neo.analyze_data()
        neo.load_nodes()
        neo.load_edges()
