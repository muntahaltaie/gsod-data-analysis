import sys

current_key = None
temp_sum = 0.0
count = 0

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    
    pair = line.split("\t")
    if len(pair) != 2:
        continue

    key, value = pair
    temp, num = value.split(",")
   
    temp = float(temp)
    num = int(num)
   
    if current_key is None:
        current_key = key
        temp_sum = temp
        count = num

    elif key == current_key:
        temp_sum += temp
        count += num

    else:
        station, year = current_key.split(",")
        avg = temp_sum / count
        print(f"{station}, {year}, {avg:.2f}")

        current_key = key
        temp_sum = temp
        count = num 

if current_key is not None:
    station, year = current_key.split(",")
    avg = temp_sum / count
    print(f"{station}, {year}, {avg:.2f}")

