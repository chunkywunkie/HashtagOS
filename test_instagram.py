from instagram.client import InstagramAPI

api = InstagramAPI(client_id='3e454d27b2704004ad3871fbe1aefa72', client_secret='ea6fd488ddd34cb58be7bbefac99c2f8')
popular_media = api.media_popular(count=10)
for media in popular_media:
    print media.images['standard_resolution'].url
