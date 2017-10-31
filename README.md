# Table of Contents
1. [Introduction](README.md#introduction)
2. [General Steps](README.md#general steps)
3. [Repo directory structure](README.md#repo-directory-structure)



# Introduction

* the src program is written in Python 3.

* to run it, run `run.sh` in the main project fold named `find-political-donors-master`.

* the src folder constains two files: 1)`functions_donors.py` has all the functions; 2) `find_poslitical_donors.py` is the main script, and import all the functions from `functions_donors.py`.

* the `functions_donors.py` has imported three moduals: 1) `os` is used to identify paths of folds and files; 2)`datetime` is used to check if the date is valid or not; (3)`heapq` is used to construct a class called `MedianFinder` composed of a min-heap and a max-heap to calculate the median of a stream of the contributed amounts.


* there are three classes defined:
1. `Donoar`:to store information from a donor, extracted from one line of the input file `itcont.txt`. Public function: `validation(self)` to check if a donor has valid information; private function: `__reform(self)` to adjust the information to current forms. 
2. `MeidanFinder`: to construct a max_heap and a min_heap and define a stream of the donor amounts. Public function: `addnum(self,num)` to add a donor amount `num` and balance the min_heap and max_heap; `findmedian(self)` to return the median.
3. `MedianDonor`:to construct a two ddictionaries(`by_zipcode` and `by_date`)to store medians by zipcode and date. 
* For the `by_zipcode` dictionary: key is a tuple(`id`,`zipcode`),value is a list(`MedianFinder`,`num`, `total`). With a same key,`MedianFinder` is used to find the median of a streaming of the amounts, `num` counts the number of the donations with the same id and zipcode, `total` sums all the amounts with the same id and zipcode. Function `add_by_zipcode` can compare the current donor with the exiting the donors stored in the `by_zipcode` dictionary, update the `by_zipcode` dictionary, and write the updated donor information and the caluculated median to the output file `medianvals_by_zip.txt`.
* Analogous, for the `by_date` dictionary: key is a tuple(`id`,`date`),value is a list(`MedianFinder`,`num`, `total`). With a same key, `MedianFinder` is used to find the median of a streaming of the amounts, `num` counts the number of the donations with the same id and date. `total` sums all the amounts with the same id and date. Function `add_by_date` can compare the current donor with the exiting the donors stored in the `by_date` dictionary, update the `by_date` dictionary.


# Approach Description

The general steps in `find_poslitical_donors.py`:

To initialize the input and output:

1. first, identify the path of the running `find_poslitical_donors.py` in the `src` folder, the input file `itcont.txt` can be identified in the 'input' folder, and be opened in a 'read' mode.
* Function `initialize_input()`: parameters(none); return(handler of the input file `itcont.txt`)

2. then, initialize the two output files with a 'write' mode in the `output` folder.
* Function `initialize_output(fn_1,fn_2)`: parameters(fn_1,fn2: names of the two outputfiles)

To analyze donor information from the  line by line by using the `for` loop in :

1. initialize a class named `MedianDonor` to store and calculate the medians. 

2. read the information of a donar from each line of the input file`itcont.txt`.

3. pass the information to a class called `Donor`, and check its validation.

4. For each valid donor, analyze the its information, and put its information to a class named `MedianDonor` to calculate and store the donor information and the calculated median. for `by_zipcode`, update and write the donor information and the caluculated median to the output file `medianvals_by_zip.txt`. for `by_date`, just update the donor information and the caluculated median.

5. after scanning the entire file`itcont.txt`, the `by_date` dictionary is sorted by its key, and write the sorted dictionary to the output file `medianvals_by_date.txt`.

To close the output files.

# 
The directory structure is:

├── README.md 
├── run.sh
├── src
│   └── find_political_donors.py
│   └── functions_donors.py
├── input
│   └── itcont.txt
├── output
|   └── medianvals_by_zip.txt
|   └── medianvals_by_date.txt
├── insight_testsuite
    └── run_tests.sh
    └── results.txt
    └── tests
         └── test_1
         |   ├── input
         |   │   └── itcont.txt
         |   |__ output
         |   │   └── medianvals_by_zip.txt
         |   |__ └── medianvals_by_date.txt




