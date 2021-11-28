from neo4j import GraphDatabase

class GraphOmicsDB:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()


    def merge_fix_ncg7(self):
        with self.driver.session() as session:
            session.write_transaction(self._merge_fix_ncg7)
        return
    @staticmethod
    def _merge_fix_ncg7(tx):
        query = """match (g1:Gene) 
                match(g2:Gene) 
                where g1.entrezGeneId = g2.entrezGeneId and id(g1) <> id(g2) and g2.ncg7CancerType is not null 
                with [g1,g2] as gs
                with * limit 1
                call apoc.refactor.mergeNodes(gs) yield node 
                return node"""
        while True:
            r = tx.run(query)
            print(r.values())
        return 

    
    def merge_fix_symbol(self):
        with self.driver.session() as session:
            session.write_transaction(self._merge_fix_symbol)
        return
    @staticmethod
    def _merge_fix_symbol(tx):
        query = """match (g1:Gene) 
                match(g2:Gene) 
                where g1.entrezGeneId = g2.entrezGeneId and id(g1) <> id(g2) and g2.geneSymbol is not null 
                with [g1,g2] as gs
                with * limit 1
                call apoc.refactor.mergeNodes(gs) yield node 
                return node"""
        counter=0
        while True:
            counter+=1
            print(counter)
            tx.run(query)
        return 


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


	def by_stage_most_expressed_genes_ppi_net(self):
	    global gene_entrezGeneId
	    result = self.by_stage_10_most_expressed_genes()
	    with self.driver.session() as session:
	        for s in result.keys():
	            i = 0
	            for gene in result[stage]:
	                gene_entrezGeneId = gene['gene']['entrezGeneId']
	                result[s][i]['lst_genes_ppi'] = session.read_transaction(self._stage_gene_ppi_net)
	                i += 1
	    return result
	@staticmethod
	def _stage_gene_ppi_net(tx):
	    query = """MATCH (:Gene {entrezGeneId: "%s"}) -[:ENCODE]-> (:Protein) 
	    -[:INTERACTS_WITH]-> (:Protein) -[:ENCODE]- (gene:Gene) RETURN gene""" % (gene_entrezGeneId)
	    result = tx.run(query)
	    return [record.data() for record in result]
