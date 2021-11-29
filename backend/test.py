from GraphOmicsDB import GraphOmicsDB

if __name__ == "__main__":
    app = GraphOmicsDB("bolt://localhost:7687", "neo4j", "qwaszx123")
    r = app.mirna_target_gene_min_max()
    print("results:", r)
    app.close()