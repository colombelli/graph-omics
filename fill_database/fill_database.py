"""
	To use, start de database (tutorial in https://neo4j.com/videos/getting-started-with-neo4j-desktop-1-2-7-on-linux/) 
	and download [gene, mirna, meth]_proc in the same path of the script. Then, simply run. To generate .txt files
	with the cypher queries, uncomment the code blocks.
"""
import numpy as np
from neo4j import GraphDatabase


class GraphDatabaseConnection:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query):
        with self.driver.session() as session:
            return_statement = session.write_transaction(self._run_and_return_result, query)
            # print(return_statement)

    @staticmethod
    def _run_and_return_result(tx, query):
        """
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        """
        result = tx.run(query)
        return result.single()


sample_col = 0
sample_lin = 1
gene_lin = 0
gene_col = 1
mirna_lin = 0
mirna_col = 1
tumor_class = "1"

delete_all = "MATCH (all) DETACH DELETE all"


def column(matrix, i):
    return [row[i] for row in matrix]


def create_sample_nodes(samples_list, db):
    print("Creating sample nodes...")
    for sample in samples_list:
        if sample != "index" and sample != "":
            create_sample_query = "MERGE (sample:Sample {tcgaBarcode: '"+sample+"'}) RETURN sample"
            db.run_query(create_sample_query)
            """
            with open('create_sample_nodes.txt', 'a') as sample_nodes_file:
                sample_nodes_file.write(create_sample_query + '\n')
            """


# GENE -----------------------------------------------------------------------------------------------------------------
def create_gene_nodes(genes_list, db):
    print("Creating gene nodes...")

    for gene in genes_list:
        if gene != "index" and gene != "class":
            gene_symbol = gene.split('|')[0]
            gene_id = gene.split('|')[1]
            create_gene_query = "MERGE (gene:Gene {id: "+gene_id+", symbol: '"+gene_symbol+"'}) RETURN gene"
            db.run_query(create_gene_query)
            """
            with open('create_gene_nodes.txt', 'a') as gene_nodes_file:
                gene_nodes_file.write(create_gene_query + '\n')
            """


def create_expression_edges(expression_grid, db):
    print("Creating expression edges...")
    class_col = len(expression_grid[0]) - 1  # 20532
    num_of_samples = len(expression_grid)

    for lin in range(sample_lin, num_of_samples):
        for col in range(gene_col, class_col - 1):
            if expression_grid[lin][col] != "":
                score = " {score: " + expression_grid[lin][col] + "}"
                gene_id = expression_grid[gene_lin][col].split('|')[1]
                sample_barcode = expression_grid[lin][sample_col]
                if expression_grid[lin][class_col] == tumor_class:
                    generate_tumoral_expression_query(gene_id, sample_barcode, score, db)
                else:
                    generate_normal_expression_query(gene_id, sample_barcode, score, db)


def generate_tumoral_expression_query(gene_id, sample_barcode, score, db):
    create_tumoral_expression_query = "MATCH (sample:Sample {tcgaBarcode:'"+sample_barcode+"'}) " \
                                      "MATCH (gene:Gene {id: "+gene_id+"}) CREATE (sample) " \
                                      "-[tumex: HAS_TUMORAL_EXPRESSION_OF" + score + "]-> (gene) " \
                                      "RETURN sample, tumex, gene"
    db.run_query(create_tumoral_expression_query)
    """
    with open('create_tumoral_expression_edges.txt', 'a') as tumoral_expression_edges_file:
        tumoral_expression_edges_file.write(create_tumoral_expression_query + '\n')
    """


def generate_normal_expression_query(gene_id, sample_barcode, score, db):
    create_normal_expression_query = "MATCH (sample:Sample {tcgaBarcode:'"+sample_barcode+"'}) " \
                                     "MATCH (gene:Gene {id: "+gene_id+"}) CREATE (sample) " \
                                     "-[norex: HAS_NORMAL_EXPRESSION_OF" + score + "]-> (gene) " \
                                     "RETURN sample, norex, gene"
    db.run_query(create_normal_expression_query)
    """
    with open('create_normal_expression_edges.txt', 'a') as normal_expression_edges_file:
        normal_expression_edges_file.write(create_normal_expression_query + '\n')
    """


def insert_from_gene_proc(db):
    sg = np.loadtxt(open("gene_proc.csv", "rb"), delimiter=",", dtype=str)

    create_gene_nodes(sg[gene_lin], db)
    create_sample_nodes(column(sg, sample_col), db)
    create_expression_edges(sg, db)
# END GENE -------------------------------------------------------------------------------------------------------------


# miRNA ----------------------------------------------------------------------------------------------------------------
def create_mirna_nodes(mirna_list, db):
    print("Creating miRNA nodes...")
    for mirna in mirna_list:
        if mirna != "index" and mirna != "class":
            mirna_id = mirna.split('|')[0]
            mirna_mimat = mirna.split('|')[1]
            create_mirna_query = "MERGE (mirna:miRNA {id: '"+mirna_id+"', mimat: '"+mirna_mimat+"'}) RETURN mirna"
            db.run_query(create_mirna_query)
            """
            with open('create_mirna_nodes.txt', 'a') as mirna_nodes_file:
                mirna_nodes_file.write(create_mirna_query + '\n')
            """


def create_mirna_expression_edges(expression_grid, db):
    print("Creating miRNA expression edges...")
    class_col = len(expression_grid[0]) - 1
    num_of_samples = len(expression_grid)

    for lin in range(sample_lin, num_of_samples):
        for col in range(mirna_col, class_col - 1):
            if expression_grid[lin][col] != "":
                score = " {score: " + expression_grid[lin][col] + "}"
                mirna_id = expression_grid[gene_lin][col].split('|')[0]
                sample_barcode = expression_grid[lin][sample_col]
                if expression_grid[lin][class_col] == tumor_class:
                    generate_mirna_tumoral_expression_query(mirna_id, sample_barcode, score, db)
                else:
                    generate_mirna_normal_expression_query(mirna_id, sample_barcode, score, db)


