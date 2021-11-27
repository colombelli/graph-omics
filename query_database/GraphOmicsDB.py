from neo4j import GraphDatabase

class GraphOmicsDB:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def count_genes(self):
        with self.driver.session() as session:
            values, info = session.read_transaction(self._count_genes)
        return values, info

    @staticmethod
    def _count_genes(tx):
        query = "MATCH (g:Gene) RETURN COUNT(g)"
        result = tx.run(query)
        record = result.single()
        value = record.value()
        info = result.consume()
        return value, info
