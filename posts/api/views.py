from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    PostListSerializer,
    CommentSerializer
)
from .services import (
    get_all_posts,
    get_post,
    get_comment,
    get_replies,
    get_all_comments_for_post
)


class PostListAPIView(APIView):
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        serializer = self.serializer_class(get_all_posts(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, post_id):
        serializer = self.serializer_class(get_post(post_id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        serializer = get_post(post_id)
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, post_id):
        serializer = self.serializer_class(get_post(post_id))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListAPIView(APIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, post_id):
        serializer = self.serializer_class(get_all_comments_for_post(post_id), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=get_post(post_id))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, post_id, comment_id):
        serializer = self.serializer_class(get_comment(post_id, comment_id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, post_id, comment_id):
        serializer = get_comment(post_id, comment_id)
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, post_id, comment_id):
        serializer = self.serializer_class(get_comment(post_id, comment_id))
        if serializer.is_valid():
            serializer.save(author=request.user, post=get_post(post_id))
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentRepliesAPIView(APIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, post_id, comment_id):
        serializer = self.serializer_class(get_replies(post_id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id, comment_id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, parent=get_comment(post_id, comment_id))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
