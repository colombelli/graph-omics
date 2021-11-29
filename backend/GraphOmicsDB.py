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



    def avg_onco_tsg(self):
        with self.driver.session() as session:
            values = session.read_transaction(self._avg_onco_tsg)
        return values
    @staticmethod
    def _avg_onco_tsg(tx):
        query = """
        CALL {
            MATCH (g:Gene)-[:IS {annotation: "oncogene"}]->(ncg:NCGgene)
            MATCH (:Patient) -[onco_te:HAS_TUMORAL_EXPRESSION_OF] -> (g)
            RETURN avg(toFloat(onco_te.expression)) AS OP
        }

        CALL {
            MATCH (g:Gene)-[:IS {annotation: "oncogene"}]->(ncg:NCGgene)
            MATCH (:Patient) -[onco_ne:HAS_NORMAL_EXPRESSION_OF] -> (g)
            RETURN avg(toFloat(onco_ne.expression)) AS ON
        }

        CALL {
            MATCH (g:Gene)-[:IS {annotation: "tsg"}]->(ncg:NCGgene)
            MATCH (:Patient) -[tsg_te:HAS_TUMORAL_EXPRESSION_OF] -> (g)
            RETURN avg(toFloat(tsg_te.expression)) AS TP
        }

        CALL {
            MATCH (g:Gene)-[:IS {annotation: "tsg"}]->(ncg:NCGgene)
            MATCH (:Patient) -[tsg_ne:HAS_NORMAL_EXPRESSION_OF] -> (g)
            RETURN avg(toFloat(tsg_ne.expression)) AS TN
        }

        RETURN OP, ON, TP, TN
        """
        result = tx.run(query)
        values = [record.data() for record in result]
        return values[0]




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
        -[:INTERACTS_WITH]-> (:Protein) -[:ENCODE]- (gene:Gene) RETURN gene LIMIT 50""" % (gene_entrezGeneId)
        result = tx.run(query)
        return [record.data() for record in result]



    def mirna_target_gene_min_max(self):
        with self.driver.session() as session:
            values = session.read_transaction(self._mirna_target_gene_min_max)
        return values
    @staticmethod
    def _mirna_target_gene_min_max(tx):
        query = """
            call{
                call{

                    call {
                        MATCH (:Patient) -[ne:HAS_NORMAL_EXPRESSION_OF]-> (gn:Gene) return gn as gene, avg(toFloat(ne.expression)) as expression
                        UNION ALL
                        MATCH (:Patient) -[te:HAS_TUMORAL_EXPRESSION_OF]-> (gt:Gene) return gt as gene, avg(toFloat(te.expression)) as expression
                    }

                    return gene, expression ORDER BY expression
                    LIMIT 50
                }

                with gene
                match (mirna:miRNA)-[:MIRTARBASE_REGULATES]->(gene)
                return distinct(mirna.mirnaId) as mirnas, gene.entrezGeneId as genes
            }

            call {
                with mirnas
                call {
                    with mirnas
                    match (p:Patient)-[ne:HAS_NORMAL_EXPRESSION_OF]->(mi:miRNA)
                    where mi.mirnaId in mirnas
                    return min(toFloat(ne.expression)) as mirna_min_expr

                    union

                    with mirnas
                    match (p:Patient)-[te:HAS_TUMORAL_EXPRESSION_OF]->(mi:miRNA)
                    where mi.mirnaId in mirnas
                    return min(toFloat(te.expression)) as mirna_min_expr
                }

                call {
                    with mirnas
                    match (p:Patient)-[ne:HAS_NORMAL_EXPRESSION_OF]->(mi:miRNA)
                    where mi.mirnaId in mirnas
                    return max(toFloat(ne.expression)) as mirna_max_expr

                    union

                    with mirnas
                    match (p:Patient)-[te:HAS_TUMORAL_EXPRESSION_OF]->(mi:miRNA)
                    where mi.mirnaId in mirnas
                    return max(toFloat(te.expression)) as mirna_max_expr
                }

                return min(mirna_min_expr) as mirna_min_expr , max(mirna_max_expr) as mirna_max_expr
            }


            call {
                with genes
                call {
                    with genes
                    match (p:Patient)-[ne:HAS_NORMAL_EXPRESSION_OF]->(g:Gene)
                    where g.entrezGeneId in genes
                    return min(toFloat(ne.expression)) as gene_min_expr

                    union

                    with genes
                    match (p:Patient)-[te:HAS_NORMAL_EXPRESSION_OF]->(g:Gene)
                    where g.entrezGeneId in genes
                    return min(toFloat(te.expression)) as gene_min_expr
                }

                call {
                    with genes
                    match (p:Patient)-[ne:HAS_NORMAL_EXPRESSION_OF]->(g:Gene)
                    where g.entrezGeneId in genes
                    return max(toFloat(ne.expression)) as gene_max_expr

                    union

                    with genes
                    match (p:Patient)-[te:HAS_NORMAL_EXPRESSION_OF]->(g:Gene)
                    where g.entrezGeneId in genes
                    return max(toFloat(te.expression)) as gene_max_expr
                }

            return min(gene_min_expr) as gene_min_expr, max(gene_max_expr) as gene_max_expr 
            }

            return distinct mirnas as miRNA, genes as gene, mirna_min_expr as miRNA_ne_menor_eg, mirna_max_expr as miRNA_ne_maior_eg, gene_min_expr as menor_eg, gene_max_expr as maior_eg
        """
        result = tx.run(query)
        return [record.data() for record in result]