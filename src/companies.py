import csv

def scrub_company(c):
    # redditors often abbreviate company names
    postfixes = ["inc", "inc.","plc", "ltd.", "corp", "corp.","corporation","Incorporated", "class a", "class b","company", "& co","& co.","co","co."]
    resultwords  = [word for word in c.split() if word.lower() not in postfixes]
    return ' '.join(resultwords)

with open("src/referencedata/SPY500.csv") as f:
    reader = csv.reader(f)
    companies = [(row[0],scrub_company(row[1])) for row in reader][1:]
