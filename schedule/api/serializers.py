import re
from django.db import transaction
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime
from django.core.exceptions import ValidationError

from pts_requests.models import PtsRequest, PtsName
from pts_config.models import (PtsConstructor,
                               CameraPtsConstructor,
                               Camera,
                               CameraBrend,
                               CameraModelBrend,
                               Optic,
                               OpticBrend,
                               OpticModelBrend,
                               OpticPtsConstructor,
                               ServerRecordingRepeatType,
                               ServerRecordingRepeatConstructor,
                               ServerPlayerType,
                               ServerRecordingRepeatBrend,
                               ServerRecordingRepeatModelBrend,
                               MicrophoneType,
                               MicrophoneBrend,
                               MicrophoneModelBrend,
                               MicrophonePtsConstructor,
                               Gfx,
                               GfxLicenseType,
                               GfxPtsConstructor)
from place_broadcast.models import PlaceConstructor, PlaceCity, EventType
from users.models import User


# Block for the matrices of equipment
# Cameras' block

class CameraTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ('id', 'name')


class CameraBrendSerializer(serializers.ModelSerializer):

    class Meta:
        model = CameraBrend
        fields = (
            'id',
            'name',
            'type_pts'
        )


class CameraBrendMatrixSerializer(serializers.ModelSerializer):
    camera_brend = serializers.SerializerMethodField()

    class Meta:
        model = Camera
        fields = (
            'id',
            'name',
            'camera_brend'
        )

    def get_camera_brend(self, obj):
        type_pts = self.context['request'].query_params.get('type_pts', None)

        camera_brends = CameraBrend.objects.filter(
            cameramodelbrend__type=obj).distinct()

        if type_pts:
            camera_brends = camera_brends.filter(
                Q(type_pts=type_pts) | Q(type_pts=None))

        serializer = CameraBrendSerializer(camera_brends, many=True)
        return serializer.data


class CameraBrendAnotherSerializer(serializers.ModelSerializer):

    type_camera = serializers.SerializerMethodField()

    class Meta:
        model = CameraBrend
        fields = ('id', 'name', 'type_pts', 'type_camera')

    def get_type_camera(self, obj):
        camera_model_brends = obj.cameramodelbrend_set.all()
        type_camera_list = [
            model_brend.type.pk
            for model_brend in camera_model_brends
        ]
        return set(type_camera_list)


class CameraModelSerializer(serializers.ModelSerializer):
    type = CameraTypeSerializer()
    brend = CameraBrendSerializer()

    class Meta:
        model = CameraModelBrend
        fields = (
            'id',
            'name',
            'type',
            'brend'
        )


# Optics' block

class OpticTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Optic
        fields = ('id', 'name', 'visible_to_user')


class OpticBrendSerializer(serializers.ModelSerializer):

    class Meta:
        model = OpticBrend
        fields = ('id', 'name', 'type_pts')


class OpticBrendMatrixSerializer(serializers.ModelSerializer):
    optic_brend = serializers.SerializerMethodField()

    class Meta:
        model = Optic
        fields = ('id', 'name', 'optic_brend')

    def get_optic_brend(self, obj):
        type_pts = self.context['request'].query_params.get('type_pts', None)

        optic_brends = OpticBrend.objects.filter(
            opticmodelbrend__type=obj).distinct()

        if type_pts:
            optic_brends = optic_brends.filter(
                Q(type_pts=type_pts) | Q(type_pts=None))

        serializer = CameraBrendSerializer(optic_brends, many=True)
        return serializer.data


class OpticBrendAnotherSerializer(serializers.ModelSerializer):

    type_optic = serializers.SerializerMethodField()

    class Meta:
        model = OpticBrend
        fields = ('id', 'name', 'type_pts', 'type_optic')

    def get_type_optic(self, obj):
        optic_model_brends = obj.opticmodelbrend_set.all()
        type_optic_list = [
            model_brend.type.pk
            for model_brend in optic_model_brends
        ]
        return set(type_optic_list)


class OpticModelSerializer(serializers.ModelSerializer):
    type = OpticTypeSerializer()
    brend = OpticBrendSerializer()

    class Meta:
        model = OpticModelBrend
        fields = ('id', 'name', 'type', 'brend')


# Servers' block

class ServerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerRecordingRepeatType
        fields = ('id', 'name')


class ServerPlayerTypeSerializer(serializers.ModelSerializer):

    rec_rep_type = ServerTypeSerializer()

    class Meta:
        model = ServerPlayerType
        fields = ('id', 'name', 'rec_rep_type', 'visible_to_user')


class ServerBrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerRecordingRepeatBrend
        fields = ('id', 'name', 'type_pts')


