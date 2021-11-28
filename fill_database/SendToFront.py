#Envia as infos com os dados das funcionalidades básicas para o front-end
#query_selecionada seria o a questão do relatório Ex: B_UM, B_DOIS, B_TRES, B_QUATRO, B_CINCO
def send_basicas_to_front(query_selecionada):

    data = {}

    data['B_UM'] = {"descricao": "Ut molestie felis id metus molestie sodales.",
                    "dados": [{'gene': "a", 'valor': 100}, {'gene': "b", 'valor': 69},
                              {'gene': "c", 'valor': 79}, {'gene': "d", 'valor': 88},
                              {'gene': "e", 'valor': 90}, {'gene': "f", 'valor': 79},
                              {'gene': "g", 'valor': 19}, {'gene': "h", 'valor': 39},
                              {'gene': "i", 'valor': 38}, {'gene': "j", 'valor': 90}]
                    }
    data['B_DOIS'] = {
        "descricao": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus vel risus in felis suscipit pellentesque. Nullam ac mauris vitae purus molestie efficitur quis vitae nibh.",
        "dados": [{'gene': "x", 'valor': 10}, {'gene': "r", 'valor': 6}, {'gene': "t", 'valor': 7},
                  {'gene': "y", 'valor': 1}, {'gene': "q", 'valor': 4},
                  {'gene': "z", 'valor': 2}, {'gene': "s", 'valor': 5}, {'gene': "u", 'valor': 9},
                  {'gene': "w", 'valor': 3}, {'gene': "v", 'valor': 7}]
        }
    data['B_TRES'] = {
        "descricao": "Nulla dapibus pretium odio, eget tempor tortor lobortis sed. Praesent at massa egestas, ultricies velit vel, dapibus tortor. Donec consectetur leo nec urna congue placerat. ",
        "dados": [{'gene': "a", 'valor': 100}, {'gene': "b", 'valor': 69}, {'gene': "c", 'valor': 79},
                  {'gene': "d", 'valor': 88}, {'gene': "e", 'valor': 90},
                  {'gene': "f", 'valor': 79}, {'gene': "g", 'valor': 19}, {'gene': "h", 'valor': 39},
                  {'gene': "i", 'valor': 38}, {'gene': "j", 'valor': 90}]
        }
    data['B_QUATRO'] = {"descricao": "",
                        "dados": [{'gene': "x", 'valor': 10}, {'gene': "r", 'valor': 6}, {'gene': "t", 'valor': 7},
                                  {'gene': "y", 'valor': 1}, {'gene': "q", 'valor': 4},
                                  {'gene': "z", 'valor': 2}, {'gene': "s", 'valor': 5}, {'gene': "u", 'valor': 9},
                                  {'gene': "w", 'valor': 3}, {'gene': "v", 'valor': 7}]
                        }
    data['B_CINCO'] = {
        "descricao": "Aenean ac luctus metus. Maecenas eros tellus, tincidunt eu sagittis quis, tempor nec eros. Vivamus tempus vehicula tellus ut egestas. Morbi vitae magna eget enim tristique finibus.",
        "dados": [{'gene': "a", 'valor': 100}, {'gene': "b", 'valor': 69}, {'gene': "c", 'valor': 79},
                  {'gene': "d", 'valor': 88}, {'gene': "e", 'valor': 90},
                  {'gene': "f", 'valor': 79}, {'gene': "g", 'valor': 19}, {'gene': "h", 'valor': 39},
                  {'gene': "i", 'valor': 38}, {'gene': "j", 'valor': 90}]
        }
    data['B_SEIS'] = {
        "descricao": "Quisque mollis magna vitae justo sollicitudin, ut rutrum ligula eleifend. Sed laoreet sit amet arcu sed gravida. Duis facilisis enim vitae dictum faucibus.",
        "dados": [{'gene': "x", 'valor': 10}, {'gene': "r", 'valor': 6}, {'gene': "t", 'valor': 7},
                  {'gene': "y", 'valor': 1}, {'gene': "q", 'valor': 4},
                  {'gene': "z", 'valor': 2}, {'gene': "s", 'valor': 5}, {'gene': "u", 'valor': 9},
                  {'gene': "w", 'valor': 3}, {'gene': "v", 'valor': 7}]
        }
    # Saber se esses genes (os mais e menos expressos de cada cenário) estão associados a
    # mais alguma doença além de KIRC#
    data['B_SETE'] = {
        "descricao": "Interdum et malesuada fames ac ante ipsum primis in faucibus. Cras tincidunt in erat non interdum. Integer libero enim, condimentum sed gravida et, luctus vel nulla. Nulla dapibus pretium odio, eget tempor tortor lobortis sed. Praesent at massa egestas, ultricies velit vel, dapibus tortor. Donec consectetur leo nec urna congue placerat. Aenean aliquet finibus turpis. Etiam odio risus, dapibus id ante ut, luctus pretium tortor. ",
        "dados": [{'gene': "x", 'proveniencia': 'tecido tumoral', 'valor': 10, 'doencas': ['Doença a', 'KIRC']},
                  {'gene': "r", 'proveniencia': 'tecido adjacente ao tumor (normais/saudaveis)', 'valor': 6,
                   'doencas': ['KIRC', 'Doença b', 'Doença c']},
                  {'gene': "t", 'proveniencia': 'tecido tumoral', 'valor': 7,
                   'doencas': ['KIRC', 'Doença ab', 'Doença a', 'Doença b']},
                  {'gene': "y", 'proveniencia': 'tecido tumoral (por estagio)', 'valor': 1, 'doencas': ['KIRC']},
                  {'gene': "q", 'proveniencia': 'tecido tumoral', 'valor': 4, 'doencas': ['Doença a', 'KIRC']},
                  {'gene': "z", 'proveniencia': 'tecido adjacente ao tumor (normais/saudaveis)', 'valor': 2,
                   'doencas': ['Doença c', 'KIRC']},
                  {'gene': "s", 'proveniencia': 'tecido adjacente ao tumor (normais/saudaveis)', 'valor': 5,
                   'doencas': ['KIRC']},
                  {'gene': "u", 'proveniencia': 'tecido tumoral (por estagio)', 'valor': 9,
                   'doencas': ['KIRC', 'Doença b']},
                  {'gene': "w", 'proveniencia': 'tecido tumoral (por estagio)', 'valor': 3,
                   'doencas': ['KIRC', 'Doença d']},
                  {'gene': "v", 'proveniencia': 'tecido tumoral', 'valor': 7, 'doencas': ['KIRC']}]
        }

    # json_data = json.dumps(data)
    # print('JSON: ', json_data)
    if query_selecionada is None:
        return data
    else:
        return data[query_selecionada]


