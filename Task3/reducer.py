import sys

# Initialize variables
current_key = None
temp_sum = 0.0
count = 0

# Read sorted key-value pairs
for line in sys.stdin:
    # Remove whitespace
    line = line.strip()

    # Skip empty lines
    if not line:
        continue

    # Split into key and value using tab delimiter
    pair = line.split("\t")
    # skip possible improper lines
    if len(pair) != 2:
        continue

    key, value = pair
    # Extract temperature and count from value
    temp, num = value.split(",")
   
   # convert temp to float and count to int
    temp = float(temp)
    num = int(num)
   
    # First key initialization
    if current_key is None:
        current_key = key
        temp_sum = temp
        count = num

    # If same key, accumulate values
    elif key == current_key:
        temp_sum += temp
        count += num

    # If new key, output result for previous key
    else:
        station, year = current_key.split(",")
        # Compute average temperature
        avg = temp_sum / count
        # Output: station, year, average temperature
        print(f"{station}, {year}, {avg:.2f}")

        # Reset for new key
        current_key = key
        temp_sum = temp
        count = num 

# Output the last key after loop ends
if current_key is not None:
    station, year = current_key.split(",")
    avg = temp_sum / count
    print(f"{station}, {year}, {avg:.2f}")

