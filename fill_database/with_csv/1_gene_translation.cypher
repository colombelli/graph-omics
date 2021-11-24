:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///gene_translation.csv" AS row
MERGE (gene:Gene {entrezGeneId: row.entrezgene_id, ensemblGeneId: row.ensembl_gene_id})
MERGE (protein:Protein {ensemblProteinId: row.ensembl_peptide_id})
MERGE (gene)-[:ENCODE]->(protein)