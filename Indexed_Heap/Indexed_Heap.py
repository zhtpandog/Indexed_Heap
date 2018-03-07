# author: Haotian Zhang, zhtpandog@gmail.com
# binary indexed heap
# it is by default a min heap
# can specify comparator by specifying __lt__ function in objects to be put in heap
# support operations: put, peek, del_root, del_by_id, change_value, heapify

class Indexed_Heap(object):

    def __init__(self, list_of_obj):
        """
        Initialize an indexed heap with id and value pairs.
        :param list_of_obj: A list of objects. Each obj must have a field "id" (e.g. vertex id in a graph) and a field "val" (e.g. distance from this vertex to origin vertex).
        """

        # initialize a random array
        self.num_items_in_heap = len(list_of_obj)
        self.heap = [None]
        self.obj_idx_map = {} # dict, key is id of object and val is position idx in heap array
        self.idx = 1
        for obj in list_of_obj:
            self.heap.append(obj)
            self.obj_idx_map[obj.id] = self.idx
            self.idx += 1


    def __cmp_lt(self, x, y):
        return (x < y) if hasattr(x, "__lt__") else (not y <= x)


    def __exch(self, idx1, idx2):
        # update obj_idx_map
        self.obj_idx_map[self.heap[idx1].id], self.obj_idx_map[self.heap[idx2].id] = \
            self.obj_idx_map[self.heap[idx2].id], self.obj_idx_map[self.heap[idx1].id]

        # do the exchange
        self.heap[idx1], self.heap[idx2] = self.heap[idx2], self.heap[idx1]


    def __siftdown(self, heap_idx):
        """
        Sift down an element in heap to maintain heap order, and maintain proper idx_map.
        For an item in heap_idx to be sifted down, it is supposed to be larger than at least one of its children
        :param heap_idx: the index of the element in heap to be sifted down
        :return:
        """

        # step = 0
        while True:
            # if the left child exists and val of left child is smaller than current
            if heap_idx * 2 < len(self.heap) and self.__cmp_lt(self.heap[heap_idx * 2].val, self.heap[heap_idx].val):
                left_child_idx = heap_idx * 2
            else:
                left_child_idx = None

            # if the right child exists and val of right child is smaller than current
            if heap_idx * 2 + 1 < len(self.heap) and self.__cmp_lt(self.heap[heap_idx * 2 + 1].val, self.heap[heap_idx].val):
                right_child_idx = heap_idx * 2 + 1
            else:
                right_child_idx = None

            # print "right: " + str(right_child_idx) + " , left: " + str(left_child_idx)
            # if not having either left child or right child, break from iteration
            if not left_child_idx and not right_child_idx:
                return

            # print "step " + str(step) + ": right: " + str(right_child_idx) + " , left: " + str(left_child_idx)

            if right_child_idx and not left_child_idx:
                self.__exch(right_child_idx, heap_idx)
                heap_idx = right_child_idx
            elif left_child_idx and not right_child_idx:
                self.__exch(left_child_idx, heap_idx)
                heap_idx = left_child_idx
            elif self.__cmp_lt(self.heap[right_child_idx], self.heap[left_child_idx]): # right is smaller
                self.__exch(right_child_idx, heap_idx)
                heap_idx = right_child_idx
            else: # left is smaller
                self.__exch(left_child_idx, heap_idx)
                heap_idx = left_child_idx

            # print [None] + [i.val for i in self.heap if i]
            # print self.obj_idx_map
            # step += 1


    def __siftup(self, heap_idx):
        """
        Sift up an element in heap to maintain heap order, and maintain proper idx_map.
        For an item in heap_idx to be sifted up, it is supposed to be smaller than its parent
        :param heap_idx: the index of the element in heap to be sifted up
        :return:
        """
        while True:
            if heap_idx <= 1:
                return
            if self.__cmp_lt(self.heap[heap_idx], self.heap[heap_idx // 2]): # if the item is smaller than its parent, exchange
                self.__exch(heap_idx // 2, heap_idx)
                heap_idx = heap_idx // 2
            else:
                return


    def __get_heap_array(self):
        return [None] + [i.val for i in self.heap if i]


    def __get_map(self):
        return self.obj_idx_map


    def heapify(self):
        """
        Heapify an heap.
        :return:
        """

        curr = self.num_items_in_heap // 2
        # step = 0
        while True:
            # see if curr is needed to be sifted down
            self.__siftdown(curr)
            curr -= 1
            if not curr:
                return


    def change_value(self, new_obj):
        """
        Change a node's value (maintain same id) and restore the heap order and obj_idx_map.
        :param heap_idx: the index of the element in heap to be changed.
        :return:
        """
        id_new = new_obj.id
        heap_idx = self.obj_idx_map[id_new]
        self.heap[heap_idx] = new_obj

        # smaller than parent, sift up
        if heap_idx > 1 and self.__cmp_lt(self.heap[heap_idx], self.heap[heap_idx // 2]):
            self.__siftup(heap_idx)
        else:  # larger than children
            self.__siftdown(heap_idx)


    def put(self, new_obj):
        """
        Put a new object into heap and maintain heap order.
        :param new_obj: A new object with same type as other objects in heap
        :return:
        """
        self.heap.append(new_obj)
        self.num_items_in_heap += 1
        pos = len(self.heap) - 1
        self.obj_idx_map[new_obj.id] = pos
        self.__siftup(pos)


    def del_by_id(self, id_del):
        """
        Remove an object in heap based on id and maintain heap order.
        :param id_del: id of object to delete
        :return:
        """
        # exchange the node with the one in the end
        pos_del = self.obj_idx_map[id_del]
        self.__exch(pos_del, len(self.heap) - 1)

        # delete the last element
        self.heap.pop()
        del self.obj_idx_map[id_del]

        # restore heap order
        self.heapify()
        # self.__siftdown(pos_del)


    def del_root(self):
        """
        Delete the element in the root, it can be either the largest or the smallest element in heap.
        :return: The deleted object
        """

        # exchange the root with the one in the end
        self.__exch(1, len(self.heap) - 1)

        # delete and get the last element
        result = self.heap.pop()
        del self.obj_idx_map[result.id]

        # restore heap order by sifting down the root
        self.__siftdown(1)

        return result


    def peek(self):
        """
        Get the object at the root but not delete it.
        :return: object at the root
        """
        return self.heap[1]





# unit tests
class test_obj(object):
    def __init__(self, id, val):
        self.id = id
        self.val = val

    def __lt__(self, other):
        return self.val < other.val

if __name__ == "__main__":
    pass

    # no need to do this again
    # import random
    # # generate a random test array of test_obj
    # test_arr = []
    # count = 1
    # input_dict = {}
    # for i in range(7):
    #     rand_num = random.randint(0,100)
    #     test_arr.append(test_obj(count, rand_num))
    #     input_dict[count] = rand_num
    #     count += 1
    ## no need to do this again

    # test_arr = []
    # input_dict = {'a': 55, 'b': 65, 'c': 20, 'd': 90, 'e': 42, 'f': 72, 'g': 3}
    # for k,v in input_dict.items():
    #     test_arr.append(test_obj(k, v))
    #
    # print "original input k-v pairs are: "
    # print input_dict
    # hp = Indexed_Heap(test_arr)
    # print "initial heap array is: "
    # print hp.__get_heap_array()
    # print "initial obj_idx_map is: "
    # print hp.__get_map()

    # # unit test __exch(), pass
    # print " "
    # print "after __exch: "
    # hp.__exch(1,2)
    # print hp.__get_heap_array()
    # print hp.__get_map()

    # # unit test _sift_down(), pass
    # hp.__siftdown(3)
    # print " "
    # print "heap array after sift down and new map: "
    # print hp.__get_heap_array()
    # print hp.__get_map()

    # # unit test __siftup(), pass
    # hp.__siftup(6)
    # print " "
    # print "heap array after sift up and new map: "
    # print hp.__get_heap_array()
    # print hp.__get_map()

    # # unit test heapify(), pass
    # hp.heapify()
    # print "heap array after heapify: "
    # print hp.__get_heap_array()
    # print hp.__get_map()

    # # unit test change_value(), pass
    # hp.heapify()
    # print "heap array after heapify: "
    # print hp.__get_heap_array()
    # print hp.__get_map()
    # hp.change_value(test_obj("b", 21))
    # print "heap array after change: "
    # print hp.__get_heap_array()
    # print hp.__get_map()
    # # hp.change_value(test_obj("g", 70))
    # # print "heap array after change: "
    # # print hp.__get_heap_array()
    # # print hp.__get_map()

    # # unit test put(), pass
    # hp.heapify()
    # print "heap array after heapify: "
    # print hp.__get_heap_array()
    # print hp.__get_map()
    # hp.put(test_obj("m", 15))
    # print "heap array after put: "
    # print hp.__get_heap_array()
    # print hp.__get_map()

    # # unit test del_by_id(), pass
    # hp.heapify()
    # print "heap array after heapify: "
    # print hp.__get_heap_array()
    # print hp.__get_map()
    # hp.del_by_id("g")
    # print "heap array after del by id: "
    # print hp.__get_heap_array()
    # print hp.__get_map()

    # # unit test del_root(), pass
    # hp.heapify()
    # print "heap array after heapify: "
    # print hp.__get_heap_array()
    # print hp.__get_map()
    # item = hp.del_root()
    # print "heap array after del root: "
    # print hp.__get_heap_array()
    # print hp.__get_map()
    # print " "
    # print item.id
    # print item.val

    # # unit test peek(), pass
    # hp.heapify()
    # print "heap array after heapify: "
    # print hp.__get_heap_array()
    # print hp.__get_map()
    # item = hp.peek()
    # print "heap array after peek: "
    # print hp.__get_heap_array()
    # print hp.__get_map()
    # print " "
    # print item.id
    # print item.val


