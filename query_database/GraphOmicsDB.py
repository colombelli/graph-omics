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
        
    def tumoral_10_least_expressed_genes(self):
        with self.driver.session() as session:
            values = session.read_transaction(self._tumoral_10_least_expressed_genes)
        return values
    @staticmethod
    def _tumoral_10_least_expressed_genes(tx):
        query = """MATCH (:Patient) -[te:HAS_TUMORAL_EXPRESSION_OF] -> (g:Gene)
        RETURN g AS gene, avg(toFloat(te.expression)) AS tumoral_expression_avg
        ORDER BY tumoral_expression_avg
        LIMIT 10"""
        result = tx.run(query)
        values = [record.data() for record in result]
        return values


    def normal_10_most_expressed_genes(self):
        with self.driver.session() as session:
            values = session.read_transaction(self._normal_10_most_expressed_genes)
        return values
    @staticmethod
    def _normal_10_most_expressed_genes(tx):
        query = """MATCH (:Patient) -[ne:HAS_NORMAL_EXPRESSION_OF] -> (g:Gene)
        RETURN g AS gene, avg(toFloat(ne.expression)) AS normal_expression_avg
        ORDER BY normal_expression_avg DESC
        LIMIT 10"""
        result = tx.run(query)
        values = [record.data() for record in result]
        return values
        
    def normal_10_least_expressed_genes(self):
        with self.driver.session() as session:
            values = session.read_transaction(self._normal_10_least_expressed_genes)
        return values
    @staticmethod
    def _normal_10_least_expressed_genes(tx):
        query = """MATCH (:Patient) -[ne:HAS_NORMAL_EXPRESSION_OF] -> (g:Gene)
        RETURN g AS gene, avg(toFloat(ne.expression)) AS normal_expression_avg
        ORDER BY normal_expression_avg
        LIMIT 10"""
        result = tx.run(query)
        values = [record.data() for record in result]
        return values


    def by_stage_10_most_expressed_genes(self):
        global stage
        result = {}
        with self.driver.session() as session:
            for s in ["stage i", "stage ii", "stage iii", "stage iv"]:
                stage = s
                result[stage] = session.read_transaction(self._stage_10_most_expressed_genes)
        return result
    @staticmethod
    def _stage_10_most_expressed_genes(tx):
        query = """MATCH (p:Patient) -[te:HAS_TUMORAL_EXPRESSION_OF] -> (g:Gene)
        WHERE p.pathologic_stage = "%s"
        RETURN g AS gene, avg(toFloat(te.expression)) AS tumoral_expression_avg
        ORDER BY tumoral_expression_avg DESC
        LIMIT 10""" % stage
        result = tx.run(query)
        values = [record.data() for record in result]
        return values


    def by_stage_10_least_expressed_genes(self):
        global stage
        result = {}
        with self.driver.session() as session:
            for s in ["stage i", "stage ii", "stage iii", "stage iv"]:
                stage = s
                result[stage] = session.read_transaction(self._stage_10_least_expressed_genes)
        return result
    @staticmethod
    def _stage_10_least_expressed_genes(tx):
        query = """MATCH (p:Patient) -[te:HAS_TUMORAL_EXPRESSION_OF] -> (g:Gene)
        WHERE p.pathologic_stage = "%s"
        RETURN g AS gene, avg(toFloat(te.expression)) AS tumoral_expression_avg
        ORDER BY tumoral_expression_avg
        LIMIT 10""" % stage
        result = tx.run(query)
        values = [record.data() for record in result]
        return values