from rest_framework import serializers
from intent_manager.models import Intent


class IntentSerializer(serializers.ModelSerializer):
    """Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes
     that can then be easily rendered into JSON, XML or other content types."""
    class Meta:
        model = Intent
        fields = '__all__'
