from GraphOmicsDB import GraphOmicsDB

if __name__ == "__main__":
    app = GraphOmicsDB("bolt://localhost:7687", "neo4j", "qwaszx123")
    c = app.count_genes()
    print("Count:", c)
    app.close()