from instagram.client import InstagramAPI
import sys


api = InstagramAPI(client_id='3e454d27b2704004ad3871fbe1aefa72', 
client_secret='ea6fd488ddd34cb58be7bbefac99c2f8')

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
            # FIXME: switch client id/secret?
            print "Too many API requests :((("
            return
"""
Write results, draft version.
Just prints relationship on each line with their associated count
"""
def writeResults(degree, tagdata):
    outfile = open('result.out', 'w') # TODO: time/day and primary tag added to ouptut file
    
    # FIXME: remove hard coding only writes up to 2 degrees
    # FIXME: dealing with tags in unicode
    for k, v in tagdata.items():
        if v:
            for kk, vv in v.items():
                if vv:
                    for k3, v3 in vv.items():
                        try:
                            text = '%s(%d) %s(%d) %s(%d)\n' % (k[0], int(k[1]), kk[0], int(kk[1]), k3[0], int(k3[1]))
                            outfile.write(text)
                        except UnicodeEncodeError:
                            pass
    outfile.close()
    

"""
TODO: Pass in arguments, rather than hard-code
"""
def main():

    # starting parameters
    res = dict()
    d = 2
    mtype = 'recent'    
    primarytags = ['dog']

    try:
        hashGraph(primarytags, d, mtype, res)
    except:
        print "Too many API requests :("
        #FIXME: switch client id/secret?

    writeResults(d, res)  # write any results


if __name__ == "__main__":
    main()