class ServerModelSerializer(serializers.ModelSerializer):

    brend = ServerBrendSerializer()

    class Meta:
        model = ServerRecordingRepeatModelBrend
        fields = ('id', 'name', 'brend')


# Block for microphones

class MicrophoneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicrophoneType
        fields = ('id', 'name')


class MicrophoneBrendSerializer(serializers.ModelSerializer):

    type_pts = serializers.SerializerMethodField(allow_null=True)
    type_micro = serializers.SerializerMethodField()

    class Meta:
        model = MicrophoneBrend
        fields = ('id', 'name', 'type_pts', 'type_micro')

    def get_type_pts(self, obj):
        microphone_model_brends = obj.microphonemodelbrend_set.all()
        type_pts_list = [
            model_brend.type_pts.pk
            for model_brend in microphone_model_brends
        ]
        return set(type_pts_list)

    def get_type_micro(self, obj):
        microphone_model_brends = obj.microphonemodelbrend_set.all()
        type_micro_list = [
            model_brend.type_micro.pk
            for model_brend in microphone_model_brends
        ]
        return set(type_micro_list)


class MicrophoneModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = MicrophoneModelBrend
        fields = ('id', 'name', 'brend', 'type_micro', 'type_pts')


# block for GFX

class GfxTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gfx
        fields = ('id', 'name', )


# class GfxModelSerializer(serializers.ModelSerializer):

#     type = GfxTypeSerializer()

#     class Meta:
#         model = GfxModel
#         fields = ('id', 'name', 'type')


class GfxLicenseTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GfxLicenseType
        fields = ('id', 'name', )


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
        fields = ('id', 'city_name', 'name', 'event_type', 'address',
                  'contact_name', 'phone', 'web', 'email_address',
                  'judge_system', 'author', 'create_date')


class PlaceSerializerSave(serializers.ModelSerializer):

    city_name = serializers.PrimaryKeyRelatedField(
        queryset=PlaceCity.objects.all()
    )
    event_type = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            queryset=EventType.objects.all()
        ), allow_empty=False
    )
    create_date = serializers.DateTimeField(
        default=datetime.now, read_only=True
    )
    # temporary without login
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = PlaceConstructor
        fields = (
            'name',
            'city_name',
            'event_type',
            'address',
            'contact_name',
            'phone',
            'web',
            'email_address',
            'judge_system',
            'author',
            'create_date'
        )

    def validate_phone(self, value):
        if len(value) > 15 or not re.match(r'^\+?\d+$', value):
            raise ValidationError('Invalid phone number')
        return value

    def validate_web(self, value):
        if value:
            if not re.match(
                r'^(https?://)?(www\.)?[\w.-]+\.[a-zA-Z]{2,}(\/\S*)?$', value
            ):
                raise ValidationError('Invalid website address')
        return value

    def validate(self, data):
        data = super().validate(data)
        name = data.get('name')
        city_name = data.get('city_name')
        author = data.get('author')

        if name and city_name and author:
            existing_place = PlaceConstructor.objects.filter(
                Q(name=name) & Q(city_name=city_name) & Q(author=author)
            ).first()

            if existing_place:
                raise serializers.ValidationError(
                    'A place with the same name, city, and author '
                    'already exists.'
                )

        return data

    @transaction.atomic
    def create(self, validated_data):
        event_types = validated_data.pop('event_type')
        # when login was login add
        # validated_data['author'] =
        place = PlaceConstructor.objects.create(**validated_data)
        place.event_type.set(event_types)
        return place

    @transaction.atomic
    def update(self, place, validated_data):
        event_types = validated_data.pop('event_type', None)

        place.name = validated_data.get('name', place.name)
        place.city_name = validated_data.get('city_name', place.city_name)
        place.address = validated_data.get('address', place.address)
        place.contact_name = validated_data.get(
            'contact_name', place.contact_name)
        place.phone = validated_data.get('phone', place.phone)
        place.web = validated_data.get('web', place.web)
        place.email_address = validated_data.get(
            'email_address', place.email_address)
        place.judge_system = validated_data.get(
            'judge_system', place.judge_system)

        if event_types is not None:
            place.event_type.set(event_types)

        place.save()
        return place

    def to_representation(self, place):
        serializer = PlaceSerializer(instance=place, context=self.context)
        return serializer.data


# block for PTS configs

class CameraPtsConstructorSerializer(serializers.ModelSerializer):
    cameras = serializers.CharField(source='cameras.name')
    cameras_id = serializers.IntegerField(source='cameras.id')
    brend = serializers.CharField(source='brend.name', allow_null=True)
    brend_id = serializers.IntegerField(source='brend.id', allow_null=True)
    model = serializers.CharField(source='model.name', allow_null=True)
    model_id = serializers.IntegerField(source='model.id', allow_null=True)

    class Meta:
        model = CameraPtsConstructor
        fields = ('cameras', 'cameras_id', 'brend',
                  'brend_id', 'model', 'model_id', 'quantity', )


