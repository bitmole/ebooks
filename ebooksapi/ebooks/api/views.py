from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from ..models import Ebook, Review
from .serializers import EbookSerializer, ReviewSerializer
from .permissions import IsAdminUserOrReadOnly, IsReviewAuthorOrReadOnly


class EbookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ebook.objects.all()
    serializer_class = EbookSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class EbookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ebook.objects.all()
    serializer_class = EbookSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        ebook_pk = self.kwargs.get('ebook_pk')
        ebook = get_object_or_404(Ebook, pk=ebook_pk)
        author = self.request.user

        # one review per user
        review = Review.objects.filter(ebook=ebook, review_author=author)
        if review.exists():
            raise ValidationError('You have already reviewed this book!')

        serializer.save(ebook=ebook, review_author=author)

class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]


# class EbookListCreateAPIView(
#         mixins.ListModelMixin,
#         mixins.CreateModelMixin,
#         generics.GenericAPIView):
# 
#     queryset = Ebook.objects.all()
#     serializer_class = EbookSerializer
# 
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
# 
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
