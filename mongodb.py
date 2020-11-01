import csv
import os
import pymongo


class MongoDb():
    # module class for mongo functions/set up

    def __init__(self):
        self.data_path = os.path.join(os.getcwd(), "data")
        self.mongo_client = pymongo.MongoClient(
            "mongodb+srv://root:root@cluster0.3iybi.gcp.mongodb.net/hetionet?retryWrites=true&w=majority"
        )
        self.mongo_db = self.mongo_client["hetionet"]
        self.mongo_collections = self.mongo_db["datas"]

    def initializeDb(self):
        #since db is not created without a document, we have
        #to create a single data

        #if condition to check for database existence
        if self.mongo_collections.find().limit(1):
            print("a database exists")
            return
        else:
            print("no database exists, creating one for you")

            # we will attempt to create a data design for any individual disease
            diseases = {}
            datas = {'Anatomy': {}, 'Gene': {}, 'Disease': {}, 'Compound': {}}

            # read data file and create rows and cols variables
            with open(os.path.join(self.data_path, "nodes.tsv"), "r") as nodes:
                reader = csv.DictReader(nodes, delimiter="t")
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


mongo = MongoDb()
mongo.initializeDb()
