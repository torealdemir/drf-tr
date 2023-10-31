from rest_framework import serializers
from haber.models import Makale
from datetime import datetime
from datetime import date
from django.utils.timesince import timesince

class MakaleSerializer(serializers.ModelSerializer):
    time_since_pub = serializers.SerializerMethodField()
    class Meta:
        model = Makale
        fields = '__all__'
        read_only_fields = ['id', 'yaratilma_tarihi', 'guncellenme_tarihi']


    def get_time_since_pub(self, object):
        now = datetime.now()
        pub_date = object.yayimlanma_tarihi
        if object.aktif ==True:
            time_delta = timesince(pub_date, now)
            return time_delta
        else:
            return 'Aktif Degil!'
    

def validate_yayimlanma_tarihi(self, tarihdegeri):
    today = date.today()
    if tarihdegeri > today:
        raise serializers.ValidationError('Yayimlanma tarihi ileri bir tarih olamaz!')
    return tarihdegeri

## Standart Serializer
class MakaleDefaultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    yazar = serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    yayimlanma_tarihi = serializers.DateField()
    aktif = serializers.BooleanField()
    yaratilma_tarihi = serializers.DateTimeField(read_only = True)
    guncellenme_tarihi = serializers.DateTimeField(read_only = True)


    def create(self, validated_data):
        print(validated_data)
        return Makale.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.yazar = validated_data.get('yazar', instance.yazar)
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.aciklama = validated_data.get('aciklama', instance.aciklama)
        instance.metin = validated_data.get('metin', instance.metin)
        instance.sehir = validated_data.get('sehir', instance.sehir)
        instance.yayimlanma_tarihi = validated_data.get('yayimlanma_tarihi', instance.yayimlanma_tarihi)
        instance.aktif = validated_data.get('aktif', instance.aktif)
        instance.save()
        return instance
        

    def validate(self, data): # object level
        if data['baslik'] ==  data['aciklama']:
            raise serializers.ValidationError('baslik ve aciklama alanlari ayni olamaz farklilastirin!');
        return data
    
    def validate_baslik(self, value): #
        if len(value)<20:
            raise serializers.ValidationError(f'baslik alani minimum 20 karakter olmali siz {len(value)} karakter girdiniz!')
        return value
