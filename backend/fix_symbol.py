from GraphOmicsDB import GraphOmicsDB

if __name__ == "__main__":
    app = GraphOmicsDB("bolt://localhost:7687", "neo4j", "qwaszx123")
    r = app.merge_fix_symbol()
    print("results:", r)
    app.close()