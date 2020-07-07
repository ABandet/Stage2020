import csv

def get_cvs_rows(path):
    rows = []
    # get all rows
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
        return rows

    raise Exception('cannot open file {}'.format(path))

def get_col_index(rows, name):
    idx = 0
    for tag in rows[0]:
        if (name == tag):
            return idx
        idx += 1
    
    raise Exception('could not find column name {}'.format(name))

def get_col_data(rows, idx):
    data = []
    for i in range(1, len(rows)):
        data.append(rows[i][idx])
    return data


def add_two_list(liste1, liste2):
    sum = []
    for i in range(min(len(liste1), len(liste2))):
        sum.append(liste1[i] + liste2[i])
    return sum

def div_two_list(liste1, liste2):
    div = []
    for i in range(min(len(liste1), len(liste2))):
        div.append(liste1[i] / liste2[i])
    return div


def convert_to_float(liste):
    tmp = []
    for i in range (len(liste)):
        tmp.append(float(liste[i]))
    return tmp

def convert_to_int(liste):
    for i in range (len(liste)):
        liste[i] = int(liste[i])
