from neo4j import Neo4jDb

def main():
    neo = Neo4jDb()
    #neo.create()
    
    
    print ("Welcome to our Hetionet model!")
    
    done = False
    while not done:
        print ("\nWhich question would you like answered?")
        print ("""\n1: Given a disease id, what is its name, what are drug
names that can treat or palliate this disease, what are gene names
that cause this disease, and where this disease occurs?
        
2: We assume that a compound can treat a disease if the compound or
its resembled compound up-regulates/down- regulates a gene, but the
location down-regulates/up-regulates the gene in an opposite
direction where the disease occurs. Find all compounds that can treat
a new disease name (i.e. the missing edges between compound and
disease excluding existing drugs).""")
        bool = True
        choice = ""
        while bool:
            choice = input("\nChoice: ")
            if choice == "1" or choice == "2":
                bool = False
            else:
                print ("try again")
        
        if choice == "1":
############ENTER CODE FOR MONGO QUERY HERE"
            print ("CODE FOR MONGO QUERY GOES HERE")
            
        else:
            print ("\nEnter the name of a new disease to find all compounds that can treat it.")
            disease = input("\nDisease: ")
            neo.query_neo(disease)
            
        bool = True
        while bool:
            choice = input("\nEnter '1' to run another query, or '2' to end program: ")
            if choice == "1":
                bool = False
            elif choice == "2":
                bool = False
                done = True
            else:
                print ("try again")

    
if __name__ == "__main__":
    main()

