from rest_framework import serializers


class ParserSerializer(serializers.Serializer):
    intent_string: serializers.CharField()
