from instagram.client import InstagramAPI
from datetime import datetime
import sys

# jackie's then annie's
instaclient = [('3e454d27b2704004ad3871fbe1aefa72', 'ea6fd488ddd34cb58be7bbefac99c2f8'), ('53bb6879057f4591834ba38265fdbcb4', 'b4bd805279254a139a66ccebb256d9cf')]

currentID = 0
api = InstagramAPI(client_id=instaclient[currentID][0], 
client_secret=instaclient[currentID][1])

"""
Search for tags recently associated w/ a particular tag
Can search within popular or recent media
"""
def _hashSearch(tag, mediatype):
    tag_search, next_tag = api.tag_search(q=tag)
    
    # only considered when query brings up results
    if not tag_search: return
    
    tag_results = []

    if mediatype == 'recent':
        tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name)
        tag_results = tag_recent_media
    elif mediatype == 'popular':
        popular_media = api.media_popular()
        tag_results = popular_media
    else:
        print "media type not supported yet"
        return

    tag_list = []

    # associated tags of the recent media
    for tag_media in tag_results:
        if hasattr(tag_media, 'tags'):
            for tag in tag_media.tags:
                try:
                    count = api.tag(tag.name).media_count # total count from instagram
                    tag_list.append((tag.name, count))
                except:
                    pass # usually errors related to privacy level of tag
    return tag_list
    

"""
Debugging: Prints tag list in abc order
"""
def printTaglist(counter):
    clist = list(counter.most_common())
    for item in clist:
        print item[0], item[1]


"""
Switch client id, if possible
"""
def switchAPI(cid):
    # toggle client index
    if cid == 0:
        currentID = 1
        print "Switched to Annie's client info"
    else: 
        currentID = 0
        print "Switched to Jackie's client info"

    try:
        api = InstagramAPI(client_id=instaclient[currentID][0], 
        client_secret=instaclient[currentID][1])
        return True
    except:
        print "Something failed"
        return False

"""
Creates internal structure to hold tag data
and represent the relationships
"""
def hashGraph(tags, degree, mtype, results):
    
    # Helper functions:

    # Finds entry based on key identifier of tuple, returns that tuple
    def findEntry(tag, tagdict):
        for k,v in tagdict.items():
            if k[0] == tag:
                return k
        return None # this shouldn't happen

    # Insert's counter's keys to a list
    def valueList(counter):
        return [i[0] for i in counter]

    if degree == 0:
        return

    # initial keys we search with
    primarykey = len(results.items()) == 0

    # run against each tag
    for tag in tags:
        try:
            tagncount = _hashSearch(tag, mtype)
        except:
            if not switchAPI(currentID):
                print "Too many API requests :(( "
                return
        if not tagncount: continue        
       
        # update mapping appropriately
        key = None
        if primarykey:
            # find associated count
            count = api.tag(tag).media_count # total count from instagram
            key = (tag, count) 
        else:
            key = findEntry(tag, results)
            if not key:
                print "Something went wrong with tag %s" % tag
                return
        
        # fill new map with placeholder
        res = dict()
        for i in tagncount:
             res[i] = None

        results[key] = res

        # run on next degree using results as the new key
        try:
            hashGraph(valueList(tagncount), degree-1, mtype, results[key])
        except:
            # more than likely too many API requests
            if not switchAPI(currentID):
                print "Too many API requests :((("
                return

"""
Writes out the results by printing the tags relationships line-by-line
"""
def unravel(tagdata, degree, keys, perline):
    if not tagdata:
        line = ' '
        line = line.join(keys)
        perline.append(line)
        if keys: keys.pop()
        return

    for k, v in tagdata.items():
        tag, count = k[0], k[1]
        try:
            tokens = str(tag) + "(" + str(count) + ")"
        except UnicodeEncodeError: # avoid unicode tags 
            continue
        keys.append(tokens) # the key will always be valid
        unravel(v, degree, keys, perline)

    if keys: keys.pop()
     
"""
Write results, filename indicates details of run.
Just prints relationship on each line with their associated count
"""
def writeResults(degree, primarytags, mediatype, tagdata):
    
    # concatenate primary tags
    primary = '_'
    primary = primary.join(primarytags) + '_'
    
    # append time and day to filename
    today = datetime.today()
    date = str(today.month) + '.' + str(today.day) + '.' + str(today.year)
    time = str(today.hour) + ':' + str(today.minute)

    outfilename = primary + date + '-' + time + '_deg' + str(degree) + '_' + mediatype + '.out'

    outfile = open(outfilename, 'w') 
    
    perlinetag = []
    unravel(tagdata, degree, [], perlinetag)

    # Write out line per tag
    for l in perlinetag:
        outfile.write(l + "\n") 

    outfile.close()
    

"""
Entry point
1st argument is media type
2nd argument is degree of separation
3rd+ argument(s) is list of primary tags to start search.
"""
def main():
    # starting parameters
    res = dict()
    mtype = sys.argv[1]    
    d = int(sys.argv[2])
    primarytags = sys.argv[3:]

    try:
        hashGraph(primarytags, d, mtype, res)
    except:
        if not switchAPI(currentID):
            print "Too many API requests :("

    writeResults(d, primarytags, mtype, res)  # write any results


if __name__ == "__main__":
    main()
