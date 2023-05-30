from django.core.exceptions import BadRequest

from .repo import createFeed, readFeed

# adds some dummy feed content for test user in the database
def initialiseFeed():
    posts = [
        {
            "id": 1,
            "title": "Pos1",
            "content": "This is an interesting caption",
            "imageUri": "s3://my-bucket/my-file.txt",
            "created_at": "2023-05-29T12:00:00Z"
        },
        {
            "id": 2,
            "title": "Post2",
            "content": "This is a poem",
            "imageUri": "s3://my-bucket/my-file.txt",
            "created_at": "2023-05-30T12:00:00Z"
        },
        {
            "id": 3,
            "title": "Post3",
            "content": "This is another interesting caption",
            "imageUri": "s3://my-bucket/my-file.txt",
            "created_at": "2023-05-30T12:00:00Z"
        }
    ]

    createFeed(posts, 1)

# Gets the list of posts to be shown on user's feed from the database
def getFeedList(request):
        user_id = request.POST.get("user-id")
        timestamp = request.POST.get("timestamp")

        if not user_id:
            raise BadRequest('User ID is required')

        return readFeed(user_id)