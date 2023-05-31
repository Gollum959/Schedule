from rest_framework import serializers

from pts_requests.models import PtsRequest, PtsName
from pts_config.models import PtsConstructor
from place_broadcast.models import PlaceConstructor


class PlaceForRequestsSerializer(serializers.ModelSerializer):
    city_name = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = PlaceConstructor
        fields = ('city_name', 'name', 'address', 'contact_name', 'phone')


class PtsConfigForRequestsSerializer(serializers.ModelSerializer):
    event_type = serializers.SlugRelatedField(
        read_only=True, slug_field='name')

    class Meta:
        model = PtsConstructor
        fields = ('name', 'event_type')


class PtsSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = PtsName
        fields = ('name', 'head_fullname', 'head_contact',
                  'deputi_head_fullname', 'deputi_head_contact',
                  'other_information', 'type')


class PtsRequestSerializer(serializers.ModelSerializer):
    start_date = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')
    author = serializers.SerializerMethodField()
    pts_name = PtsSerializer()
    pts_cfg = PtsConfigForRequestsSerializer()
    place = PlaceForRequestsSerializer()

    class Meta:
        model = PtsRequest
        fields = ('id', 'start_date', 'start_time', 'end_date', 'end_time',
                  'name', 'status', 'author', 'pts_name', 'pts_cfg', 'place')

    def get_start_date(self, obj):
        return obj.broadcast_start_date.strftime('%Y-%m-%d')

    def get_end_date(self, obj):
        return obj.broadcast_end_date.strftime('%Y-%m-%d')

    def get_start_time(self, obj):
        return obj.broadcast_start_date.strftime('%H:%M')

    def get_end_time(self, obj):
        return obj.broadcast_end_date.strftime('%H:%M')

    def get_author(self, obj):
        return obj.author.get_full_name() if obj.author else None
