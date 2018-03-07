# Indexed_Heap #
It is Python package of an indexed binary heap, that designed to solve the inefficiencies of Python ```heapq``` package.  

## Motivation ##
In many of the heap-based algorithms, like Prim's Algorithm to find Minimum Spanning Tree (MST), or Dijkstra Algorithm to find shortest path in a positively weighted graph, we need the ability to modify the value of elements within a heap, while maintaining the heap order in O(logN) time complexity.  
In Python's most popular heap package, ```heapq```, such operations are not allowed. So we cannot implement heap-based algorithms that require value changes efficiently using ```heapq```.   
Here I develop my own solution using an Indexed Heap idea. I use additional dictionaries to index elements inside a heap, and grarantee a O(logN) time complexity when modifying elements inside a heap.  

## Major Scripts ##
Please check Indexed_Heap/Indexed_Heap.py file. It contains doumented Python code and unit tests.  

## Demo ##
Prepare the input. Suppose we have a test_obj class that serves as the elements inside the indexed heap. We create test_obj lists as input array:  
```
class test_obj(object):
    def __init__(self, id, val):
        self.id = id
        self.val = val

    def __lt__(self, other):
        return self.val < other.val
test_arr = []
input_dict = {'a': 55, 'b': 65, 'c': 20, 'd': 90, 'e': 42, 'f': 72, 'g': 3}
for k,v in input_dict.items():
    test_arr.append(test_obj(k, v))
```
Intialize the indexed heap and heapify it:  
```
hp = Indexed_Heap(test_arr)
hp.heapify()
```
The current smallest element has value 3:  
```
print(hp.peek().val) # output 3
```
After we change the element, the smallest element is the one with value 20:  
```
hp.change_value(test_obj('g', 50))
print(hp.peek().val # output 20
```