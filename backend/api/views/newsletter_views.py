from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers import NewsletterSubscriptionSerializer

@api_view(['POST'])
def subscribe_to_newsletter(request):
    serializer = NewsletterSubscriptionSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({
                "message": "Вы успешно подписались на новости!",
                "email": serializer.data['email']
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "error": "Произошла ошибка при подписке.",
                "details": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)