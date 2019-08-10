from rest_framework import serializers


class AlertVideoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        read_only_fields = ['name', 'hashs', 'created_on', 'updated_on']
