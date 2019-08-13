def sort(items):
    for i in range(len(items)):
        for j in range(len(items)-1-i):
            if items[j][2] < items[j+1][2]:
                items[j], items[j+1] = items[j+1], items[j]
    return items

if __name__ == "__main__":
    print(sort([[1,"otto",10],[2,"jim",15],[3,"john",8],[4,"jeff",11]]))
