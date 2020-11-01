map_relationship = {
    "CtD": ['target', 'source', "Compound", "treat"],
    "CpD": ['target', 'source', "Compound", "palliate"],
    "DaG": ['source', 'target', "Gene", "gene"],
    "DuG": ['source', 'target', "Gene", "gene"],
    "DdG": ['source', 'target', "Gene", "gene"],
    "DlA": ['source', 'target', "Anatomy", "where"]
}

mongo_uri = "mongodb+srv://root:root@cluster0.3iybi.gcp.mongodb.net/hetionet?retryWrites=true&w=majority"
