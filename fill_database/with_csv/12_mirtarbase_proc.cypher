:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///mirtarbase_proc.csv" AS row 
MERGE (mirna:miRNA {mirnaId: row.mirna_id})
MERGE (gene: Gene {entrezGeneId: row.Target_Gene_Entrez})
MERGE (mirna)-[:MIRTARBASE_REGULATES {pmidRef: row.References_PMID}]->(gene)