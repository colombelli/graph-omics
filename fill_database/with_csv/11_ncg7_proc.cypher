:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///NCG7_proc.csv" AS row 
MATCH (gene:Gene {entrezGeneId: row.entrez})
SET gene.ncg7CancerType = row.cancer_type
MERGE (ncggene: NCGgene {version: 7})
MERGE (gene)-[:IS {annotation: row.ncg_annotation}]->(ncggene)