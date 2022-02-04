answer = ""
with open("./answer.txt", "r") as txt:
    for line in txt:
        answer += chr(int(line))
print(answer)