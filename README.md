# Indexed_Heap #
It is Python package of an indexed binary heap, that designed to solve the inefficiencies of Python ```heapq``` package.  

## Motivation ##
In many of the heap-based algorithms, like Prim's Algorithm to find Minimum Spanning Tree (MST), or Dijkstra Algorithm to find shortest path in a positively weighted graph, we need the ability to modify the value of elements within a heap, while maintaining the heap order in O(logN) time complexity.  
In Python's most popular heap package, ```heapq```, such operations are not allowed. So we cannot implement heap-based algorithms that require value changes efficiently using ```heapq```.   
Here I develop my own solution using an Indexed Heap idea. I use additional dictionaries to index elements inside a heap, and grarantee a O(logN) time complexity when modifying elements inside a heap.  

## Major Scripts ##
Please check Indexed_Heap/Indexed_Heap.py file. It contains doumented Python code and unit tests.  
