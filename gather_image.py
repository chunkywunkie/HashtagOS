from instagram.client import InstagramAPI
from datetime import datetime
import sys

# jackie's then annie's
instaclient = [('3e454d27b2704004ad3871fbe1aefa72', 'ea6fd488ddd34cb58be7bbefac99c2f8'), ('53bb6879057f4591834ba38265fdbcb4', 'b4bd805279254a139a66ccebb256d9cf')]

currentID = 0
api = InstagramAPI(client_id=instaclient[currentID][0], 
client_secret=instaclient[currentID][1])

"""
Search for image urls associated with tag (top 20)
Can search within popular or recent media
"""
def _hashImgSearch(tag, mediatype, numurl):
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

    urls = []

    i = 0
    # associated tags of the recent media
    for tag_media in tag_results:
            if i == numurl: break
            try:
                urls.append(tag_media.images['standard_resolution'].url)
                i = i + 1    
            except:
                    pass # usually errors related to privacy level of tag
    
    return urls
    
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
Write results of urls line-by-line, filename indicates details of run.
"""
def writeResults(mediatype, numurl, tagdata):
    
    # append time and day to filename
    today = datetime.today()
    date = str(today.month) + '.' + str(today.day) + '.' + str(today.year)
    time = str(today.hour) + ':' + str(today.minute)

    # create a file for each tag's urls
    for tag, urls in tagdata.items():
        outfilename = tag + '_' + date + '-' + time + '_' + mediatype + '+' + str(numurl) + '.url'
        outfile = open(outfilename, 'w')
        
        for u in urls:
            outfile.write(u + "\n") 
        outfile.close()
    

"""
Entry point
1st argument is media type
2nd+ argument(s) is list of tags to grab urls.
"""
def main():
    # starting parameters
    res = dict()
    mtype = sys.argv[1]    
    numurl = int(sys.argv[2])
    primarytags = sys.argv[3:]

    try:
        for tag in primarytags:
           res[tag] = _hashImgSearch(tag, mtype, numurl)    
    except:
        if not switchAPI(currentID):
            print "Too many API requests :("

    writeResults(mtype, numurl, res)  # write any results


if __name__ == "__main__":
    main()
