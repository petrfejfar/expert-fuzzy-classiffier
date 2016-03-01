import csv
import operator

def preprocessData(filename):
    with open(filename, 'rt') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
        data = [];
        for row in csv_reader:
            data.append(row)

        # find max and min in column
        mins = []
        maxs = []
        for col in range(4):
            max_value = max(row[col] for row in data)
            maxs.append(max_value)
            min_value = min(row[col] for row in data)
            mins.append(min_value)
        
        # normalize data
        for row in data:
            for col in range(len(mins)):
                row[col] = (row[col] - mins[col]) / (maxs[col] - mins[col]); 
                
        return data;

def ruleOr(a, b):
    return max(a, b)

def ruleAnd(a, b):
    return min(a, b)

def fuzOr(a, b):
    result = {};
    for property in a:
        result[property] = max(a[property], b[property]);
    return result;

def fuzAnd(a, b):
    result = {};
    for property in a:
        result[property] = min(a[property], b[property]);
    return result;

def fuz(value):
    if(value < 0 or value > 1):
        raise ValueError("Argument out of range")
    result = {};
    
    result["short"] = max(0, value/-0.6 + 1);
    result["middle"] = min(value*-2.5 + 2.5, value/0.6);
    result["long"] = max(0, value*2.5 - 1.5);
    return result;


def strengthOfR1(x1, x2, x3, x4):
    return  ruleAnd(
                ruleAnd(
                    ruleOr(fuz(x1)["short"], fuz(x1)["long"]),
                    ruleOr(fuz(x2)["middle"], fuz(x2)["long"])
                    ),
                ruleAnd(
                    ruleOr(fuz(x3)["middle"], fuz(x3)["long"]),
                    fuz(x4)["middle"]
                    )
                )

def strengthOfR2(x1, x2, x3, x4):
    return  ruleAnd(
                ruleOr(fuz(x3)["short"], fuz(x3)["middle"]),
                fuz(x4)["short"]
                )
                

def strengthOfR3(x1, x2, x3, x4):
    return  ruleAnd(
                ruleAnd(
                    ruleOr(fuz(x2)["short"], fuz(x2)["middle"]),
                    fuz(x3)["long"]
                    ),
                fuz(x4)["long"]    
                )


def strengthOfR4(x1, x2, x3, x4):
    return  ruleAnd(
                ruleAnd(
                    fuz(x1)["middle"],
                    ruleOr(fuz(x2)["short"], fuz(x2)["middle"])
                    ),
                ruleAnd(
                    fuz(x3)["short"],
                    fuz(x4)["long"]
                    )
                )

def classify(x1, x2, x3, x4):
    return {
        "versicolor": strengthOfR1(x1, x2, x3, x4) + strengthOfR4(x1, x2, x3, x4),
        "setosa": strengthOfR2(x1, x2, x3, x4),
        "virginica": strengthOfR3(x1, x2, x3, x4)}


hit = 0;
miss = 0;
bird_map = {1: "setosa", 2: "versicolor", 3: "virginica"};
for row in preprocessData("iris.txt"):
    if bird_map[row[4]] == max(classify(row[0], row[1], row[2], row[3]).items(),key=operator.itemgetter(1))[0]:
        hit += 1;
    else:
        miss += 1;

print("%.2f" % (100.0 * hit / (hit + miss)))
