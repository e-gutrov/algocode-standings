import json
import arrow

import get_standings

url = "https://algocode.ru/standings/43/"
url = f"http://0.0.0.0:8050/render.html?url={url}&wait=2"

new_results = get_standings.main(url)
with open("results.json", "r") as fin:
    old_results = json.load(fin)
with open("contests.json", "r") as fin:
    contests = json.load(fin)
for contest in contests:
    contests[contest]["start"] = arrow.get(contests[contest]["start"], "DD.MM.YYYY")

now = arrow.now()

for name in new_results:
    if name not in old_results:
        old_results[name] = dict()
    for contest in new_results[name]:
        if contest in old_results[name]:
            old_mark = old_results[name][contest].get("mark", 0)
            old_solved = old_results[name][contest]["solved"]
        else:
            old_mark = 0
            old_solved = 0
        new_solved = new_results[name][contest]["solved"]

        if (now - contests[contest]["start"]).days > contests[contest].get("duration", 14):
            mul = 1
        else:
            mul = 2
        new_results[name][contest]["mark"] = old_mark +\
            (new_solved - old_solved) * mul / (2 * contests[contest]["tasks"])

print(new_results)
with open("new_results.json", "w") as fout:
    json.dump(new_results, fp=fout,
              ensure_ascii=False, indent=2)
