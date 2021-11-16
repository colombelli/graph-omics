library(biomaRt)
library(httr)

httr::set_config(httr::config(ssl_verifypeer = FALSE))

get_entrez_id <- function(col_name) {
  return(tail(strsplit(col_name, "\\.")[[1]], n=1))
}

gene_expr_df <- read.csv(file="/home/colombelli/Documents/datasets/graph-omics/KIRC/gene_proc.csv")
genes <- colnames(gene_expr_df) 


entrez_ids <- c()
for (g in tail(genes, -1))
  entrez_ids <- c(entrez_ids, get_entrez_id(g))


mart <- useMart(biomart = "ensembl", dataset = "hsapiens_gene_ensembl")
results <- getBM(attributes = c("entrezgene_id", "ensembl_gene_id_version", 
                                "ensembl_gene_id", "ensembl_peptide_id"), 
                 filters = "entrezgene_id",
                 values = entrez_ids, mart = mart, verbose=TRUE)

write.csv(results, 
          "/home/colombelli/Documents/datasets/graph-omics/gene_translation.csv",
          row.names = FALSE)
