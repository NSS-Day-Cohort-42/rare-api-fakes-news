"""PostTags Views Module"""
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rareapi.models import PostTag, Tag, Post


class PostTags(ViewSet):
    """ Responsible for GET, POST, DELETE """
    def list(self, request):
        """ GET all pt objects """
        posttags = PostTag.objects.all()

        post_id = self.request.query_params.get("postId", None)
        if post_id is not None:
            posttags = posttags.filter(post_id=post_id)
        
        serializer = PostTagsSerializer(posttags, many=True, context={'request', request})
        return Response(serializer.data)

    def create(self, request):
        """ POST """
        post_id = request.data["post_id"]
        tag_id = request.data["tag_id"]
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'message: invalid post id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response({'message: invalid tag id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        try: 
            posttag = PostTag.objects.get(post=post, tag=tag)
            return Response({'message': 'Posttag already exists for these two items'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except PostTag.DoesNotExist:
            posttag = PostTag()
            posttag.post = post
            posttag.tag = tag
            try: 
                posttag.save()
                serializer = PostTagsSerializer(posttag, many=False, )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """ DELETE """
        try:
            posttag = PostTag.objects.get(pk=pk)
            posttag.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except PostTag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostTagsSerializer(serializers.ModelSerializer):
    """ Serializes PostTags """
    class Meta:
        model = PostTag
        fields = ('id', 'tag', 'post')
        depth = 1
