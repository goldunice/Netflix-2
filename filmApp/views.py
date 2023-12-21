from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class HelloAPI(APIView):
    def get(self, request):
        d = {
            'xabar': 'Salom Dunyo',
            'izoh': 'Test uchun API yozdik'
        }
        return Response(d)

    def post(self, request):
        d = request.data
        natija = {
            'xabar': 'POST qabul qilindi',
            'post malumoti': d
        }
        return Response(natija)


class AktyorlarAPI(APIView):
    def get(self, request):
        aktyorlar = Aktyor.objects.all()
        soz = request.query_params.get('ismi')
        davlati = request.query_params.get('davlati')
        tartib = request.query_params.get('order')
        if soz:
            aktyorlar = aktyorlar.filter(ism__contains=soz)
        if davlati:
            aktyorlar = aktyorlar.filter(davlat__contains=davlati)
        if tartib:
            aktyorlar = aktyorlar.order_by(tartib)
        serializer = AktyorSerializer(aktyorlar, many=True)
        return Response(serializer.data)

    def post(self, request):
        aktyor = request.data
        serializer = AktyorSerializer(data=aktyor)
        if serializer.is_valid():
            d = serializer.validated_data
            Aktyor.objects.create(
                ism=d.get('ism'),
                davlat=d.get('davlat'),
                jins=d.get('jins'),
                tugilgan_yil=d.get('tugilgan_yil')
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class AktyorAPI(APIView):
    def get(self, request, pk):
        aktyor = Aktyor.objects.get(id=pk)
        serializer = AktyorSerializer(aktyor)
        return Response(serializer.data)

    def update(self, request, pk):
        aktyor = Aktyor.objects.get(id=pk)
        serializer = AktyorSerializer(aktyor, data=request.data)
        if serializer.is_valid():
            d = serializer.validated_data
            Aktyor.objects.filter(id=pk).update(
                ism=d.get('ism'),
                davlat=d.get('davlat'),
                jins=d.get('jins'),
                tugilgan_yil=d.get('tugilgan_yil')
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class TariflarAPI(APIView):
    def get(self, request):
        tariflar = Tarif.objects.all()
        serializer = TarifSerializer(tariflar, many=True)
        return Response(serializer.data)

    def post(self, request):
        tarif = request.data
        serializer = TarifSerializer(data=tarif)
        if serializer.is_valid():
            data = serializer.validated_data
            Tarif.objects.create(
                nom=data.get('nom'),
                narx=data.get('narx'),
                davomiylik=data.get('davomiylik')
            )
            return Response(serializer.data)
        return Response(serializer.errors)


class TarifOchirAPI(APIView):
    def get(self, request, pk):
        d = Tarif.objects.get(id=pk)
        serializer = TarifSerializer(d)
        d.delete()
        return Response(serializer.data)


class TarifUpdateAPI(APIView):
    def get(self, request, pk):
        tarif = Tarif.objects.get(id=pk)
        serializer = TarifSerializer(tarif)
        return Response(serializer.data)

    def put(self, request, pk):
        tarif = Tarif.objects.get(id=pk)
        serializer = TarifSerializer(tarif, data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            Tarif.objects.filter(id=pk).update(
                nom=data.get('nom'),
                narx=data.get('narx'),
                davomiylik=data.get('davomiylik')
            )
            return Response(serializer.data)
        return Response(serializer.errors)


class KinolarModelViewSet(ModelViewSet):
    queryset = Kino.objects.all()
    serializer_class = KinoPostSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2

    # def list(self, request, *args, **kwargs):
    #     kinolar = self.queryset
    #     serializer = KinoSerializer(kinolar, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        kino = self.get_object()
        serializer = KinoSerializer(kino)
        return Response(serializer.data)

    @action(detail=True)
    def izohlar(self, request, pk):
        kino = self.get_object()
        kino_izohlar = kino.izoh_set.all()
        serializer = Izohserializer(kino_izohlar, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def aktyorlar(self, request, pk):
        kino = self.get_object()
        kino_aktyorlar = kino.aktyor.all()
        serializer = AktyorSerializer(kino_aktyorlar, many=True)
        return Response(serializer.data)


class KinolarAPI(APIView):
    def get(self, request):
        kinolar = Kino.objects.all()
        serializer = KinoSerializer(kinolar, many=True)
        return Response(serializer.data)

    def post(self, request):
        kino = request.data
        serializer = KinoPostSerializer(data=kino)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class KinoAPI(APIView):
    def get(self, request, pk):
        kino = Kino.objects.get(id=pk)
        serializer = KinoSerializer(kino)
        return Response(serializer.data)

    def delete(self, request, pk):
        kino = Kino.objects.get(id=pk)
        serializer = KinoSerializer(kino)
        kino.delete()
        return Response(serializer.data)


class IzohModelViewSet(ModelViewSet):
    serializer_class = Izohserializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Izoh.objects.all()
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

    def get_queryset(self):
        izohlar = self.queryset
        soz = self.request.query_params.get('tartiblash')
        if soz:
            izohlar = izohlar.order_by('sana')
        return izohlar.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return status.HTTP_201_CREATED

    # def create(self, request, *args, **kwargs): ---> post
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #     return serializer

    # def retrieve(self, request, *args, **kwargs):
    #     izoh = self.get_object()
    #     if izoh.baho < 5:
    #         return Response()
    #     else:
    #         return Response()

    # def destroy(self, request, *args, **kwargs):
    #    pass


class AktyorModelViewSet(ModelViewSet):
    queryset = Aktyor.objects.all()
    serializer_class = AktyorSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['id', 'ism', 'tugilgan_yil']  # ?ordering=
    search_fields = ['id', 'ism', 'davlat']  # ?search=
    pagination_class = PageNumberPagination
    pagination_class.page_size = 3

    def get_queryset(self):
        aktyorlar = self.queryset
        gender = self.request.query_params.get('jins')
        if gender:
            aktyorlar = aktyorlar.filter(jins__contains=gender)
        return aktyorlar
