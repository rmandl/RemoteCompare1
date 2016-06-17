"""
MagPy
RCS input filter for MagPy
Written by Richard Mandl
Short description...
"""
from __future__ import print_function

from magpy.stream import *

def GetINIData(relatedtofilename):
    # add here methods whcih you need to analyze RCS data    
    pass


def isRCS(filename):
    """
    Checks whether a file an RCS data set of form:

    """
    # if a unique pattern (e.g. in first line or filename or content) is recognized:
    #     return True
    # else:
    #     return False
    # tries to find a LabView Timestamp in the third column (seconds since 1904)
    # difference to UNIX timestamp (seconds since 1970): 1293840000 
    # 3376684800 means 2011-01-01. Before there were no RCS loggings
    try:
        temp = open(filename,'rt').readline()
        tempcol = temp.split('\t')
        if int(tempcol[0])>20110000 and int(tempcol[1])<240001 and float(tempcol[2].replace(',','.'))>3376684800:
            return False
    except:
        return False
    return True

def readRCS(filename, headonly=False, **kwargs):
    """
    DESCRIPTION:
        Reading RCS data
    PARAMETER:
        myparameter      (string) one of day,hour,minute,k   - default is minute

    """

    # typical keyword arguments - free to extend
    starttime = kwargs.get('starttime')
    endtime = kwargs.get('endtime')

    getfile = True
    gethead = True

    # Initialize contents of DataStream object
    stream = DataStream()
    headers = {}
    ndlist = [np.asarray([]) for key in KEYLIST]

    theday = extractDateFromString(filename.replace('_','-'))
    try:
        if starttime:
            if not theday[-1] >= datetime.date(stream._testtime(starttime)):
                getfile = False
        if endtime:
            if not theday[0] <= datetime.date(stream._testtime(endtime)):
                getfile = False
    except:
        # Date format not recognized. Need to read all files
        getfile = True

    if getfile:

        fh = open(filename, 'rt')
        print ("filename: ",filename)

        for line in fh:
            colsstr = line.split('\t')



    print ("Hi Richard, this is the skeleton to insert your code")

    ndarray = np.asarray(ndlist)
    return DataStream([LineStruct()], headers, ndarray)


