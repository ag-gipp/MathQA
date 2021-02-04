import math

file_path = r"C:\Users\phili\Dropbox\PhD\Paper\upcoming\SemanticFormulaSearch\5d6b8d07b6030d2987d20b7b\evaluation\FormulaIdentifierQuestions(Modes7-12)\SemanticSearch_WikidataMode9_allhits.csv"

with open(file_path,'r',encoding='utf8') as f:
    csv_lines = f.readlines()

scores = {}
for line in csv_lines[1:]:
    line = line.split("\t")
    name = line[0]
    score = line[1]
    try:
        scores[name].append(score)
    except:
        scores[name] = [score]

DCG_scores_dict = {}
DCG_scores_list = []
tops = 0
for result in scores.items():
    name = result[0]

    scores_ten = result[1][:10]
    tops += int(any(int(score) > 0 for score in scores_ten[:10]))

    rank = 1
    DCG_scores_dict[name] = 0
    for score in scores_ten:
        DCG_scores_dict[name] += int(score) / math.log2(rank+1)
        rank += 1
    DCG_scores_list.append(DCG_scores_dict[name])

mean_DCG = sum(DCG_scores_list)/66
top1_acc = tops/66

print("end")