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
        if not (int(tempcol[0])>20110000 and int(tempcol[1])<240001 and float(tempcol[2].replace(',','.'))>3376684800):
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

    # Initialize contents of DataStream object
    stream = DataStream()
    if stream.header == {}:
        headers = {} 
        print('Header neu')
    else:
        headers = stream.header
        print('Header vorhanden',headers)
    ndlist = [np.asarray([]) for key in KEYLIST]

    # typical keyword arguments - free to extend

    # selection of signals
    signalsstr = kwargs.get('signals')
    if signalsstr is None:
        # no signals given - taking as much as possible
        signalsstr = "1-"+str(len(NUMKEYLIST))
    try:
        # produce an array of signal numbers
        signalsarray = []
        sigranges = signalsstr.split(',')
        for sig in sigranges:
            sigchan = sig.split('-')
            if len(sigchan) == 1:
                # a single number
                signalsarray.append(int(sigchan[0]))
            elif len(sigchan) == 2:
                # a range of signals
                for s in range(int(sigchan[0]),int(sigchan[1])+1):
                    signalsarray.append(s)
            else:
                # something went wrong
                print('errorhandling!!')
    except:
        print('could not create an array of signal numbers')

    # provide a fieldpoint name, e.g. if it is not part of the filename any more
    nameFP = kwargs.get('nameFP')
    
    # select FPs, e.g. if there are RCS files from different FieldPoints
    FP = kwargs.get('FP')
    headers['FP'] = FP

    # time range
    starttime = kwargs.get('starttime')
    endtime = kwargs.get('endtime')

    getfile = True
    gethead = True

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


    if nameFP is None:
        try:
            fpaux = filename.split('-GENLOG_')
            if len(fpaux) == 2 and not fpaux[0] == '':
                FPname = fpaux[0]
        except:
            print('errorhandling!')


    if getfile:

        fh = open(filename, 'rt')
        print ("filename: ",filename)
        if nameFP is None:
            try:
                fpaux = filename.split('-GENLOG_')
                if len(fpaux) == 2 and not fpaux[0] == '':
                    FPname = fpaux[0]
            except:
                print('errorhandling!')
        print('FP:',FPname)


#    print ("Hi Richard, this is the skeleton to insert your code")

    ndarray = np.asarray(ndlist)
    return DataStream([LineStruct()], headers, ndarray)


