from rest_framework import serializers
from api.models import PDF

class PDFSerializer(serializers.Serializer):
    src = serializers.CharField(default='')
    client_name = serializers.CharField(default='')
    nouns = serializers.ListField(default=[])
    verbs = serializers.ListField(default=[])
    upload_date = serializers.DateTimeField(default=None)
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if PDF.objects(email=value).first():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        return PDF.objects.create(**validated_data)
