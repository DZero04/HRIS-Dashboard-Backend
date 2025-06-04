from rest_framework import serializers
from .models import *

class DataTab1ToTab3Serializer(serializers.ModelSerializer):
    class Meta:
        model = DataTab1ToTab3
        fields = '__all__'

class DataTab4Serializer(serializers.ModelSerializer):
    class Meta:
        model = DataTab4
        fields = '__all__'

class DataTab5OTSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataTab5OT
        fields = '__all__'

class DataTab5TravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataTab5Travel
        fields = '__all__'

class DataTab6Serializer(serializers.ModelSerializer):
    class Meta:
        model = DataTab6
        fields = '__all__'

class DataTab8Serializer(serializers.ModelSerializer):
    class Meta:
        model = DataTab8
        fields = '__all__'

class DataTab9Serializer(serializers.ModelSerializer):
    class Meta:
        model = DataTab9
        fields = '__all__'

class DataChurnRiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataChurnRisk
        fields = '__all__'

class DataTab7Serializer(serializers.ModelSerializer):
    class Meta:
        model = DataTab7
        fields = '__all__'