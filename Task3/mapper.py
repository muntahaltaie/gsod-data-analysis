import sys
import csv

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    if line.startswith('"STATION"'):
        continue

    fields = next(csv.reader([line]))

    if len(fields) < 8:
        continue

    station = fields[0]
    date = fields[1]
    tempstr = fields[6]
    year = date[:4]



    if tempstr == "" or tempstr == "9999.9":
        continue
    
    temp = float(tempstr)

    print(f"{station},{year}\t{temp},{1}")
  
