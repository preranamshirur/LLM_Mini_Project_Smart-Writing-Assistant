import json
from transliteration import convert_text

def cer(ref, hyp):
    a,b=ref, hyp
    dp=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        nd=[i]+[0]*len(b)
        for j,cb in enumerate(b,1):
            nd[j]=min(nd[j-1]+1, dp[j]+1, dp[j-1]+(ca!=cb))
        dp=nd
    return dp[-1]/max(1,len(a))

data=json.load(open("data/evaluation_samples.json",encoding="utf-8"))
scores=[]
for row in data:
    pred=convert_text(row["input"],row["language"])
    score=cer(row["reference"],pred)
    scores.append(score)
    print(f'{row["language"]:8} CER={score:.3f} | {row["input"]} -> {pred}')
print(f"Mean CER: {sum(scores)/len(scores):.3f}")
