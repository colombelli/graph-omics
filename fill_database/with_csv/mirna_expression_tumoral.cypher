:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///adj_list_separated/tumoral_mirna_adj_list.csv" AS row WITH row WHERE row.expression IS NOT NULL
MERGE (mirna:miRNA {mirnaId: row.symbol, mirnaMIMAT: row.id})
MERGE (patient:Patient {patientId: row.sample_id})
MERGE (patient)-[:HAS_TUMORAL_EXPRESSION_OF {expression:row.expression}]->(mirna)