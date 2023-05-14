from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import json

from .serializers import *
from core.models import *

@api_view(["GET"])
def get_routes(request):
    routes = [
        "/api/token",
        "/api/token/refresh",
    ]
    return Response(routes)

class LoginAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                username = serializer.data["username"]
                password = serializer.data["password"]

                user = User.objects.filter(username=username).first()
                if user is None:
                    return Response({
                        "status": 400,
                        "message": "User is not exists",
                        "data": {}
                    })

                if not user.check_password(password):

                    return Response({
                        "status": 401,
                        "message": "Invalid Password",
                        "data": {}
                    })
                
                if user.is_active is False:

                    return Response({
                        "status": 400,
                        "message": "User is Not Active",
                        "data": {}
                    })


                refresh = RefreshToken.for_user(user)

                response = Response()
                response.set_cookie(key="auth_token", value=str(refresh.access_token),httponly=True)
                response.data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return response


            return Response({
                "status": 400,
                "message": "Something went wrong!",
                "data": serializer.errors
            })


        except Exception as error:
            print(error)


class UserAPI(APIView):

    def get(self, request):
        token = request.COOKIES.get("auth_token")
        access_token = AccessToken(token)
        user = User.objects.get(pk=access_token['user_id'])
        return Response({"email": user.email})


class OverviewAPI(APIView):
    
    def get(self, request):
        texts = TextModel.objects.all()
        count = texts.count()

        data = []
        for text in texts:
            data.append({"snippet": text.text_snippet, "link": "/api/detail/"+str(text.id)})

        return Response({
                "status": 200,
                "total": count,
                "data": data
            })

class CreateAPI(APIView):
    
    def post(self, request):
        data = request.data
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            text_snippet = serializer.data["text_snippet"]
            tag_value = serializer.data["tag"]
            tag = TagModel.objects.filter(title=tag_value).first()
            if tag is None:
                tag = TagModel.objects.create(title=tag_value)
            try:
                token = request.COOKIES.get("auth_token")
                access_token = AccessToken(token)
                user = User.objects.get(pk=access_token['user_id'])
                obj = TextModel.objects.create(text_snippet=text_snippet, tag=tag, user=user)
                return Response({
                    "status": 200,
                    "message": "Successfully Created!",
                    "data": {"id": obj.id}
                })
            except:
                return Response({
                "status": 401,
                "message": "User is Not Authenticated!",
                "data": {}
            })
        
        return Response({
                "status": 400,
                "message": "Something went wrong!",
                "data": serializer.errors
            })

        

class DetailAPI(APIView):
    
    def get(self, request, id):
        text_snippet = TextModel.objects.filter(id=id).first()

        if text_snippet is None:
            return Response({
                "status": 404,
                "message": "Not Found!",
                "data": {}
            })

        response = TextModelSerializer(text_snippet)
        return Response({
                "status": 200,
                "message": "Found",
                "data": {response.data}
            })

class UpdateAPI(APIView):
    
    def put(self, request, id):
        
        text_snippet = TextModel.objects.filter(id=id).first()

        if text_snippet is None:
            return Response({
                "status": 404,
                "message": "Not Found!",
                "data": {}
            })
        
        data = request.data
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            text = serializer.data["text_snippet"]
            tag_value = serializer.data["tag"]
            tag = TagModel.objects.filter(title=tag_value).first()
            if tag is None:
                tag = TagModel.objects.create(title=tag_value)
            text_snippet.text_snippet = text
            text_snippet.tag = tag
            text_snippet.save()
            response = TextModelSerializer(text_snippet)

            return Response({
                "status": 200,
                "message": "Successfully updated.",
                "data": {}
            })


        return Response({
                "status": 400,
                "message": "Something went wrong!",
                "data": serializer.errors
            })

class DeleteAPI(APIView):
    
    def delete(self, request, id):
        
        text_snippet = TextModel.objects.filter(id=id).first()

        if text_snippet is None:
            return Response({
                "status": 404,
                "message": "Not Found!",
                "data": {}
            })

        text_snippet.delete()
        return Response({
                "status": 200,
                "message": "Successfully Deleted",
                "data": {}
            })

class TagListAPI(APIView):
    
    def get(self, request):
        queryset = TagModel.objects.all()
        response = TagModelSerializer(queryset, many=True)
        print(response.data)
        return Response({
                "status": 200,
                "message": "Found",
                "data": response.data
            })

class TagDetailAPI(APIView):
    
    def get(self, request, id):
        tag = TagModel.objects.filter(id=id).first()
        if tag is None:
            return Response({
                "status": 404,
                "message": "Not Found!",
            })

        response = TagModelSerializer(tag)
        return Response({
                "status": 200,
                "message": "Found",
                "data": response.data
            })

