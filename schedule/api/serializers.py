from rest_framework import serializers

from pts_requests.models import PtsRequest, PtsName
from pts_config.models import PtsConstructor, CameraPtsConstructor, OpticPtsConstructor, ServerRecordingRepeatConstructor, MicrophonePtsConstructor
from place_broadcast.models import PlaceConstructor, PlaceCity, EventType
from users.models import User


# Block for User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
        )


# Block for Places

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaceCity
        fields = ('id', 'name')


class EventTypeSerializer(serializers.ModelSerializer):

    direction = serializers.ChoiceField(choices=EventType.DIRECTIONS)

    class Meta:
        model = EventType
        fields = ('id', 'name', 'direction')


class PlaceSerializer(serializers.ModelSerializer):
    city_name = CitySerializer()
    event_type = EventTypeSerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model = PlaceConstructor
        fields = ('city_name', 'name', 'event_type', 'address',
                  'contact_name', 'phone', 'web', 'email_address',
                  'judge_system', 'author', 'create_date')


# block for PTS configs

class CameraPtsConstructorSerializer(serializers.ModelSerializer):
    cameras = serializers.CharField(source='cameras.name')
    cameras_id = serializers.IntegerField(source='cameras.id')
    brend = serializers.CharField(source='brend.name')
    brend_id = serializers.IntegerField(source='brend.id')
    model = serializers.CharField(source='model.name')
    model_id = serializers.IntegerField(source='model.id')

    class Meta:
        model = CameraPtsConstructor
        fields = ('cameras', 'cameras_id', 'brend', 'brend_id', 'model', 'model_id', 'quantity', )


class OpticPtsConstructorSerializer(serializers.ModelSerializer):
    optics = serializers.CharField(source='optics.name')
    optics_id = serializers.IntegerField(source='optics.id')
    brend = serializers.CharField(source='brend.name')
    brend_id = serializers.IntegerField(source='brend.id')
    model = serializers.CharField(source='model.name')
    model_id = serializers.IntegerField(source='model.id')

    class Meta:
        model = OpticPtsConstructor
        fields = ('optics', 'optics_id', 'brend', 'brend_id', 'model', 'model_id', 'quantity', )


class ServerConstructorSerializer(serializers.ModelSerializer):
    server_type = serializers.CharField(source='type.name')
    server_type_id = serializers.IntegerField(source='type.id')
    type_player = serializers.CharField(source='type_player.name')
    type_player_id = serializers.IntegerField(source='type_player.id')
    brend = serializers.CharField(source='brend.name')
    brend_id = serializers.IntegerField(source='brend.id')
    model = serializers.CharField(source='model.name')
    model_id = serializers.IntegerField(source='model.id')

    class Meta:
        model = ServerRecordingRepeatConstructor
        fields = ('server_type', 'server_type_id', 'type_player', 'type_player_id', 'brend', 'brend_id', 'model', 'model_id', 'quantity', )


class MicrophonePtsConstructorSerializer(serializers.ModelSerializer):
    microphone_type = serializers.CharField(source='type.name', allow_null=True)
    microphone_type_id = serializers.IntegerField(source='type.id', allow_null=True)
    brend = serializers.CharField(source='brend.name', allow_null=True)
    brend_id = serializers.IntegerField(source='brend.id', allow_null=True)
    model = serializers.CharField(source='model.name', allow_null=True)
    model_id = serializers.IntegerField(source='model.id', allow_null=True)

    class Meta:
        model = MicrophonePtsConstructor
        fields = ('microphone_type', 'microphone_type_id', 'brend', 'brend_id', 'model', 'model_id', 'quantity', )

        
class PtsConfigSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    event_type = EventTypeSerializer()
    place = serializers.CharField(source='place.name')
    place_id = serializers.IntegerField(source='place.id')
    camera_pts_constructor = CameraPtsConstructorSerializer(source='cameraptsconstructor_set', many=True)
    optic_pts_constructor = OpticPtsConstructorSerializer(source='opticptsconstructor_set', many=True)
    server_pts_constructor = ServerConstructorSerializer(source='serverrecordingrepeatconstructor_set', many=True)
    microphone_pts_constructor = MicrophonePtsConstructorSerializer(source='microphoneptsconstructor_set', many=True)

    class Meta:
        model = PtsConstructor
        fields = ('id', 'name', 'author', 'event_type', 'place', 'place_id', 'base_conf',
                  'clone_conf', 'camera_pts_constructor', 'optic_pts_constructor', 'server_pts_constructor', 'microphone_pts_constructor', 'microphone_quantity', 'microphone_comment',
                  'image', 'create_date')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for micro in representation['microphone_pts_constructor']:
            if not micro['quantity']:
                representation['microphone_pts_constructor'].remove(micro)
        return representation

# block for PTS requests


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
    place = PlaceSerializer()

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
