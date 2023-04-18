from django.core.mail import send_mail
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.response import Response
from reviews.models import User
from django.shortcuts import get_object_or_404
from .permissions import AdminModeratorAuthorPermission
from reviews.models import Review, Title
from .serializers import (CommentSerializer, ReviewSerializer)
from django.db.models import Avg



from .serializers import GetTokenSerializer, SingUpSerializer, UsersSerializer
from .utils import check_token, get_token_for_user, make_token


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,
                          permissions.IsAdminUser)
    serializer_class = UsersSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class SignUpView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SingUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(username=request.data.get('username'))
        confirmation_code = make_token(user)
        send_mail(
            subject='Код подтверждения для регистрации',
            message=f'Код подтверждения для пользователя {user.username}:'
                    f' {confirmation_code}',
            from_email='from@example.com',
            recipient_list=[f'{user.email}'],
            fail_silently=False
        )
        return Response(request.data, status=status.HTTP_200_OK)


class GetTokenView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data.get('username'))
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if check_token(user=user, token=data.get('confirmation_code')):
            return Response({'token': get_token_for_user(user)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)

lass ReviewViewSet(viewsets.ModelViewSet):
    rating = Review.objects.aggregate(Avg("score"))
    serializer_class = ReviewSerializer
    permission_classes = AdminModeratorAuthorPermission

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = AdminModeratorAuthorPermission

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments
    
    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
