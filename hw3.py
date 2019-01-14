# First of all we import random to generate random lists of numbers,
# time to time the performance of our functions, heapq for the heap data structure
# and pyplot to plot our data and csv to write a table containing the data.
import random
import time
import heapq
import csv
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(1500)

# define our function that implements QuickSort algorithm
def quicksort(array):
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            if x == pivot:
                equal.append(x)
            if x > pivot:
                greater.append(x)
        return quicksort(less) + equal + quicksort(greater)

    else:
        return array

# define our function that implements BubbleSort algorithm
def bubble_sort(arr):
    for passnum in range(len(arr) - 1, 0, -1):
        for i in range(passnum):
            if arr[i] > arr[i + 1]:
                temp = arr[i]
                arr[i] = arr[i + 1]
                arr[i + 1] = temp


# define TreeNode class, necessary for our BST
class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

    def findMin(self):
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def findMax(self):
        current = self
        while current.hasRightChild():
            current = current.rightChild
        return current

    def findSuccessor(self):
        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            if self.parent:
                if self.isLeftChild():
                    succ = self.parent
                else:
                    self.parent.rightChild = None
                    succ = self.parent.findSuccessor()
                    self.parent.rightChild = self
        return succ

    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
                self.leftChild.parent = self.parent
            else:
                if self.isLeftChild():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent

