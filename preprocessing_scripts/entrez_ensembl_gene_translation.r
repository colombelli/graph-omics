library("AnnotationDbi")
library("org.Hs.eg.db")
library("tibble")

get_entrez_id <- function(col_name) {
  return(tail(strsplit(col_name, "\\.")[[1]], n=1))
}

gene_expr_df <- read.csv(file="/home/colombelli/Documents/datasets/graph-omics/KIRC/gene_proc.csv")
genes <- colnames(gene_expr_df) 


entrez_ids <- c()
for (g in tail(genes, -1))
  entrez_ids <- c(entrez_ids, get_entrez_id(g))



ensembl_ids = mapIds(org.Hs.eg.db,
                     keys=entrez_ids, #Column containing entrez gene ids
                     column="ENSEMBL",
                     keytype="ENTREZID",
                     multiVals="first")


translation_df <- enframe(ensembl_ids)
colnames(translation_df) <- c("entrezid", "ensembl")

write.csv(translation_df, 
          "/home/colombelli/Documents/datasets/graph-omics/entrez_ensembl_translation.csv",
          row.names = FALSE)