class OpticPtsConstructorSerializer(serializers.ModelSerializer):
    optics = serializers.CharField(source='optics.name')
    optics_id = serializers.IntegerField(source='optics.id')
    brend = serializers.CharField(source='brend.name', allow_null=True)
    brend_id = serializers.IntegerField(source='brend.id', allow_null=True)
    model = serializers.CharField(source='model.name', allow_null=True)
    model_id = serializers.IntegerField(source='model.id', allow_null=True)

    class Meta:
        model = OpticPtsConstructor
        fields = ('optics', 'optics_id', 'brend', 'brend_id', 'model',
                  'model_id', 'quantity', )


class ServerConstructorSerializer(serializers.ModelSerializer):
    server_type = serializers.CharField(source='type.name')
    server_type_id = serializers.IntegerField(source='type.id')
    type_player = serializers.CharField(source='type_player.name')
    type_player_id = serializers.IntegerField(source='type_player.id')
    brend = serializers.CharField(source='brend.name', allow_null=True)
    brend_id = serializers.IntegerField(source='brend.id', allow_null=True)
    model = serializers.CharField(source='model.name', allow_null=True)
    model_id = serializers.IntegerField(source='model.id', allow_null=True)

    class Meta:
        model = ServerRecordingRepeatConstructor
        fields = ('server_type', 'server_type_id', 'type_player',
                  'type_player_id', 'brend', 'brend_id', 'model',
                  'model_id', 'quantity', )


class MicrophonePtsConstructorSerializer(serializers.ModelSerializer):
    microphone_type = serializers.CharField(
        source='type.name',
        allow_null=True
    )
    microphone_type_id = serializers.IntegerField(
        source='type.id',
        allow_null=True
    )
    brend = serializers.CharField(source='brend.name', allow_null=True)
    brend_id = serializers.IntegerField(source='brend.id', allow_null=True)
    model = serializers.CharField(source='model.name', allow_null=True)
    model_id = serializers.IntegerField(source='model.id', allow_null=True)

    class Meta:
        model = MicrophonePtsConstructor
        fields = ('microphone_type', 'microphone_type_id', 'brend',
                  'brend_id', 'model', 'model_id', 'quantity', )


class GfxPtsConstructorSerializer(serializers.ModelSerializer):
    gfx_type = serializers.CharField(source='gfx.name', allow_null=True)
    gfx_type_id = serializers.IntegerField(source='gfx.id', allow_null=True)
    license_type = GfxLicenseTypeSerializer(many=True)

    class Meta:
        model = GfxPtsConstructor
        fields = ('gfx_type', 'gfx_type_id', 'license_type',
                  'judicial_system', 'quantity', )


class PtsConfigSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    event_type = EventTypeSerializer()
    place = serializers.CharField(source='place.name')
    place_id = serializers.IntegerField(source='place.id')
    camera_pts_constructor = CameraPtsConstructorSerializer(
        source='cameraptsconstructor_set',
        many=True
    )
    optic_pts_constructor = OpticPtsConstructorSerializer(
        source='opticptsconstructor_set',
        many=True
    )
    server_pts_constructor = ServerConstructorSerializer(
        source='serverrecordingrepeatconstructor_set',
        many=True
    )
    microphone_pts_constructor = MicrophonePtsConstructorSerializer(
        source='microphoneptsconstructor_set',
        many=True
    )
    gfx_pts_constructor = GfxPtsConstructorSerializer(
        source='gfxptsconstructor_set',
        many=True
    )

    class Meta:
        model = PtsConstructor
        fields = ('id', 'name', 'author', 'event_type', 'place', 'place_id',
                  'base_conf', 'clone_conf', 'camera_pts_constructor',
                  'optic_pts_constructor', 'server_pts_constructor',
                  'microphone_pts_constructor', 'gfx_pts_constructor',
                  'microphone_quantity', 'microphone_comment', 'image',
                  'create_date')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for micro in representation['microphone_pts_constructor']:
            if not micro['quantity']:
                representation['microphone_pts_constructor'].remove(micro)
        return representation


# Block for creating PTS config

class CameraConstructorSaveSerializer(serializers.ModelSerializer):

    cameras = serializers.PrimaryKeyRelatedField(
        queryset=Camera.objects.all(),
    )
    brend = serializers.PrimaryKeyRelatedField(
        queryset=CameraBrend.objects.all(),
        required=False,
    )
    model = serializers.PrimaryKeyRelatedField(
        queryset=CameraModelBrend.objects.all(),
        required=False,
    )

    class Meta:
        model = CameraPtsConstructor
        fields = ('cameras', 'brend', 'model', 'quantity',)