#Envia as infos com os dados das funcionalidades avançadas para o front-end
#query_selecionada seria o a questão do relatório Ex: A_UM, A_DOIS, A_TRES, A_QUATRO, A_CINCO
def send_avancadas_to_front(query_selecionada):
    data = {}

    # Consultar qual a expressão média dos oncogenes e genes tumor-supressores nas amostras
    # positivas para KIRC e nas amostras negativas para KIRC.
    data['A_UM'] = {
                      "descricao": "",
                      "OP":"expressao1",
                      "ON":"expressao2",
                      "TSP": "expressao3",
                      "TSN": "expressao4"
                 }

    # Para os genes mais expressos em cada estágio tumoral, visualizar que outros genes interagem com ele
    # (através da rede PPI). Queremos entender se a expressão desses outros genes é afetada comparando entre
    # estágios tumorais e entre amostras positivas e negativas para KIRC.
    data['A_DOIS'] = {
                          "descricao": "",
                          "dados" :[
                                    {
                                        'estagio': "Estágio x",
                                        'genes_maix_exp': [
                                                            {"gene": "r", "expressao":123,"KIRK":"+",
                                                                "lst_genes_ppi": [
                                                                    {"gene": "r", "expressao": 123}
                                                                ]
                                                            },
                                                            {"gene": "s", "expressao": 35,"KIRK":"-",
                                                                 "lst_genes_ppi": [
                                                                     {"gene": "r", "expressao": 123},
                                                                     {"gene": "s", "expressao": 35}
                                                                 ]
                                                             },
                                                            {"gene": "t", "expressao": 678,"KIRK":"-",
                                                             "lst_genes_ppi": [
                                                                 {"gene": "t", "expressao": 678},
                                                                 {"gene": "s", "expressao": 35}
                                                                ]
                                                             }
                                                         ]
                                        },
                                    {
                                  'estagio': "Estágio a",
                                  'genes_maix_exp': [
                                      {"gene": "r", "expressao": 123, "KIRK": "+",
                                       "lst_genes_ppi": [
                                           {"gene": "r", "expressao": 123}
                                       ]
                                       },
                                      {"gene": "s", "expressao": 35, "KIRK": "-",
                                       "lst_genes_ppi": [
                                           {"gene": "r", "expressao": 123},
                                           {"gene": "s", "expressao": 35}
                                       ]
                                       },
                                      {"gene": "t", "expressao": 678, "KIRK": "-",
                                       "lst_genes_ppi": [
                                           {"gene": "t", "expressao": 678},
                                           {"gene": "s", "expressao": 35}
                                       ]
                                       }
                                  ]
                              }
                                    ]
                     }

    #Dentre os genes menos expressos, entender se eles são conhecidamente regulados por algum miRNA e, nas
    # suas amostras com maior e menor expressão gênica, saber qual é o miRNA que os regula
    # (se catalogado pelo miRTarBase) assim como o nível de expressão desses miRNAs em cada caso.
    data['A_TRES'] = {"descricao":"opcional opcional",
                      "dados" :[
                                {'gene': "a", 'miRNA': "aasda",
                                    'maior_eg': 1023, 'miRNA_maior_eg': "aa",'miRNA_ne_maior_eg': 90,
                                    'menor_eg': 3, 'miRNA_menor_eg': "aa", 'miRNA_ne_menor_eg': 2
                                },
                                {'gene': "b", 'miRNA': "aas",
                                 'maior_eg': 234, 'miRNA_maior_eg': "aa", 'miRNA_ne_maior_eg': 54,
                                 'menor_eg': 1, 'miRNA_menor_eg': "aa", 'miRNA_ne_menor_eg': 7
                                 }
                               ]}


    #Analisar se existe alguma diferença estatística na expressão dos oncogenes e genes supressores
    # do tumor entre cada estágio tumoral.
    data['A_QUATRO'] = {
        "descricao": "",
        "oncogene": [ {"estagio": "a","expressao":10},{"estagio": "b","expressao":102}],
        "gene_supressor":  [ {"estagio": "a","expressao":7},{"estagio": "b","expressao":502}]
    }

    # A5: Analisar se existe alguma diferença estatística na metilação dos oncogenes e dos
    # genes supressores do tumor entre as amostras tumorais e as normais.
    data['A_CINCO'] = {
                       "descricao":"",
                       "OAT": "oncogene - amostra tumoral",
                       "OAN": "oncogene - amostra normal",
                       "GAT": "gene supressor - amostra tumoral",
                       "GAN": "gene supressor - amostra normal"
                      }

    #Para cada estágio tumoral, verificar se os genes mais expressos (média de expressão dentre
    # todas as amostras daquele estágio) compõe alguma via biológica comumente desregulada na presença de
    # câncer, e que vias são estas.


    if query_selecionada is None:
        return data
    else:
        return data[query_selecionada]