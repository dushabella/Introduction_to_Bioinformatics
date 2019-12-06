my_file = open('data_ex5.txt')

new_data = []

for i, line in enumerate(my_file):
    if (i+1)%2 == 0:
        print("parzyste")
        print(line)
        new_data.append(line)

print(new_data)
my_file.close()
