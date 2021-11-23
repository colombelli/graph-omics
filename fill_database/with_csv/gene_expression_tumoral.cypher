:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///adj_list_separated/tumoral_gene_adj_list.csv" AS row WHERE row.expression IS NOT NULL
MERGE (gene:Gene {entrezGeneId: row.id, geneSymbol:row.symbol})
MERGE (patient:Patient {patientId: row.sample_id})
MERGE (patient)-[:HAS_TUMORAL_EXPRESSION_OF {expression:row.expression}]->(gene)