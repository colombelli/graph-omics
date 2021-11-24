:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///.csv" AS row 
MERGE (gene:Gene {entrezGeneId: row.Gene_id})
MERGE (disgenet: Disgenet {version: 7})
MERGE (gene)-[:IS_PRESENT_IN {diseases: row.N_diseases, snps: row.N_SNPs}]->(disgenet)