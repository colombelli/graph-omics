:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///c6v74_adj_list.csv" AS row 
MERGE (gene:Gene {entrezGeneId: row.gene})
MERGE (c6geneset:C6geneset {geneSet: row.pathway, info: row.pathway_info})
MERGE (gene)-[:MEMBER_OF]->(c6geneset)