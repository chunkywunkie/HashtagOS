from instagram.client import InstagramAPI

api = InstagramAPI(client_id='3e454d27b2704004ad3871fbe1aefa72', 
client_secret='ea6fd488ddd34cb58be7bbefac99c2f8')

# search for tags recently associated w/ a particular tag:

tag_search, next_tag = api.tag_search(q="dog")
tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name)

tag_list = []

for tag_media in tag_recent_media:
    if hasattr(tag_media, 'tags'):
        for tag in tag_media.tags:
            tag_list.append(tag.name)

#find frequency of related tags

from collections import Counter
print Counter(tag_list)