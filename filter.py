import sys

wordset = set()
for line in open(sys.argv[1]):
    line = line.strip().lower()[:-1]
    if "," in line:
        for word in line.split(","):
            wordset.add(word)
    else:
        wordset.add(line)

count =0
for line in open(sys.argv[2]):
    path = line.strip()
    count+=1
    if count%10000==0:
        sys.stderr.write(str(count)+"\n")
    content = open(path).read().strip().lower()
    for word in wordset:
        if word in content:
            print path
            break



