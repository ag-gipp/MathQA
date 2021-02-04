import math

path = "inverse_formula_index_results.csv"

with open(path,'r',encoding='utf8') as f:
    csv_list = f.readlines()

# calculate (n)DCG
tophit_score = 0
DCG_score = 0
IDCG_score = 0
GoldID_scores = {}
for line in csv_list[1:]:
    content = line.split("\t")
    GoldID = content[0]
    score = content[1]
    try:
        GoldID_scores[GoldID].append(score)
    except:
        GoldID_scores[GoldID] = []
        GoldID_scores[GoldID].append(score)

for GoldID in GoldID_scores.items():
    rank = 1
    for score in GoldID[1]:
        # tophit?
        if rank == 1 and int(score) > 0:
            tophit_score += 1
        # DCG formula
        DCG_score += int(score) / math.log2(rank+1)
        # IDCG rule
        if rank == 1:
            IDCG_score += 2
        else:
            IDCG_score += 0
        rank += 1

print("end")