def generate_mirna_tumoral_expression_query(mirna_id, sample_barcode, score, db):
    create_tumoral_expression_query = "MATCH (sample:Sample {tcgaBarcode:'"+sample_barcode+"'}) " \
                                      "MATCH (mirna:miRNA {id: '"+mirna_id+"'}) " \
                                      "CREATE (sample) -[tumex: HAS_TUMORAL_EXPRESSION_OF" + score + "]-> (mirna) " \
                                      "RETURN sample, tumex, mirna"
    db.run_query(create_tumoral_expression_query)
    """
    with open('create_mirna_tumoral_expression_edges.txt', 'a') as tumoral_expression_edges_file:
        tumoral_expression_edges_file.write(create_tumoral_expression_query + '\n')
    """


def generate_mirna_normal_expression_query(mirna_id, sample_barcode, score, db):
    create_normal_expression_query = "MATCH (sample:Sample {tcgaBarcode:'" + sample_barcode + "'}) " \
                                     "MATCH (mirna:miRNA {id: '"+mirna_id+"'}) " \
                                     "CREATE (sample) -[norex: HAS_NORMAL_EXPRESSION_OF" + score + "]-> (mirna) " \
                                     "RETURN sample, norex, mirna"
    db.run_query(create_normal_expression_query)
    """
    with open('create_mirna_normal_expression_edges.txt', 'a') as normal_expression_edges_file:
        normal_expression_edges_file.write(create_normal_expression_query + '\n')
    """


def insert_from_mirna_proc(db):
    sm = np.loadtxt(open("mirna_proc.csv", "rb"), delimiter=",", dtype=str)

    create_sample_nodes(column(sm, sample_col), db)
    create_mirna_nodes(sm[mirna_lin], db)
    create_mirna_expression_edges(sm, db)
# END miRNA ------------------------------------------------------------------------------------------------------------


# methylation ----------------------------------------------------------------------------------------------------------
def create_gene_nodes_from_symbol(genes_list, db):
    print("Creating gene nodes for methylation...")

    for gene_symbol in genes_list:
        if gene_symbol != "index" and gene_symbol != "class" and gene_symbol != "":
            create_gene_query = "MERGE (gene:Gene {symbol: '"+gene_symbol+"'}) RETURN gene"
            db.run_query(create_gene_query)
            """
            with open('create_meth_gene_nodes.txt', 'a') as gene_nodes_file:
                gene_nodes_file.write(create_gene_query + '\n')
            """


def create_methylation_edges(methylation_grid, db):
    print("Creating methylation edges...")
    class_col = len(methylation_grid[0]) - 1
    num_of_samples = len(methylation_grid)

    for lin in range(sample_lin, num_of_samples):
        for col in range(gene_col, class_col - 1):
            if methylation_grid[lin][col] != "":
                score = " {score: " + methylation_grid[lin][col] + "}"
                gene_symbol = methylation_grid[gene_lin][col]
                sample_barcode = methylation_grid[lin][sample_col]
                if methylation_grid[lin][class_col] == tumor_class:
                    generate_tumoral_methylation_query(gene_symbol, sample_barcode, score, db)
                else:
                    generate_normal_methylation_query(gene_symbol, sample_barcode, score, db)


def generate_tumoral_methylation_query(gene_symbol, sample_barcode, score, db):
    create_tumoral_methylation_query = "MATCH (sample:Sample {tcgaBarcode:'"+sample_barcode+"'}) " \
                                      "MATCH (gene:Gene {symbol: '"+gene_symbol+"'}) " \
                                      "CREATE (sample) -[tumeth: HAS_TUMORAL_METHYLATION_OF" + score + "]-> (gene) " \
                                      "RETURN sample, tumeth, gene"
    db.run_query(create_tumoral_methylation_query)
    """
    with open('create_tumoral_methylation_edges.txt', 'a') as tumoral_methylation_edges_file:
        tumoral_methylation_edges_file.write(create_tumoral_methylation_query + '\n')
    """


def generate_normal_methylation_query(gene_symbol, sample_barcode, score, db):
    create_normal_methylation_query = "MATCH (sample:Sample {tcgaBarcode:'" + sample_barcode + "'}) " \
                                     "MATCH (gene:Gene {symbol: '"+gene_symbol+"'}) " \
                                     "CREATE (sample) -[nometh: HAS_NORMAL_METHYLATION_OF" + score + "]-> (gene) " \
                                     "RETURN sample, nometh, gene"
    db.run_query(create_normal_methylation_query)
    """
    with open('create_normal_methylation_edges.txt', 'a') as normal_methylation_edges_file:
        normal_methylation_edges_file.write(create_normal_methylation_query + '\n')
    """


def insert_from_meth_proc(db):
    sgm = np.loadtxt(open("meth_proc.csv", "rb"), delimiter=",", dtype=str)

    create_gene_nodes_from_symbol(sgm[gene_lin], db)
    create_sample_nodes(column(sgm, sample_col), db)
    create_methylation_edges(sgm, db)
# END methylation ------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    database = GraphDatabaseConnection("bolt://localhost:7687", "neo4j", "sgbd_senha")
    try:
        print("Clearing database...")
        database.run_query(delete_all)
        print("Database clear.\n")

        insert_from_gene_proc(database)
        insert_from_mirna_proc(database)
        insert_from_meth_proc(database)

        print("\nDone! :D")
    except Exception as e:  # work on python 3.x
        print(str(e))
    finally:
        database.close()




