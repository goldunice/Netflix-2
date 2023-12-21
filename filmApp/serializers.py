from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import *


class AktyorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    ism = serializers.CharField()
    davlat = serializers.CharField()
    jins = serializers.CharField()
    tugilgan_yil = serializers.DateField()

    # def validate(self, attrs):
    def validate_ism(self, qiymat):
        if len(qiymat) < 4:
            raise ValidationError("Ism va Familiya bunday kalta bo'lmaydi")
        else:
            return qiymat

    def validate_jins(self, qiymat):
        if qiymat not in ['Erkak', 'Ayol']:
            raise ValidationError("Jins ustuniga xato ma'lumot kiritdinggiz 1")
        else:
            return qiymat


class TarifSerializer(serializers.Serializer):
    nom = serializers.CharField()
    narx = serializers.IntegerField()
    davomiylik = serializers.DurationField()


class KinoSerializer(serializers.ModelSerializer):
    aktyor = AktyorSerializer(many=True)

    class Meta:
        model = Kino
        fields = "__all__"

    def to_representation(self, instance):
        kino = super(KinoSerializer, self).to_representation(instance)
        kino.update({'Akytorlar soni: ': len(kino.get('aktyor'))})
        kino.update({'Izoh soni: ': instance.izoh_set.all().count()})
        return kino


class KinoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kino
        fields = "__all__"


class Izohserializer(serializers.ModelSerializer):
    class Meta:
        model = Izoh
        fields = 'id', 'kino', 'matn', 'baho', 'sana'

    def to_representation(self, instance):
        izoh = super(Izohserializer, self).to_representation(instance)
        izoh.update({'kino': instance.kino.nom})
        izoh.update({'user': instance.user.username})
        return izoh
