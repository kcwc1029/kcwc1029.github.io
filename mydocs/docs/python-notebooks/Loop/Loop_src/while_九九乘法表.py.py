i = 1
while i <= 9:
    j = 1
    while j <= 9:
        result = i * j
        print(f"{i}*{j}={result}", end='\t')
        j += 1
    print()
    i += 1