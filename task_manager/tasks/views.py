
# Create your views here.

from .serializers import TaskSerializer, UserSerializer  

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Task, Comment
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from django.contrib.auth import authenticate  # Import authenticate


@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return Response({'error': 'Please provide username, password, and email'})

    user = User.objects.create_user(username=username, email=email, password=password)
    Token.objects.create(user=user)
    return Response({'success': 'User created successfully'})

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide both username and password'})

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid credentials'}, status=401)

class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print(request.META.get('HTTP_AUTHORIZATION'))
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()

class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response


class TaskMemberAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

    def get_queryset(self):
        task_id = self.kwargs['pk']
        task = Task.objects.get(id=task_id)
        
        return task.members.all()
    

@api_view(['POST', 'DELETE'])
def add_remove_task_member(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Task does not exist'}, status=404)

    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'error': 'Please provide user_id'}, status=400)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=404)

    if request.method == 'POST':
        task.members.add(user)
        return Response({'success': f'User {user.username} added to task {task.title}'})
    
    if request.method == 'DELETE':
        task.members.remove(user)
        return Response({'success': f'User {user.username} removed from task {task.title}'})

    return Response({'error': 'Invalid request method'}, status=405)


@api_view(['POST'])
def add_task_comment(request, pk):
    task = Task.objects.get(id=pk)
    text = request.data.get('text')
    if text:
        comment = Comment.objects.create(task=task, text=text)
        return Response({'success': 'Comment added successfully'})
    else:
        return Response({'error': 'Please provide text for the comment'})

@api_view(['PUT'])
def update_task_status(request, pk):
    task = Task.objects.get(id=pk)
    status = request.data.get('status')
    if status in ['Todo', 'Inprogress', 'Done']:
        task.status = status
        task.save()
        return Response({'success': f'Task status updated to {status}'})
    else:
        return Response({'error': 'Invalid status value'})

