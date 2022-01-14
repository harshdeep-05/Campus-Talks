from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField, SerializerMethodField
from tweets.models import Tweet

class TweetListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="tweets-api:detail")
    delete_url = HyperlinkedIdentityField(view_name="tweets-api:delete")
    user = SerializerMethodField()
    class Meta:
        model = Tweet
        fields = [
            'url',
            'user',
            'id',
            'content',
            'timestamp',
            'delete_url',
        ]
    def get_user(self, obj):
        return str(obj.user.username)

class TweetCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Tweet
        fields = [
            'content',
        ]

class TweetDetailSerializer(ModelSerializer):
    class Meta:
        model = Tweet
        fields = [
            'content',
            'timestamp',
            'retweet_status',
        ]
