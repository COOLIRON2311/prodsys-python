a = {}
doubles = []
with open('facts.txt', 'r') as f:
    for line in f:
        if line and line[0] != '\n':
            # print(line.split(';'))
            ident = line.split(';')[1]
            if ident not in a:
                a[ident] = 1
            else:
                a[ident] += 1
                doubles.append(ident)
print(doubles)

# https://www.minecraft-crafting.net

