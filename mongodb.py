import csv
import os
import pymongo

from models import map_relationship, mongo_uri
map = map_relationship


class MongoDb():
    # module class for mongo functions/set up

    def __init__(self):
        self.data_path = os.path.join(os.getcwd(), "data")
        self.mongo_client = pymongo.MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client["hetionet"]
        self.mongo_collections = self.mongo_db["datas"]

    def initializeDb(self):
        #since db is not created without a document, we have
        #to create a single data

        #if condition to check for database existence
        if "hetionet" in self.mongo_client.list_database_names():
            print("a database exists")
            return
        else:
            print("no database exists, creating one for you")

            # we will attempt to create a data design for any individual disease
            diseases = {}
            datas = {'Anatomy': {}, 'Gene': {}, 'Disease': {}, 'Compound': {}}

            # read data file and create rows and cols variables
            with open(os.path.join(self.data_path, "nodes_test.tsv"),
                      "r") as nodes:
                reader = csv.DictReader(nodes, delimiter="\t")
                for row in reader:
                    datas[row['kind']][row['id']] = row['name']

            for k, v in datas['Disease'].items():
                diseases[k] = {
                    'id': k,
                    'name': v,
                    "treat": [],
                    "palliate": [],
                    "gene": [],
                    "where": []
                }

        # create an object of arrays with each relationships
            with open(os.path.join(self.data_path, "edges_test.tsv"),
                      "r") as edges:
                reader = csv.DictReader(edges, delimiter="\t")
                for row in reader:
                    edge = row['metaedge']
                if edge in map.keys():
                    diseases[row[map[edge][0]]][map[edge][3]].append(
                        datas[map[edge][2]][row[map[edge][1]]])

        self.mongo_collections.insert_many([v for _, v in diseases.items()])

    def query(self, query):
        cursor = self.mongo_collections.find({"id": query})

        colCount = 0

        ## wild card count for result
        for _ in cursor:
            if colCount > 0:
                break
            colCount = colCount + 1

        if colCount == 0:
            next_cursor = self.mongo_collections.find({"name": query})
        else:
            cursor.rewind()
            next_cursor = cursor

        # data fetching by fields

        colCount = 0
        id = ""
        name = ""
        treat = []
        palliate = []
        gene = []
        where = []

        for v in cursor:
            # initialize id
            id = v['id']
            name = v['name']
            treat.extend(v['treat'])
            palliate.extend(v['palliate'])
            gene.extend(v['gene'])
            where.extend(v['where'])
            colCount = colCount + 1

        if colCount == 0:
            print("no data found for this disease")
            return

    def separate(sep, res):
        return sep.join(res)

    def format(res):

        # default case
        if not res:
            return "None"

        #create group
        res = [res[v:v + 5] for v in range(0, len(res), 5)]
        #remove commas
        commas = map(lambda v: separate(",", v) + ',', res)
        return separate("\n\t", commas)[:-1]

    print(f'{query}" we found the following:',
          f'name => \n\t{name}',
          f'compound that treats it => "{query}":\n{separate(treat)}',
          f'compound that palliates it => "{query}":\n{separate(palliate)}',
          f'gene that causes it => "{query}":\n{separate(gene)}',
          f'where "{query}" occures => \n{separate(where)}',
          sep='\n')


mongo = MongoDb()
mongo.initializeDb()
