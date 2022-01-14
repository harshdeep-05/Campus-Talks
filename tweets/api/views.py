from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView,RetrieveAPIView,RetrieveUpdateAPIView,DestroyAPIView,CreateAPIView
from tweets.models import Tweet
from .serializers import TweetListSerializer,TweetDetailSerializer,TweetCreateUpdateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly

class TweetListAPIView(ListAPIView):
    serializer_class = TweetListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__username', 'user__first_name', 'user__last_name']

    def get_queryset(self, *args, **kwargs):
        query_set_list = Tweet.objects.all()
        query = self.request.GET.get('q')
        if query:
            query_set_list = query_set_list.filter(
                    Q(content__icontains=query) |
                    Q(user__username__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
            ).distinct()
        return query_set_list


class TweetUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Tweet.objects.all().order_by('-timestamp')
    serializer_class = TweetCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class TweetDeleteAPIView(DestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class TweetDetailAPIView(RetrieveAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetDetailSerializer

class TweetCreateAPIView(CreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
