from datetime import datetime
import random
import threading

arrayA = []
threads = []
threadsMaxElem = []


def add_element(element_count):
    count = 0
    while count < element_count:
        arrayA.append(random.randint(0, 100000))
        count += 1


def start_threads():
    count = 0
    while count < threadNumber:
        threads[count].start()
        count += 1


def join_threads():
    count = 0
    while count < threadNumber:
        threads[count].join()
        count += 1


def create_sort_element_threads(element_sum, number_of_thread):
    count = 0
    element_per_thread = int(element_sum / number_of_thread)
    while count < number_of_thread:
        threads.append(threading.Thread(target=find_max_thread, args=(element_per_thread, count,)))
        count += 1


def find_max_thread(element_count, thread_count):
    count = 0
    if thread_count <= 0:
        index = 0
    else:
        index = thread_count * element_count

    sub_array = []
    while count < element_count:
        sub_array.append(arrayA[index])
        index += 1
        count += 1

    print(f"sub_array {thread_count}: {len(sub_array)} elements")
    sub_array.sort(reverse=True)
    print(f"Max element of sub_array {thread_count}: {sub_array[0]}")
    threadsMaxElem.append(sub_array[0])
    print(f"Thread {thread_count} finished at {datetime.now()}\n")


# <editor-fold desc="Input from keyboard">
print('Enter number of elements for global array:')
arrayCount = int(input('arrayCount = '))

print('Enter number of threads:')
threadNumber = int(input('threadNumber = '))
print('\n')
# </editor-fold>

# <editor-fold desc="Create and start adding elements to arrayA">
add_element(arrayCount)
print(f'arrayA: {arrayA}')
# </editor-fold>

# <editor-fold desc="Create and start find max of arrayA by finding max of smaller arrayA's array">
create_sort_element_threads(arrayCount, threadNumber)
start_threads()
join_threads()
# </editor-fold>

# <editor-fold desc="Handle finding max in leftover elements of arrayA if thread division has remainder">
if len(arrayA) < arrayCount:
    mainIndex = len(arrayA)
    mainCount = 0
    tempMaxArray = []
    while mainCount < (len(arrayA) - arrayCount):
        tempMaxArray.append(arrayA[mainIndex])
        mainCount += 1
        mainIndex += 1
    tempMaxArray.sort(reverse=True)
    threadsMaxElem.append(tempMaxArray[0])
# </editor-fold>

# <editor-fold desc="Print largest element of arrayA">
threadsMaxElem.sort(reverse=True)
print(f"Largest element in the array is: {threadsMaxElem[0]}")
# </editor-fold>

# <editor-fold desc="Double-check the result">
arrayA.sort(reverse=True)

if threadsMaxElem[0] == arrayA[0]:
    print("Result is correct")
else:
    print("Incorrect result")
# </editor-fold>