# define BST data structure class
class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1

    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)
        elif key > currentNode.key:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)
        else:
            currentNode.payload = val

    def __setitem__(self, k, v):
        self.put(k, v)

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    def getNode(self, key):
        if self.root:
            res = self._getNode(key, self.root)
            if res:
                return res
            else:
                return None
        else:
            return None

    def _getNode(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._getNode(key, currentNode.leftChild)
        else:
            return self._getNode(key, currentNode.rightChild)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        if self._get(key, self.root):
            return True
        else:
            return False

    def delete(self, key):
        if self.size > 1:
            nodeToRemove = self._get(key, self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size = self.size - 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error, key not in tree')

    def __delitem__(self, key):
        self.delete(key)


    def findMin(self):
        current = self.root
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def findMax(self):
        current = self.root
        while current.hasRightChild():
            current = current.rightChild
        return current

    def remove(self, currentNode):
        if currentNode.isLeaf():  # leaf
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren():  # interior
            succ = currentNode.findSuccessor()
            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.payload = succ.payload

        else:  # this node has one child
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:
                    currentNode.replaceNodeData(currentNode.leftChild.key,
                                                currentNode.leftChild.payload,
                                                currentNode.leftChild.leftChild,
                                                currentNode.leftChild.rightChild)
            else:
                if currentNode.isLeftChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.key,
                                                currentNode.rightChild.payload,
                                                currentNode.rightChild.leftChild,
                                                currentNode.rightChild.rightChild)

# define class for QuickSort algorithm to find minimum and maximum of a list with methods add, get_min, get_max
class MinMaxQuick(object):

    def __init__(self):
        self.content = []

    def add(self, value):
        self.content.append(value)
        quicksort(self.content)

    def get_min(self):
        return self.content[0]

    def get_max(self):
        return self.content[-1]

# define class for BST data structure to find minimum and maximum of a list with methods add, get_min, get_max
class MinMaxBinary(object):

    def __init__(self):
        self.content = BinarySearchTree()
        self.size = 0

    def add(self, value):
        self.content.put(value, value)

    def get_min(self):
        return self.content.findMin()

    def get_max(self):
        return self.content.findMax()

# define class for Heap data structure to find minimum and maximum of a list with methods add, get_min, get_max
class MinMaxHeap(object):

    def __init__(self):
        self.content_min = []
        self.content_max = []

    def add(self, value):
        heapq.heappush(self.content_min, value)
        heapq.heappush(self.content_max, -value)

    def get_min(self):
        if len(self.content_min) > 0:
            return self.content_min[0]

    def get_max(self):
        if len(self.content_max) > 0:
            return -self.content_max[0]

# define class for BubbleSort algorithm to find minimum and maximum of a list with methods add, get_min, get_max
class MinMaxBubble(object):

    def __init__(self):
        self.content = []

    def add(self, value):
        self.content.append(value)
        bubble_sort(self.content)

    def get_min(self):
        return self.content[0]

    def get_max(self):
        return self.content[-1]

# define a function to time our class's add, get_min, get_max methods and return the three execution times.
# clss = the class to be used, num_list = list the function will get numbers from to add to our class object
def measure_time(clss, num_list):
    tot_time_add = 0
    tot_time_min = 0
    tot_time_max = 0

    for num in num_list:
        start = time.time()
        clss.add(num)
        tot_time_add += (time.time() - start)

        start = time.time()
        min = clss.get_min()
        tot_time_min += (time.time() - start)

        start = time.time()
        max = clss.get_max()
        tot_time_max += (time.time() - start)

    return tot_time_add, tot_time_min, tot_time_max

# max_operations = max size of number list we will use
# step = increments of number list size
# repetitions = n of times we execute the time measurement for a give list size for accuracy
# slow= will allow to remove BubbleSort and QuickSort from the benchmark in case you want to go over ~1000 with max_operations
def benchmark(max_operations, step=100, repetitions=20, slow=True):

    length = []

    values_quick_add, values_quick_min, values_quick_max = [], [], []
    values_binary_add, values_binary_min, values_binary_max = [], [], []
    values_heap_add, values_heap_min, values_heap_max = [], [], []
    values_bubble_add, values_bubble_min, values_bubble_max = [], [], []

    for rounds in range(step, max_operations, step):
        length.append(rounds)
        this_list = []
        for r in range(rounds):
            this_list.append(random.randint(0, 1000))

        tot_time_add, tot_time_min, tot_time_max = 0, 0, 0
        if slow:
            for repetition in range(repetitions):
                a = MinMaxQuick()
                myadd, mymin, mymax = measure_time(a, this_list)
                tot_time_add += myadd
                tot_time_min += mymin
                tot_time_max += mymax

            tot_time_add /= repetitions
            tot_time_min /= repetitions
            tot_time_max /= repetitions

            values_quick_add.append(tot_time_add * 1000)
            values_quick_min.append(tot_time_min * 1000)
            values_quick_max.append(tot_time_max * 1000)

            tot_time_add, tot_time_min, tot_time_max = 0, 0, 0
        for repetition in range(repetitions):
            a = MinMaxBinary()
            myadd, mymin, mymax = measure_time(a, this_list)
            tot_time_add += myadd
            tot_time_min += mymin
            tot_time_max += mymax

        tot_time_add /= repetitions
        tot_time_min /= repetitions
        tot_time_max /= repetitions

        values_binary_add.append(tot_time_add * 1000)
        values_binary_min.append(tot_time_min * 1000)
        values_binary_max.append(tot_time_max * 1000)

        tot_time_add, tot_time_min, tot_time_max = 0, 0, 0

        for repetition in range(repetitions):
            a = MinMaxHeap()
            myadd, mymin, mymax = measure_time(a, this_list)
            tot_time_add += myadd
            tot_time_min += mymin
            tot_time_max += mymax

        tot_time_add /= repetitions
        tot_time_min /= repetitions
        tot_time_max /= repetitions

        values_heap_add.append(tot_time_add * 1000)
        values_heap_min.append(tot_time_min * 1000)
        values_heap_max.append(tot_time_max * 1000)

        tot_time_add, tot_time_min, tot_time_max = 0, 0, 0
        if slow:
            for repetition in range(repetitions):
                a = MinMaxBubble()
                myadd, mymin, mymax = measure_time(a, this_list)
                tot_time_add += myadd
                tot_time_min += mymin
                tot_time_max += mymax

            tot_time_add /= repetitions
            tot_time_min /= repetitions
            tot_time_max /= repetitions

            values_bubble_add.append(tot_time_add * 1000)
            values_bubble_min.append(tot_time_min * 1000)
            values_bubble_max.append(tot_time_max * 1000)

# write to cvs file
    if slow:
        header = ['List length', 'BST add', 'BST get_min', 'BST get_max', 'Heap add', 'Heap get_min', 'Heap get_max', 'Quick add', 'Quick get_min', 'Quick get_max', 'Bubble add', 'Bubble get_min', 'Bubble get_max']
        with open('data_table.csv', 'w') as w:
            writer = csv.writer(w, lineterminator='\n')
            writer.writerow(header)
            for i in range(len(values_binary_add)):
                row = [length[i], round(values_binary_add[i], 5), round(values_binary_min[i], 5), round(values_binary_max[i], 5), round(values_heap_add[i], 5), round(values_heap_min[i], 5), round(values_heap_max[i], 5), round(values_quick_add[i], 5), round(values_quick_min[i], 5), round(values_quick_max[i], 5), round(values_bubble_add[i], 5), round(values_bubble_min[i], 5), round(values_bubble_max[i], 5)]
                writer.writerow(row)
                print(row)
    else:
        header = ['List length', 'BST add', 'BST get_min', 'BST get_max', 'Heap add', 'Heap get_min', 'Heap get_max']
        with open('data_table.csv', 'w') as w:
            writer = csv.writer(w, lineterminator='\n')
            writer.writerow(header)
            for i in range(len(values_binary_add)):
                row = [length[i], round(values_binary_add[i], 5), round(values_binary_min[i], 5), round(values_binary_max[i], 5), round(values_heap_add[i], 5), round(values_heap_min[i], 5), round(values_heap_max[i], 5)]
                writer.writerow(row)
                print(row)

    xlabels = range(step, max_operations, step)


# plot BST
    plt.plot(xlabels, values_binary_add, color='g', linestyle='-', label='Add')
    plt.plot(xlabels, values_binary_min, color='g', linestyle='--', label='Get Min')
    plt.plot(xlabels, values_binary_max, color='g', linestyle='-.', label='Get Max')
    plt.gca().yaxis.grid(True)
    plt.legend()
    plt.xlabel("Number of Operations")
    plt.ylabel(r"Execution time ($\mu$sec)")
    plt.title("Performance of BinarySearchTree ")
    plt.savefig('BST')
    plt.show()


# plot Quick
    if slow:
        plt.plot(xlabels, values_quick_add, color='r', linestyle='-',  label='Add')
        plt.plot(xlabels, values_quick_min, color='r', linestyle='--', label='Get Min')
        plt.plot(xlabels, values_quick_max, color='r', linestyle='-.', label='Get Max')
        plt.gca().yaxis.grid(True)
        plt.legend()
        plt.xlabel("Number of Operations")
        plt.ylabel(r"Execution time ($\mu$sec)")
        plt.title("Performance of QuickSort algorithm")
        plt.savefig('Quick')
        plt.show()

# plot Heap
    plt.plot(xlabels, values_heap_add, color='b', linestyle='-', label='Add')
    plt.plot(xlabels, values_heap_min, color='b', linestyle='--', label='Get Min')
    plt.plot(xlabels, values_heap_max, color='b', linestyle='-.', label='Get Max')
    plt.gca().yaxis.grid(True)
    plt.legend()
    plt.xlabel("Number of Operations")
    plt.ylabel(r"Execution time (($\mu$sec)")
    plt.title("Performance of Heap")
    plt.savefig('Heap')
    plt.show()

# plot Bubble
    if slow:
        plt.plot(xlabels, values_bubble_add, color='y', linestyle='-', label='Add')
        plt.plot(xlabels, values_bubble_min, color='y', linestyle='--', label='Get Min')
        plt.plot(xlabels, values_bubble_max, color='y', linestyle='-.', label='Get Max')
        plt.gca().yaxis.grid(True)
        plt.legend()
        plt.xlabel("Number of Operations")
        plt.ylabel(r"Execution time ($\mu$sec)")
        plt.title("Performance of BubbleSort algorithm")
        plt.savefig('Bubble')
        plt.show()

# plot all Add
    plt.plot(xlabels, values_binary_add, color='g', linestyle='-', label='BST Add')
    plt.plot(xlabels, values_heap_add, color='b', linestyle='-', label='Heap Add')
    if slow:
        plt.plot(xlabels, values_bubble_add, color='y', linestyle='-', label='Bubble Add')
        plt.plot(xlabels, values_quick_add, color='r', linestyle='-', label='Quick Add')
    plt.gca().yaxis.grid(True)
    plt.legend()
    plt.xlabel("Number of Operations")
    plt.ylabel(r"Execution time ($\mu$sec)")
    plt.title("Performance of Add")
    plt.savefig('allAdd')
    plt.show()

# plot all Add in log scale
    plt.plot(xlabels, values_binary_add, color='g', linestyle='-', label='BST Add')
    plt.plot(xlabels, values_heap_add, color='b', linestyle='-', label='Heap Add')
    if slow:
        plt.plot(xlabels, values_bubble_add, color='y', linestyle='-', label='Bubble Add')
        plt.plot(xlabels, values_quick_add, color='r', linestyle='-', label='Quick Add')
    plt.gca().yaxis.grid(True)
    plt.legend()
    plt.xlabel("Number of Operations")
    plt.ylabel(r"Execution time ($\mu$sec)")
    plt.title("Performance of Add")
    plt.savefig('allAdd')
    plt.show()

# plot all Min and Max
    plt.subplot(211)
    plt.plot(xlabels, values_binary_min, color='g', linestyle='-', label='BST Get Min')
    plt.plot(xlabels, values_heap_min, color='b', linestyle='-', label='Heap Get Min')
    if slow:
        plt.plot(xlabels, values_bubble_min, color='y', linestyle='-', label='Bubble Get Min')
        plt.plot(xlabels, values_quick_min, color='r', linestyle='-', label='Quick Get Min')
    cur_axes = plt.gca()
    cur_axes.axes.get_xaxis().set_ticks([])
    cur_axes.yaxis.grid(True)
    plt.legend()

    plt.ylabel(r"Execution time ($\mu$sec)")
    plt.title("Performance of Get Min")

    plt.subplot(212)
    plt.plot(xlabels, values_binary_max, color='g', linestyle='-', label='BST Get Max')
    plt.plot(xlabels, values_heap_max, color='b', linestyle='-', label='Heap Get Max')
    if slow:
        plt.plot(xlabels, values_bubble_max, color='y', linestyle='-', label='Bubble Get Max')
        plt.plot(xlabels, values_quick_max, color='r', linestyle='-', label='Quick Get Max')
    plt.gca().yaxis.grid(True)
    plt.legend()
    plt.xlabel("Number of Operations")
    plt.ylabel(r"Execution time (($\mu$sec)")
    plt.title("Performance of Get Max")

    plt.savefig('allMinMax')
    plt.show()

# plot All in log
    plt.plot(xlabels, values_binary_add, color='g', linestyle='-', label='BST Add')
    plt.plot(xlabels, values_binary_min, color='g', linestyle='--', label='BST Get Min')
    plt.plot(xlabels, values_binary_max, color='g', linestyle='-.', label='BST Get Max')

    plt.plot(xlabels, values_heap_add, color='b', linestyle='-', label='Heap Add')
    plt.plot(xlabels, values_heap_min, color='b', linestyle='--', label='Heap Get Min')
    plt.plot(xlabels, values_heap_max, color='b', linestyle='-.', label='Heap Get Max')

    if slow:
        plt.plot(xlabels, values_bubble_add, color='y', linestyle='-', label='Bubble Add')
        plt.plot(xlabels, values_bubble_min, color='y', linestyle='--', label='Bubble Get Min')
        plt.plot(xlabels, values_bubble_max, color='y', linestyle='-.', label='Bubble Get Max')

        plt.plot(xlabels, values_quick_add, color='r', linestyle='-', label='Quick Add')
        plt.plot(xlabels, values_quick_min, color='r', linestyle='--', label='Quick Get Min')
        plt.plot(xlabels, values_quick_max, color='r', linestyle='-.', label='Quick Get Max')

    plt.xscale('log')

    plt.gca().yaxis.grid(True)
    plt.legend()
    plt.xlabel("Number of Operations")
    plt.ylabel(r"Execution time ($\mu$sec)")
    if slow:
        plt.title("Performance of BST, Bubble, Heap, Quick ")
    else:
        plt.title("Performance of BST, Heap")
    plt.savefig('Alllog')
    plt.show()

# plot All
    plt.plot(xlabels, values_binary_add, color='g', linestyle='-', label='BST Add')
    plt.plot(xlabels, values_binary_min, color='g', linestyle='--', label='BST Get Min')
    plt.plot(xlabels, values_binary_max, color='g', linestyle='-.', label='BST Get Max')

    plt.plot(xlabels, values_heap_add, color='b', linestyle='-', label='Heap Add')
    plt.plot(xlabels, values_heap_min, color='b', linestyle='--', label='Heap Get Min')
    plt.plot(xlabels, values_heap_max, color='b', linestyle='-.', label='Heap Get Max')

    if slow:
        plt.plot(xlabels, values_bubble_add, color='y', linestyle='-', label='Bubble Add')
        plt.plot(xlabels, values_bubble_min, color='y', linestyle='--', label='Bubble Get Min')
        plt.plot(xlabels, values_bubble_max, color='y', linestyle='-.', label='Bubble Get Max')

        plt.plot(xlabels, values_quick_add, color='r', linestyle='-', label='Quick Add')
        plt.plot(xlabels, values_quick_min, color='r', linestyle='--', label='Quick Get Min')
        plt.plot(xlabels, values_quick_max, color='r', linestyle='-.', label='Quick Get Max')

    plt.gca().yaxis.grid(True)
    plt.legend()
    plt.xlabel("Number of Operations")
    plt.ylabel(r"Execution time ($\mu$sec)")
    if slow:
        plt.title("Performance of BST, Bubble, Heap, Quick ")
    else:
        plt.title("Performance of BST, Heap")
    plt.savefig('All')
    plt.show()

# plot BST, Heap add in log scale
    plt.plot(xlabels, values_binary_add, color='g', linestyle='-', label='BST Add')
    plt.plot(xlabels, values_heap_add, color='b', linestyle='-', label='Heap Add')

    plt.xscale('log')

    plt.gca().yaxis.grid(True)
    plt.legend()
    plt.xlabel("Number of Operations")
    plt.ylabel(r"Execution time ($\mu$sec)")
    plt.title("Performance of BST, Heap add")
    plt.savefig('BHAddlog')
    plt.show()

# plot BST, Heap add
    plt.plot(xlabels, values_binary_add, color='g', linestyle='-', label='BST Add')
    plt.plot(xlabels, values_heap_add, color='b', linestyle='-', label='Heap Add')

    plt.gca().yaxis.grid(True)
    plt.legend()
    plt.xlabel("Number of Operations")
    plt.ylabel(r"Execution time ($\mu$sec)")
    plt.title("Performance of BST, Heap add")
    plt.savefig('BHAdd')
    plt.show()

# plot BST, Heap in log scale
    plt.plot(xlabels, values_binary_add, color='g', linestyle='-', label='BST Add')
    plt.plot(xlabels, values_binary_min, color='g', linestyle='--', label='BST Get Min')
    plt.plot(xlabels, values_binary_max, color='g', linestyle='-.', label='BST Get Max')

    plt.plot(xlabels, values_heap_add, color='b', linestyle='-', label='Heap Add')
    plt.plot(xlabels, values_heap_min, color='b', linestyle='--', label='Heap Get Min')
    plt.plot(xlabels, values_heap_max, color='b', linestyle='-.', label='Heap Get Max')

    plt.xscale('log')
    plt.gca().yaxis.grid(True)
    plt.legend()
    plt.xlabel("Number of Operations")
    plt.ylabel(r"Execution time ($\mu$sec)")
    plt.title("Performance of BST and Heap")
    plt.savefig('BHlog')
    plt.show()

# plto BST, Heap
    plt.plot(xlabels, values_binary_add, color='g', linestyle='-', label='BST Add')
    plt.plot(xlabels, values_binary_min, color='g', linestyle='--', label='BST Get Min')
    plt.plot(xlabels, values_binary_max, color='g', linestyle='-.', label='BST Get Max')

    plt.plot(xlabels, values_heap_add, color='b', linestyle='-', label='Heap Add')
    plt.plot(xlabels, values_heap_min, color='b', linestyle='--', label='Heap Get Min')
    plt.plot(xlabels, values_heap_max, color='b', linestyle='-.', label='Heap Get Max')

    plt.gca().yaxis.grid(True)
    plt.legend()
    plt.xlabel("Number of Operations")
    plt.ylabel(r"Execution time ($\mu$sec)")
    plt.title("Performance of BST and Heap")
    plt.savefig('BH')
    plt.show()


    if slow:
        plt.plot(xlabels, values_bubble_add, color='y', linestyle='-', label='Bubble Add')
        plt.plot(xlabels, values_quick_add, color='r', linestyle='-', label='Quick Add')
        plt.gca().yaxis.grid(True)
        plt.legend()
        plt.xlabel("Number of Operations")
        plt.ylabel(r"Execution time ($\mu$sec)")
        plt.title("Performance Bubble, Quick Add")
        plt.savefig('allAdd')
        plt.show()


if __name__ == '__main__':
    benchmark(10100, slow=False)

