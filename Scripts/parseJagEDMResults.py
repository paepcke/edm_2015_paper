'''
Created on Feb 6, 2015

@author: paepcke

Takes a file created by Jagadish's snippet extraction
and ranking. Outputs to stdout a CSV:
query,rank1,treatment1,rank2,treatment2,minute1,captionFileName1,minute2,captionFileName2

Example input line:
    1#8idf: 1#13tf: If you want... **Metadata: filename: 9 min: /Users/jag/Downloads/Stanford medstats/HRP261 Unit1 Mod1.srt **Metadata: filename: 9 min: /Users/jag/Downloads/Stanford medstats/HRP261 Unit1 Mod1.srt

Respective output:
    Q1,8,idf,13,tf,9,HRP261 Unit1 Mod1,9,HRP261 Unit1 Mod1

When rank2/treatment2 are absent, properly inserts empty columns.
'''

import sys

def parseSnippetLabel(snipLabel):
    '''
    Given something like 1#8idf: return (8,idf):
    '''
    # Peel the 8 from 8idf:
    try:
        snipLabelRankAndTreatment = snipLabel.split('#')[1]
    except IndexError:
        # Not a well formed snipLabel:
        return (None,None)
    rank = getInt(snipLabelRankAndTreatment)
    # Get the 'tf' or 'idf' from '8idf'
    strPtr = len(snipLabelRankAndTreatment) - 1
    while not snipLabelRankAndTreatment[strPtr].isdigit():
        strPtr -= 1
    treatment = snipLabelRankAndTreatment[strPtr+1:len(snipLabelRankAndTreatment)]
    return (rank,treatment)

def getInt(label):
    '''
    Given a string, try to grab an int from the start.
    Return the int if there, else return None
    '''
    res = None
    for aChar in label:
        if aChar.isdigit():
            res = int(aChar) if res is None else 10*res + int(aChar)
        else:
            return res
    

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print('Usage: parseJagEDMResults.py idfOrTfResultsFilePath')
    with open(sys.argv[1], 'r') as fd:
        #print('Arg: %s' % sys.argv[0])
        queryCount = 0
        for line in fd:
            resLine = ''
            # Something like: ['1#8idf', ' 1#13tf', " If you want...**Metadata: filename: 9 min: /Users/jag/Downloads/Stanford medstats/HRP261 Unit1 Mod1.srt **Metadata: filename: 9 min: /Users/jag/Downloads/Stanford medstats/HRP261 Unit1 Mod1.srt
            #print('|%s|' % line)
            if len(line.strip()) == 0 or line.startswith('***'):
                continue
            if line.startswith('QUERY:'):
                queryCount +=1
                continue
            resLine += 'Q%d,' % queryCount
            # Now pointing to something like 1#8idf:
            # point to #
            colonArr = line.split(':')
            # Process 1#8idf (we always have one):
            (rank,treatment) = parseSnippetLabel(colonArr[0])
            resLine += '%s,%s,' % (str(rank),treatment)
            # A second marker there? (e.g. the 1#13tf)
            # This either gets the 1#13tf, or a snippet):
            maybeLabel = colonArr[1].strip()
            (rank,treatment) = parseSnippetLabel(maybeLabel)
            if rank is None:
                rank = ''
                treatment = ''
            resLine += '%s,%s' % (str(rank),treatment)
            # Next element in colonArr is the snippet itself; 
            # don't need it. Instead, get the **Metadata endings:
            metaStartPos = line.find('**Metadata')
            metaData = line[metaStartPos:]
            # Now have: 
            # **Metadata: filename: 9 min: /Users/jag/Downloads/Stanford medstats/HRP261 Unit1 Mod1.srt **Metadata: filename: 9 min: /Users/jag/Downloads/Stanford medstats/HRP261 Unit1 Mod1.srt
            metaDataArr = metaData.split('**Metadata: filename: ')
            for metaData in metaDataArr:
                if len(metaData) == 0:
                    continue
                minute = getInt(metaData)
                fileArr = metaData.split('/')
                # Only need last part of file name, without the .srt:
                videoDesc = fileArr[-1].split('.')[0]
                resLine += ',%s,%s' % (minute, videoDesc)
            print('%s' % resLine)
        
                
            

        
         
