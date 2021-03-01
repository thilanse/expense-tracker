from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .models import Expense
from .serializers import ExpenseSerializer


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def expense_list(request):

    if request.method == 'GET':
        expenses = Expense.objects.filter(user=request.user)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['user'] == request.user:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def expense_detail(request, pk):

    try:
        expense = Expense.objects.get(pk=pk)
    except Expense.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            if expense.user == request.user and serializer.validated_data['user'] == request.user:
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if expense.user == request.user:
            expense.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        })