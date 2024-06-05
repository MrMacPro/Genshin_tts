def read_lib():
    d = dict()

    with open("lib.txt", "r", encoding='utf-8') as file:
        for line in file:
            line = line.split()
            if line[1] in ("男", "女"):
                d[line[0]] = line[1]
    return d

if __name__ == "__main__":
    print(read_lib())