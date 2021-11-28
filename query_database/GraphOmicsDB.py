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


    def tumoral_10_most_expressed_genes(self):
        with self.driver.session() as session:
            values = session.read_transaction(self._tumoral_10_most_expressed_genes)
        return values
    @staticmethod
    def _tumoral_10_most_expressed_genes(tx):
        query = """MATCH (:Patient) -[te:HAS_TUMORAL_EXPRESSION_OF] -> (g:Gene)
        RETURN g AS gene, avg(toFloat(te.expression)) AS tumoral_expression_avg
        ORDER BY tumoral_expression_avg DESC
        LIMIT 10"""
        result = tx.run(query)
        values = [record.data() for record in result]
        return values
        