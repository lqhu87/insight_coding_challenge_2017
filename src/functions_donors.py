import os
import datetime
from heapq import heappush, heappop


def initialize_input():
    '''
    to initialize the input information
    :param fn: the file name of the input file
    :return: the file handler of the open input file
    '''
    running_path = os.path.dirname(os.path.realpath(__file__))
    root_path = '/'.join(running_path.split('/')[:-1])
    input_path = root_path + '/input/'
    for f in os.listdir(input_path):
        if f.endswith('.txt'):
            path = os.path.join(input_path,f)
    return open(path, 'r')


def initialize_output(fn_1,fn_2):
    '''
    to initalize the output files
    :param fn_1: the file name of the medianvals_by_zip
    :param fn_2: the file name of the medianvals_by_date
    :return: the file handlers of 'medianvals_by_zip' and 'medianvals_by_date' files
    '''
    running_path = os.path.dirname(os.path.realpath(__file__))
    root_path = '/'.join(running_path.split('/')[:-1])
    fp_1 = root_path + '/output/' + fn_1
    fp_2 = root_path + '/output/' + fn_2
    return open(fp_1,'w'), open(fp_2,'w')


def analyze(fh_input, fh_output_1, fh_output_2):
    '''
    :param fh_input: the file handler of the input file
    :param fh_output_1: the file handler of the output 'medianvals_by_zip' file
    :param fh_output_2: the file handler of the output 'medianvals_by_date' files
    :return: None
    '''
    median_results = MedianDonor()  # to initialize the class to calculated median values
    for line in fh_input:
        tmp_s = line.rstrip('\n')
        raw_l = tmp_s.split('|')
        donor = Donor(raw_l)  # pass information of a line to a donor
        if donor.validation():  # if the donor is valid
            median_results.add_by_zipcode(donor, fh_output_1) # calculate the median, write it to the output file by zip
            median_results.add_by_date(donor) # calculate the median by date
    median_results.sort_save_by_date(fh_output_2) # sort the median values by id and date, write it to the output file by date
    del median_results  # delete the class


def valid_zipcode(zp):
    '''
    to check the zipcode is valid with 5 or 9 digits
    :param zp: zipcode
    :return: True if zipcode is valid, else False
    '''
    if (len(zp)==5 or len(zp)==9) and zp.isdigit():
        return True
    else:
        return False


def valid_date(dt):
    '''
    to check the date is valid
    :param dt: date
    :return: Turn True if date is valid, or else False
    '''
    if len(dt) == 8 and dt.isdigit():
        month = int(dt[0:2])
        day = int(dt[2:4])
        year = int(dt[4:8])
        try:
            tmp = datetime.datetime(year, month, day)
            return True
        except ValueError:
            return False


class MedianFinder:
    '''
    to use max-heap, and min-heap to find the median value.
    '''
    def __init__(self):
        '''
        Initialize data structure.
        '''
        self.max_heap = []
        self.min_heap = []


    def addnum(self, num):
        '''
        add a number to the data structure
        :param num: a donor's amount
        :return:
        '''
        # Balance smaller half and larger half.
        if not self.max_heap or num > -self.max_heap[0]:
            heappush(self.min_heap, num)
            if len(self.min_heap) > len(self.max_heap) + 1:
                heappush(self.max_heap, -heappop(self.min_heap))
        else:
            heappush(self.max_heap, -num)
            if len(self.max_heap) > len(self.min_heap):
                heappush(self.min_heap, -heappop(self.max_heap))


    def findmedian(self):
        '''
        to return the median of the current data stream
        :return: a rounded median, int
        '''
        if len(self.min_heap) == len(self.max_heap):
            return int((-self.max_heap[0] + self.min_heap[0]) / 2 + 0.5)
        else:
            return self.min_heap[0]


