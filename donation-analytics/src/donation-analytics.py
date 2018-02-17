##############################################################################
#
#  donations - a dictionary to hold the donation total amount, total count
#              and maxheap and minheap of individual donation amounts. The 
#              maxheap amd minheap are used to maintain percentile. The key 
#              is combination of recipient, zipcode and calendar year
#
#  donors - a dictionary to hold the earliest donation year of the donors.
#           The key is combination of donor name and zip code
#
##############################################################################
import sys
import time
import heapq
import math

SEPARATOR = "|"

def valid_contribution(receiver, zipcode, year, amount, donor, other):
    if len(other) != 0:
        return False
    if len(zipcode) < 5:
        return False
    if len(words[13]) != 8:
        return False
    if len(donor) == 0:
        return False
    try:
        int(amount)
    except e:
        return False
    if len(receiver) == 0:
         return False
    return True

def repeat_donor(donors, donor, zipcode, year):
    key = donor+SEPARATOR+zipcode
    if key in donors:
        if donors[key] < year:
            return True
        elif donors[key] > year:
            donors[key] = year
    else:
        donors[key] = year
    return False

def add_donation(donation, amount, percentile):
    donation[0] = donation[0]+amount
    donation[1] = donation[1]+1
    minheap = donation[2]
    maxheap = donation[3]
    if amount <= (-1)*maxheap[0]:
        heapq.heappush(maxheap, (-1)*amount)
    else:
        heapq.heappush(minheap, amount)
    rank = math.ceil(donation[1]*percentile/100)
    if len(maxheap) > rank:
        heapq.heappush(minheap, (-1)*heapq.heappop(maxheap))
    elif len(maxheap) < rank:
        heapq.heappush(maxheap, (-1)*heapq.heappop(minheap))

def new_donation(donations, key, amount):
    donations[key] = [amount, 1, [], [(-1)*amount]]

def output_donation(donations, key):
    donation = donations[key]
    return key+SEPARATOR+str((-1)*donation[3][0])+SEPARATOR+str(donation[0])+SEPARATOR+str(donation[1])

##############################    
# main process start here
##############################
donors = {}
donations = {}

if len(sys.argv) != 4:
    sys.exit("usage: python donation_analytics.py <inputfile> <percentilefile> <outputfile>")

inputfile = sys.argv[1]
percentilefile = sys.argv[2]
outputfile = sys.argv[3]
percentile = int(open(percentilefile, 'r').readline())
outfile = open(outputfile, 'w')

rownumber = 0
start = time.time()
for line in open(inputfile, 'r'):
    rownumber = rownumber+1
    if rownumber % 100000 == 0:
        print("processing rownumber="+str(rownumber))

    words = line.split(SEPARATOR)
    receiver = words[0]
    zipcode = words[10][:5]
    year = words[13][-4:]
    amount = int(words[14])
    donor = words[7]
    other = words[15]

    if not valid_contribution(receiver, zipcode, year, amount, donor, other):
        continue
    if not repeat_donor(donors, donor, zipcode, year):
        continue
    key = receiver+SEPARATOR+zipcode+SEPARATOR+year
    if key in donations:
        add_donation(donations[key], amount, percentile)
    else:
        new_donation(donations, key, amount)
    outfile.write(output_donation(donations, key)+"\n")
outfile.close()     
end = time.time()
print( 'timelapsed=' + format((end - start), '.3f'))
