

template = open("template.html", "r")
t = 0


for line in template:
    t += 1
    #print(t)
    print(type(line))
    print(line)
    print(len(line))
    if line == "++++++++++\n":
        print("This is where we enter the code")
        break
    #else:
    #    print(line)

print("Replace the code line with whatever is here")
for line in template:
    print(line)

template.close()
