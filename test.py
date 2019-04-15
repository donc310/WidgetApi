data = [{'sum':1000},{'sum':1000},{'sum':1000},{'sum':1000},{'sum':1000}]
total = 0
index = 0 
while index < len(data):
    total += (data[index]['sum'])
    index += 1

print(total)