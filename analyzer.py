import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import json

print(*list(map(lambda x: x.split(".")[0], os.listdir("./opinions"))), sep="\n")
product_code = input("Podaj kod produktu: ")


opinions = pd.read_json(f"./opinions/{product_code}.json")
print(opinions)
opinions.score = opinions.score.map(lambda x: x.split("/")[0].replace(",",".")).astype(float)

stats = {
    "opinions_count": opinions.shape[0],
    "pros_count": opinions.pros.astype(bool).sum(),
    "cons_count": opinions.cons.astype(bool).sum(),
    "average_score": opinions.score.mean()
}
print(f'''Dla produktu o kodzie {product_code} pobrancyh zostało {stats["opinions_count"]} opinii.
Dla {stats["pros_count"]} opinii podana została lista zalet  produktu,
a dla {stats["cons_count"]} opinii lista jego wad.
Średnia ocena produktu wynosi {stats["average_score"]:.2f}.''')

if not os.path.exists("./plots"):
    os.mkdir("./plots")

score = opinions.score.value_counts().reindex(list(np.arange(0, 5.5, 0.5)), fill_value=0)
print(score)
score.plot.bar()
plt.savefig(f"./plots/{product_code}_score.png")
plt.close()

recommendation = opinions.recommendation.value_counts(dropna=False)
print(recommendation)
recommendation.plot.pie()
plt.savefig(f"./plots/{product_code}_recommendation.png")
plt.close()

if not os.path.exists("./stats"):
    os.mkdir("./stats")

stats["score"] = score.to_dict()
stats[recommendation] = recommendation.to_dict()
with open(f"./stats/{product_code}.json", "w", encoding="utf-8") as jf:
    json.dump(stats, jf, indent=4, ensure_ascii=False)