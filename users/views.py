from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from requests import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import user
from .serializers import UserSerializer, CustomRegisterSerializer


# @api_view(['GET', 'POST'])
# def user(request):
#     if request.method == 'GET':
#         return user_is_exit(request)
#     if request.method == 'POST':
#         return user_sign_up(request)


# 회원 정보 조회
def user_is_exit(request):
    pass


# 회원가입
def user_sign_up(request):
    pass

# 누구나 접근 가능
@permission_classes([AllowAny])
class create(generics.GenericAPIView):
    serializer_class = CustomRegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        serializer.is_valid(raise_exception=True)

        user = serializer.save() # request 필요 -> 오류 발생
        return Response(
            {
                # get_serializer_context: serializer에 포함되어야 할 어떠한 정보의 context를 딕셔너리 형태로 리턴
                # 디폴트 정보 context는 request, view, format
                "user": UserSerializer(
                    user, context=self.get_serializer.context()
                ).data
            },
            status=status.HTTP_201_CREATED,
        )



@api_view(['GET'])
def user_list_create_api_view(request):
    if request.method =='GET':
        users = user.objects.filter(active = True)
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)



class UsertListAPI(APIView):
    def get(self, request):
        queryset = user.objects.all()
        print(queryset)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
def hello_world(request):
    return HttpResponse("hello world!")
    # if request.method=="POST":
    #     input_name = request.POST.get('user_name')
    #     input_email = request.POST.get('user_email')
    #     input_password = request.POST.get('user_password')
    #
    #     new_user=user(name=input_name, email=input_email, password=input_password, is_deleted=False)
    #     new_user.save()
    #
    #     return HttpResponseRedirect(reverse('account:hello_world'))
    # else:
    #     new_user_list = user.objects.all()
    #     return render(request, 'account/hello_world.html', context={'new_user_list':new_user_list})