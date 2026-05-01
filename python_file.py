def hacker_rank_task1():
    datas=[]

    rows=int(input())

    for _ in range(rows):
        name=input().split()
        grade=float(input().split())
        datas.append([name,grade])

    grades=[]

    for item in datas:
        grades.append(item[1])


    unique_grade=sorted(set(grades))

    second_lowest=unique_grade[1]

    names=[]

    for item in datas:
        if item[1]==second_lowest:
            names.append(item[0])

    names.sort()

    for name in names:
        print(name)



#Task 2 

def hack_rank_task2():
    student={}
    row=int(input())
    for _ in range(row):
        data=input().split()
        name=data[0]
        mark=list(map(float,data[1:]))
        student[name]=mark
    query_name=input()
    average=sum(student[query_name])/(len(student[query_name]))
    return f'{average:.2f}'


def hack_rank_task3():
    n = int(input())

    list1 = []

    for _ in range(n):
        data = input().split()
        command = data[0]

        try:
            if command == "append":
                list1.append(int(data[1]))

            elif command == "print":
                print(list1)

            elif command == "insert":
                list1.insert(int(data[1]), int(data[2]))

            elif command == "remove":
                list1.remove(int(data[1]))

            elif command == "sort":
                list1.sort()

            elif command == "pop":
                list1.pop()

            elif command == "reverse":
                list1.reverse()

            else:
                print("wrong command")

        except Exception as e:
            print("operation failed:", e)



def hack_rank_task4():
    n=int(input())
    number=input().split()
    num=tuple(map(int,number))
    print(hash(num))
hack_rank_task4()



    
