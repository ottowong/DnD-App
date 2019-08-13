def sort(items):
    for i in range(len(items)):
        for j in range(len(items)-1-i):
            if items[j][1] > items[j+1][1]:
                items[j][1], items[j+1][1] = items[j+1][1], items[j][1]
    return items
    
if __name__ == "__main__":
    print(sort([["otto",10],["jim",15],["john",8],["jeff",11]]))
