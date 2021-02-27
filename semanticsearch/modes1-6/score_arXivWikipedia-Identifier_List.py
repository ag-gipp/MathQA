import pandas as pd
from ast import literal_eval as make_tuple
import math

path = r"C:\Users\phili\Dropbox\PhD\Paper\upcoming\SemanticFormulaSearch\5d6b8d07b6030d2987d20b7b\evaluation\FormulaIdentifierRelationships(Modes1-6)"

arXiv_file = "EvaluationIdentifierNamesToSymbolsOrSymbolsToNames_arXiv(1).csv"
Wikipedia_file = "EvaluationIdentifierNamesToSymbolsOrSymbolsToNames_Wikipedia.csv"

def get_score(file_path):
    # get table
    table = pd.read_csv(file_path,sep=',')
    # get columns
    score_rank_col = table['(Score, Rank)']
    query_col = table['Query']
    # init metrics
    nr_relevant_mode12 = 0
    DCG_mode12 = 0
    nr_relevant_mode45 = 0
    DCG_mode45 = 0
    # init counter
    total_vals_mode12 = 0
    total_vals_mode45 = 0
    for idx,row in score_rank_col.iteritems():
        if row != '-' and str(row) != 'nan':
            score_ranks = row.split(", ")
            for score_rank in score_ranks:
                try:
                    score, rank = make_tuple(score_rank)
                except:
                    pass
                # rank cutoff
                if rank <= 10:
                    query = query_col.at[idx]
                    # distinguish modes by query (names=mode12, symbols=mode45)
                    # symbols=mode45
                    if len(query) == 1 or "\\" in query:
                        # update counter
                        total_vals_mode45 += 1
                        # update nr_relevant
                        if rank == 1 and score > 0:
                            nr_relevant_mode45 += 1
                        # update DCG
                        DCG_mode45 += score / math.log2(rank + 1)
                    # names=mode12
                    else:
                        # update counter
                        total_vals_mode12 += 1
                        # update nr_relevant
                        if rank == 1 and score > 0:
                            nr_relevant_mode12 += 1
                        # update DCG
                        DCG_mode12 += score / math.log2(rank + 1)

    # calculate top1 accuracy and mean(DCG)
    # mode12
    top1_acc_mode12 = nr_relevant_mode12/total_vals_mode12
    mean_DCG_mode12 = DCG_mode12/total_vals_mode12
    # mode45
    top1_acc_mode45 = nr_relevant_mode45/total_vals_mode45
    mean_DCG_mode45 = DCG_mode45/total_vals_mode45
    return {'top1_acc_mode12':top1_acc_mode12},{'mean_DCG_mode12':mean_DCG_mode12},\
           {'top1_acc_mode45':top1_acc_mode45},{'mean_DCG_mode45':mean_DCG_mode45}

arXiv_score = get_score(path + "/" + arXiv_file)
Wikipedia_score = get_score(path + "/" + Wikipedia_file)

print("end")