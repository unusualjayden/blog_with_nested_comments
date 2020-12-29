from posts.models import Post, Comment


def get_all_posts():
    return Post.objects.all()


def get_post(post_id):
    return Post.objects.get(id=post_id)


def get_all_comments_for_post(post_id):
    return Comment.objects.filter(post=get_post(post_id)).get_descendants(include_self=True)


def get_comment(post_id, comment_id):
    return Comment.objects.filter(post=get_post(post_id)).get_descendants(include_self=True).get(id=comment_id)


def get_replies(comment_id):
    return Comment.objects.filter(id=comment_id).get_children()
