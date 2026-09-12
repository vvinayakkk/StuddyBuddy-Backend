from rest_framework import serializers
from .models import Note, NoteImage, NoteDocument
from authentication.serializers import UserSerializer

class NoteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteImage
        fields = ['id', 'image']

class NoteDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteDocument
        fields = ['id', 'document']

class NoteSerializer(serializers.ModelSerializer):
    images = NoteImageSerializer(many=True, read_only=True)
    documents = NoteDocumentSerializer(many=True, read_only=True)
    shared_with = UserSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_by', 'shared_with', 'last_modified_by', 'rich_text_content', 'drawing', 'images', 'documents']
