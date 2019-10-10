import requests
from bs4 import BeautifulSoup


def extract_table(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find("table", {"id": "standings"}).find("tbody")
    result = []
    for row in table.find_all("tr"):
        cur_row = []
        if len(result) == 1:
            cur_row += [''] * 5
        for column in row.find_all("td"):
            cur_row += [''] * (int(column["colspan"]) - 1)
            cur_row.append(column.text)
        result.append(cur_row)
    return result


def proc(table):
    sum_indexes = []
    cnt = 0
    for j in range(len(table[1])):
        elem = table[1][j]
        if (len(elem) == 1) and ('A' <= elem[0] <= 'Z'):
            cnt += 1
        else:
            if cnt != 0:
                table[1][j] = table[0][j]
                sum_indexes.append(j)
            cnt = 0
    result = dict()
    for i in range(2, len(table)):
        name = table[i][2]
        result[name] = dict()
        for j in sum_indexes:
            if table[i][j] == "":
                table[i][j] = "0"
            solved = int(table[i][j])

            result_dict = {"solved": solved}
            result[name][table[1][j]] = result_dict

    return result


def main(url):
    table = extract_table(url)
    return proc(table)
