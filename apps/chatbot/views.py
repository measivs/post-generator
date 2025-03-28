from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from .models import Session, Chat
from .serializers import ChatMessageSerializer
from .post_generator import generate_response


class ChatbotView(GenericAPIView):
    """
    Handles user messages in strict 3-step flow:
    1. AI asks for topic
    2. User provides topic
    3. AI asks for platform
    4. User provides platform
    5. AI generates post
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Starts new session with static message asking for topic
        """
        session = Session.objects.create(user=request.user)
        Chat.objects.create(
            session=session,
            sender="bot",
            message="Hello! About what topic do you want to generate a post?"
        )
        
        return Response({
            "render_to_ui": "Hello! About what topic do you want to generate a post?",
            "post": "",
            "chat_history": []
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_message = serializer.validated_data.get("message")

        session = Session.objects.filter(user=request.user).latest('created_at')
        last_bot_message = Chat.objects.filter(session=session, sender="bot").last()
        last_user_message = Chat.objects.filter(session=session, sender="user").last()

        user_chat = Chat.objects.create(
            session=session,
            sender="user",
            message=user_message,
            generated_content=None
        )

        if not last_user_message:
            bot_response = "For which platform should I generate this? (LinkedIn/Instagram/Facebook/Twitter)"
            generated_post = None
            
        elif "for which platform" in last_bot_message.message.lower():
            platform = (
                "instagram" if "instagram" in user_message.lower() else
                "linkedin" if "linkedin" in user_message.lower() else
                "facebook" if "facebook" in user_message.lower() else
                "twitter" if "twitter" in user_message.lower() else
                user_message.split()[-1]
            )
            
            generated_post = generate_response(
                topic=last_user_message.message, 
                platform=platform
            )
            bot_response = f"Here is your {platform.capitalize()} post"
            
        else:
            bot_response = "Please choose a platform: LinkedIn, Instagram, Facebook, or Twitter"
            generated_post = None

        Chat.objects.create(
            session=session,
            sender="bot",
            message=bot_response,
            generated_content=generated_post
        )

        chat_history = Chat.objects.filter(session=session).order_by('timestamp')
        history = [{
            "sender": chat.sender,
            "message": chat.message,
            "generated_content": chat.generated_content
        } for chat in chat_history]

        return Response({
            "render_to_ui": bot_response,
            "post": generated_post,
            "chat_history": history
        }, status=status.HTTP_200_OK)
    