class Donor():
    '''
    to get each donor's information extracted from each line in the input data file
    '''
    def __init__(self, info=[]):
        '''
        to extract necessary information of a donor
        :param info: a list containing all information of the donor
        '''
        self.cmte_id = info[0]
        self.zipcode = info[10]
        self.dt = info[13]
        self.amt = info[14]
        self.other_id = info[15]

    def __reform(self):
        '''
        to adjust donor's id for the sake of future sorting
        to adjust donor's zipcode to 5 digits
        to adjust donate amount to be a number
        :return:
        '''
        self.cmte_id = self.cmte_id.title()
        self.zipcode = str(self.zipcode[0:5])
        self.amt = int(self.amt)

    def validation(self):
        '''
        to check a donor is valid or not, and reform the donor if so.
        :return: True if the donor is valid.
        '''
        if self.cmte_id != '' \
                and self.amt != '' \
                and self.other_id == '' \
                and (valid_zipcode(self.zipcode) or valid_date(self.dt)):
            self.__reform()
            return True


class MedianDonor:
    '''
    set a class containing two dicts to deal with the calculated median values by zipcode and date.
    '''
    def __init__(self):
        '''
        self.by_zipcode:
            key: (cmte_id,zipcode)
            value: [MedianFinder, num, total amount]
        self.by_date:
            key: (cmte_id,date)
            value: [MedianFinder, num, total amount]
        '''
        self.by_zipcode = {}
        self.by_date = {}

    def add_by_zipcode(self, donor,fh):
        '''
        :param donor: a valid donor
        :param fh: the output file handler of the 'median_by_zipcode' file
        :return:
        '''
        if valid_zipcode(donor.zipcode):  # to check if zipcode is valid
            key = (donor.cmte_id, donor.zipcode)
            if key not in self.by_zipcode: # if the valid donor appears at the first time, add it to 'by_zipcode' dict
                median_heap = MedianFinder()
                median_heap.addnum(donor.amt)
                num = 1
                total = donor.amt
                self.by_zipcode[key] = [median_heap, num, total]
            else:  # if the valid donor have the same id and zipcode, update the existing dict.
                self.by_zipcode[key][0].addnum(donor.amt)
                self.by_zipcode[key][1] += 1
                self.by_zipcode[key][2] += donor.amt
            tmp_info = '|'.join(str(j) for j in [donor.cmte_id,
                                                 donor.zipcode,
                                                 self.by_zipcode[key][0].findmedian(),
                                                 self.by_zipcode[key][1],
                                                 self.by_zipcode[key][2]])
            fh.write('{}\n'.format(tmp_info))  # write the updated information to the output file

    def add_by_date(self, donor):
        if valid_date(donor.dt): # to check if date is valid
            tmp_dt = int(donor.dt[4:8] + donor.dt[0:4])
            key = (donor.cmte_id, tmp_dt)
            if key not in self.by_date: # if the valid donor appears at the first time, add it to 'by_date' dict
                median_heap = MedianFinder()
                median_heap.addnum(donor.amt)
                num = 1
                total = donor.amt
                self.by_date[key] = [median_heap, num, total]
            else:  # if the valid donor have the same id and date, update the existing dict.
                self.by_date[key][0].addnum(donor.amt)
                self.by_date[key][1] += 1
                self.by_date[key][2] += donor.amt

    def sort_save_by_date(self,fh):
        '''
        to sort and save the dict for the calculated median values by date.
        :param fh: the dict by date
        :return:
        '''
        tmp_sorted = sorted(self.by_date.items(), key=lambda key: (key[0], key[1]))  # return a sorted list of tuple (value, key)
        for i in tmp_sorted: # to write the donor with the same date to the output file
            cmte_id = i[0][0]  # get cmte_id
            tmp_dt = str(i[0][1])
            dt = tmp_dt[4:8] + tmp_dt[0:4]  # get the dt
            tmp_info = '|'.join(str(j) for j in [cmte_id,
                                                 dt,
                                                 i[1][0].findmedian(),
                                                 i[1][1],
                                                 i[1][2]])
            fh.write('{}\n'.format(tmp_info))


