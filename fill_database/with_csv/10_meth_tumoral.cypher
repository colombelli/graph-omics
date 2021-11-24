:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///adj_list_separated/tumoral_meth_adj_list.csv" AS row WITH row WHERE row.expression IS NOT NULL
MERGE (gene:Gene {geneSymbol: row.symbol})
MERGE (patient:Patient {patientId: row.sample_id})
MERGE (patient)-[:HAS_TUMORAL_METHYLATION_OF {methylation:row.expression}]->(gene)