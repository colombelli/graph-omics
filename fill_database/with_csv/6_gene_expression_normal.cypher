:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///adj_list_separated/normal_gene_adj_list.csv" AS row WITH row WHERE row.expression IS NOT NULL
MATCH (gene:Gene {entrezGeneId: row.id})
SET gene.geneSymbol = row.symbol
MERGE (patient:Patient {patientId: row.sample_id})
MERGE (patient)-[:HAS_NORMAL_EXPRESSION_OF {expression:row.expression}]->(gene)