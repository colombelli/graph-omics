:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///ppi_selected_genes.csv" AS row 
MATCH (protein1:Protein {ensemblProteinId: row.protein1})
MATCH (protein2:Protein {ensemblProteinId: row.protein2})
MERGE (protein1)-[:INTERACTS_WITH {score:row.combined_score}]->(protein2)