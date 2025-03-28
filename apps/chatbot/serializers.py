from rest_framework import serializers

class ChatMessageSerializer(serializers.Serializer):
    """
    Serializer for validating and handling user messages in the chatbot.
    """
    message = serializers.CharField(required=True, max_length=500, help_text="The message the user sends to the bot.")

    def validate_message(self, value):
        """
        Custom validation for the user's message.
        """
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message cannot be empty.")
        return value
