"""PostReactions Views Module"""
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rareapi.models import PostReaction, Reaction, Post, RareUser


class PostReactions(ViewSet):
    """ Responsible for GET, POST, DELETE """

    def list(self, request):
        """ GET all postreaction objects """
        postreactions = PostReaction.objects.all()

        post_id = self.request.query_params.get("postId", None)
        if post_id is not None:
            postreactions = postreactions.filter(post_id=post_id)

        serializer = PostReactionSerializer(
            postreactions, many=True, context={'request', request})
        return Response(serializer.data)

    def create(self, request):
        """ POST """
        rareuser = RareUser.objects.get(user=request.auth.user)
        postreaction = PostReaction()

        # these match the properties in PostForm.js
        post_id = request.data["post_id"]
        reaction_id = request.data["reaction_id"]

        # check if post exists
        try:
            post = Post.objects.get(id=post_id)

        except Post.DoesNotExist:
            return Response({'message: invalid post id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # check if reaction exists
        try:
            reaction = Reaction.objects.get(id=reaction_id)
        except Reaction.DoesNotExist:
            return Response({'message: invalid reaction id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # check if postreaction exists

        try:
            postreaction = PostReaction.objects.get(
                post=post, reaction=reaction, user=rareuser)
            if postreaction.user.id == rareuser:
                return Response({'message': 'Postreaction already exists for these two items'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except PostReaction.DoesNotExist:
        #     #if it does not exist, make new obj
            
            postreaction = PostReaction()
            postreaction.post = post
            postreaction.reaction = reaction
            postreaction.user = rareuser

            if rareuser is not None:

                try:
                    postreaction.save()
                    serializer = PostReactionSerializer(
                        postreaction, many=False, )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except ValidationError as ex:
                    return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """ DELETE """
        try:
            postreaction = PostReaction.objects.get(pk=pk)
            postreaction.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except PostReaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostReactionSerializer(serializers.ModelSerializer):
    """ Serializes PostTags """
    class Meta:
        model = PostReaction
        fields = ('id', 'user', 'reaction', 'post')
        depth = 1
        # so we can access whole reaction and post object
