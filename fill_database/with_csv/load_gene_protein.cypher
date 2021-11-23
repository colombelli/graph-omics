:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///home/colombelli/Documents/datasets/graph-omics/data/gene_translation.csv" AS row
MERGE (gene:Gene {entrezGeneId: row.entrezgene_id, ensemblGeneId: row.ensembl_gene_id})
MERGE (protein:Protein {proteinId: row.OrderID})