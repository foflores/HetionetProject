import os
import re
from py2neo import Graph

class Neo4jDb():
    def __init__(neo):
        neo.graph = Graph(user="neo4j", password="letmein")
        neo.path_nodes = "data/nodes.tsv"
        neo.path_edges = "data/edges.tsv"
        neo.path_import = "~/Neo_Server/import"
        neo.nodes = [];
        neo.edges = [];

    def clear(neo):
        input = "MATCH (n) DETACH DELETE n"
        neo.graph.run(input)
        input = f"rm -r {neo.path_import}"
        os.system(input)
        input = f"mkdir {neo.path_import}"
        os.system(input)
    
            
    def analyze_data(neo):
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
        for node in neo.nodes:
            input = f"grep '{node}' {neo.path_nodes} >> {neo.path_import}/{node}.tsv"
            os.system(input)
            input = f"CREATE CONSTRAINT ON (n:{node}) ASSERT (n.id) is UNIQUE"
            neo.graph.run(input)
            input = f"LOAD CSV FROM 'file:///{node}.tsv' AS row FIELDTERMINATOR '\u0009' CREATE (:{node} {{id: row[0], name: row[1]}})"
            neo.graph.run(input)
            
    def load_edges(neo):
        for edge in neo.edges:
            edge_no_symbol = edge
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
            input = f"""USING PERIODIC COMMIT
            LOAD CSV FROM 'file:///{edge_no_symbol}.tsv' AS row FIELDTERMINATOR '\u0009'
            MATCH (a:{source} {{id:row[0]}})
            MATCH (b:{target} {{id:row[2]}})
            CREATE (a)-[:{edge_no_symbol}]->(b)"""
            neo.graph.run(input)
        
    def create(neo):
        neo.clear()
        neo.analyze_data()
        neo.load_nodes()
        neo.load_edges()