class OpticConstructorSaveSerializer(serializers.ModelSerializer):
    optics = serializers.PrimaryKeyRelatedField(
        queryset=Optic.objects.all(),
    )
    brend = serializers.PrimaryKeyRelatedField(
        queryset=OpticBrend.objects.all(),
        required=False,
    )
    model = serializers.PrimaryKeyRelatedField(
        queryset=OpticModelBrend.objects.all(),
        required=False,
    )

    class Meta:
        model = OpticPtsConstructor
        fields = ('optics', 'brend', 'model', 'quantity',)


class ServerConstructorSaveSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(
        queryset=ServerRecordingRepeatType.objects.all(),
    )
    type_player = serializers.PrimaryKeyRelatedField(
        queryset=ServerPlayerType.objects.all(),
    )
    brend = serializers.PrimaryKeyRelatedField(
        queryset=ServerRecordingRepeatBrend.objects.all(),
        required=False,
    )
    model = serializers.PrimaryKeyRelatedField(
        queryset=ServerRecordingRepeatModelBrend.objects.all(),
        required=False,
    )

    class Meta:
        model = ServerRecordingRepeatConstructor
        fields = ('type', 'type_player', 'brend', 'model', 'quantity',)


class GfxConstructorSaveSerializer(serializers.ModelSerializer):

    gfx = serializers.PrimaryKeyRelatedField(
        queryset=Gfx.objects.all(),
    )
    license_type = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            queryset=GfxLicenseType.objects.all()
        ), allow_empty=True
    )

    class Meta:
        model = GfxPtsConstructor
        fields = ('gfx', 'license_type', 'judicial_system', 'quantity', )


class PtsConfigSerializerSave(serializers.ModelSerializer):

    # temporary without login
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # temporary without login

    event_type = serializers.PrimaryKeyRelatedField(
        queryset=EventType.objects.all(),
        allow_empty=False),
    place = serializers.PrimaryKeyRelatedField(
        queryset=PlaceConstructor.objects.all()
    )
    create_date = serializers.DateTimeField(
        default=datetime.now, read_only=True
    )
    camera_pts_constructor = CameraConstructorSaveSerializer(many=True, required=False,)
    optic_pts_constructor = OpticConstructorSaveSerializer(many=True, required=False,)
    server_pts_constructor = ServerConstructorSaveSerializer(many=True, required=False,)
    gfx_pts_constructor = GfxConstructorSaveSerializer(many=True, required=False,)

    class Meta:
        model = PtsConstructor
        fields = (
            'name', 'author', 'event_type', 'place', 'base_conf', 'clone_conf',
            'camera_pts_constructor', 'optic_pts_constructor',
            'server_pts_constructor', 'gfx_pts_constructor', 'microphone_quantity',
            'microphone_comment', 'image', 'create_date'
        )

    @transaction.atomic
    def create(self, validated_data):
        camera_pts_constructor_data = validated_data.pop(
            'camera_pts_constructor', None
        )
        optic_pts_constructor_data = validated_data.pop(
            'optic_pts_constructor', None
        )
        server_pts_constructor_data = validated_data.pop(
            'server_pts_constructor', None
        )
        gfx_pts_constructor_data = validated_data.pop(
            'gfx_pts_constructor', None
        )

        pts_constructor = PtsConstructor.objects.create(**validated_data)

        if camera_pts_constructor_data:
            for camera_pts_data in camera_pts_constructor_data:
                CameraPtsConstructor.objects.create(
                    constructor=pts_constructor, **camera_pts_data
                )

        if optic_pts_constructor_data:
            for optic_pts_data in optic_pts_constructor_data:
                OpticPtsConstructor.objects.create(
                    constructor=pts_constructor, **optic_pts_data
                )

        if server_pts_constructor_data:
            for server_pts_data in server_pts_constructor_data:
                ServerRecordingRepeatConstructor.objects.create(
                    constructor=pts_constructor, **server_pts_data
                )

        if gfx_pts_constructor_data:
            for gfx_pts_data in gfx_pts_constructor_data:
                license_type = gfx_pts_data.pop('license_type', [])
                gfx_pts_constructor = GfxPtsConstructor.objects.create(constructor=pts_constructor, **gfx_pts_data)
                gfx_pts_constructor.license_type.set(license_type)

        return pts_constructor

    def to_representation(self, pts_constructor):
        serializer = PtsConfigSerializer(
            instance=pts_constructor, context=self.context
        )
        return serializer.data


# block for PTS requests

class PtsSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = PtsName
        fields = ('id', 'name', 'head_fullname', 'head_contact',
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
    pts_cfg = PtsConfigSerializer()
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
