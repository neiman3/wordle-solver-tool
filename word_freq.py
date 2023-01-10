def oxford_list(file="oxford3k.txt"):
    f = open(file, "r")
    res = []
    for line in f:
        words = line.split()
        if words == []:
            continue
        elif len(words[0]) == 5:
            if words[0] not in res:
                res.append(words[0])

    f.close()
    return res