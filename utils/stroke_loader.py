from yac_client import stroke as stroke
import csv

def load(path):
    with open(path) as f:
        reader = csv.reader(f)
        data = [i for i in reader]
        data = [[float(j) for j in i] for i in data[1:]]
        return [stroke.Stroke(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12]) for i in data]