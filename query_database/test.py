from GraphOmicsDB import GraphOmicsDB

if __name__ == "__main__":
    app = GraphOmicsDB("bolt://localhost:7687", "neo4j", "qwaszx123")
    r = app.tumoral_10_least_expressed_genes()
    print("results:", r)
    app.close()