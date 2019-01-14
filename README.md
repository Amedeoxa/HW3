# HW3
This benchmark is our third assignment for PCSII course of Sapienza University.
# Third PCSII Assignment

## Benchmark analysis of `BinarySearchTree`, `Heap` data structures and `QuickSort`, `BubbleSort` sorting algorithms with Python

### The goal is to measure the time our four different approaches take to take in data from and unordered list of random numbers, and the time it takes to return the smallest and the largest number of the list.

I've created a class for each approach with the following methods:
* add: receives a number from the list of random numbers and adds it to the class object
* get_min: returns the smallest number 
* get_max: returns the largest number

For the benchmark I've tested the four classes using lists of numbers generated with `random.randint()` of increasing size, from 100 elements to 10000 elements with increments of 100. The performance was measured with `time.time()` for each method of each class 20 times for precision.

In the file [data](https://github.com/Amedeoxa/HW3/tree/master/data) and [datawithBQ](https://github.com/Amedeoxa/HW3/tree/master/datawithBQ)\\\\ you can find more graphs and the [csv](https://github.com/Amedeoxa/HW3/blob/master/data/data_table.csv) containing the table with the benchmark numbers. And [here](https://github.com/Amedeoxa/HW3/blob/master/hw3.py) you can find the actual Python code used.

Here is a table of the times(in μs) of the first 10 runs:

|             |             |            |         |          |             |             |              |              |               |               |                |                | 
|-------------|-------------|------------|---------|----------|-------------|-------------|--------------|--------------|---------------|---------------|----------------|----------------| 
| List length | Bubble add  | Quick add  | BST add | Heap add | BST get_min | BST get_max | Heap get_min | Heap get_max | Quick get_min | Quick get_max | Bubble get_min | Bubble get_max | 
| 100         | 36.2082     | 12.64749   | 0.74391 | 0.19832  | 0.09928     | 0           | 0            | 0            | 0.09918       | 0.09959       | 0.04959        | 0.09923        | 
| 200         | 274.88289   | 52.22116   | 1.09141 | 0.04954  | 0.29745     | 0.34711     | 0.09918      | 0.04959      | 0.14875       | 0.05312       | 0.04961        | 0.04959        | 
| …           | …           | …          | …       | …        | …           | …           | …            | …            | …             | …             | …              | …              | 
| 800         | 17549.44811 | 939.973    | 5.60141 | 0.843    | 1.58699     | 0.9922      | 0.54569      | 0.44663      | 0.74468       | 0.39711       | 1.08507        | 0.55211        | 
| 900         | 24851.5837  | 1250.17579 | 6.34975 | 0.74441  | 1.49138     | 1.98169     | 0.5425       | 0.74358      | 1.04506       | 0.44901       | 1.38571        | 0.83988        | 
| 1000        | ***34680.15754*** | **1492.45019** | 6.74284 | 0.79341  | 1.44022     | 2.28565     | 0.4962       | 0.49605      | 1.23847       | 0.8461        | 2.38478        | 0.69716        | 


As we can see the `BubbleSort` algorithm quickly becomes unmanageable, taking ~5000x longer than `BinarySearchTree` to ad a new element as the lists reached length 1400. Infact `BubbleSort` has an average time complexity of **O(n^2)**. Likewise `QuickSort` hase an average time commplexity of O(nlog(n)), and slows much faster then `BinarySearchTree` and `Heap`.

![image addAll](https://github.com/Amedeoxa/HW3/blob/master/datawithBQ/allAdd.png)\\\\\\

Therefore, we continued **without** `BubbleSort` of `Quicksort` for lists > 1000.

### Here is a table of the times(in μs) for list length up to 10000


|             |          |             |             |          |              |              | 
|-------------|----------|-------------|-------------|----------|--------------|--------------| 
| List length | BST add  | BST get_min | BST get_max | Heap add | Heap get_min | Heap get_max | 
| 100         | 0.84493  | 0.19829     | 0.19677     | 0.09911  | 0            | 0            | 
| 200         | 1.73593  | 0.29747     | 0.14904     | 0.24796  | 0.09909      | 0.04969      | 
| 300         | 2.18198  | 0.54643     | 0.54524     | 0.24805  | 0.09918      | 0.19848      | 
| …           | …        | …           | …           | …        | …            | …            | 
| 5900        | 50.60501 | 7.97527     | 15.27708    | 5.35626  | 3.27377      | 3.42383      | 
| 6000        | 46.62316 | 8.7193      | 16.11521    | 5.10993  | 3.47192      | 3.77004      | 
| 6100        | 46.05479 | 22.60761    | 10.23612    | 5.91118  | 3.02699      | 3.12045      | 
| …           | …        | …           | …           | …        | …            | …            | 
| 9800        | 86.98492 | 15.49006    | 21.03248    | 8.21636  | 5.02708      | 6.14443      | 
| 9900        | 80.54256 | 24.47503    | 18.77801    | 7.88913  | 5.98121      | 5.15652      | 
| 10000       | 73.54188 | 22.02954    | 29.72786    | 7.56209  | 5.91767      | 5.20909      | 



#### A graph of the performance of `BinarySearchTree` and `Heap`
![All](https://github.com/Amedeoxa/HW3/blob/master/data/All.png)
![Alllog](https://github.com/Amedeoxa/HW3/blob/master/data/Alllog.png)


#### `get_min` and `get_max`
As we can see from the graph below, getting the min and max from `QuickSort` (and `BubbleSort` for that matter) and `Heap`
immediate. This is because the all we are doing is accessing the first or last element of a list.
`BinarySearchTree` instead takes a bit more time since we must traverse all the tree's leftmost or rightmost branches.

![allMinMax](https://github.com/Amedeoxa/HW3/blob/master/datawithBQ/allMinMax.png)
![allMinMax](https://github.com/Amedeoxa/HW3/blob/master/data/allMinMax.png)



#### `add`
As we can see from the graph below, adding a random value to our `Heap` is the quickest since we add it to the first free branch, only checking if it is smaller or larger than our root. Worst case time complexity is O(log(n)), but on average it is closer to O(1) 

`BinarySearchTree`is the second fastest of the four with a time complexity averaging O(log(n)). 

`QuickSort` takes more time since every value must be added to a list wich is then sorted. It's time complexity is steady at O(nlog(n)).

`BubbleSort` is by far the slowest, becoming unusable on larger data sets, with an average time complexity of O(n^2)!


![allAdd](https://github.com/Amedeoxa/HW3/blob/master/data/allAdd.png)

In conclusion the winner of this benchmark is the `Heap` data structure :1st_place_medal:

#### System Information
Python 3.5
OS Windows 10 Pro
CPU Intel(R) Core(TM) i5-6200U CPU @ 2.30GHz
Installed Physical Memory (RAM)	8.00 GB




