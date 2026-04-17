import sys
import csv

# Read input line by line 
for line in sys.stdin:
    # Remove leading/trailing whitespace
    line = line.strip()

    # Skip empty lines
    if not line:
        continue
    # Skip header row (column names)
    if line.startswith('"STATION"'):
        continue

    # Parse CSV line safely 
    # used to handles quoted commas properly
    fields = next(csv.reader([line]))

    # Ensure the row has enough columns before accessing indices
    if len(fields) < 8:
        continue

    # Extract relevant fields
    # station ID in first column
    station = fields[0]
    # Date in 2nd column
    date = fields[1]
    # Temp value as string in 7 column
    tempstr = fields[6]
    # extrcats year from the date YYYYMMDD
    year = date[:4]

    # Skip missing or invalid temperature values
    if tempstr == "" or tempstr == "9999.9":
        continue
    
     # Convert temperature to float
    temp = float(tempstr)

    # Output key-value pair:
    print(f"{station},{year}\t{temp},{1}")
  
