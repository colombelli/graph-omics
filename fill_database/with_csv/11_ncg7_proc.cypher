:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///NCG7_proc.csv" AS row 
MATCH (gene:Gene {entrezGeneId: row.entrez})
MERGE (ncggene: NCGgene {version: 7})
MERGE (gene)-[:IS {annotation: row.ncg_annotation, cancerType: row.cancer_type}]->(ncggene)