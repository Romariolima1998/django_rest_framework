# from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
from rest_framework import generics
from .models import Curso, Avaliacao
from .serializers import CursoSerializer, AvaliacaoSerializer
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework import permissions
from .permissions import EhSuperUsuario


# class CursoAPIView(APIView):

#     def get(self, request):
#         curso = Curso.objects.all()
#         serializer = CursoSerializer(curso, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CursoSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response({'msg': 'Criado com sucesso'}, status=status.HTTP_201_CREATED)


# class AvaliacaoAPIView(APIView):

#     def get(self, request):
#         avaliacao = Avaliacao.objects.all()
#         serializer = AvaliacaoSerializer(avaliacao, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = AvaliacaoSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# -----------------------generics view------------------------------------
# ==================== api v1===========================================
class CursosAPIView(generics.ListCreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class CursoAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class AvaliacoesAPIView(generics.ListCreateAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

    def get_queryset(self):
        if self.kwargs.get('curso_pk'):
            return self.queryset.filter(curso_id=self.kwargs.get('curso_pk'))
        return super().get_queryset()


class AvaliacaoAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

    def get_object(self):
        if self.kwargs.get('curso_pk'):
            print('cheguei aki')
            return get_object_or_404(
                self.get_queryset(),
                curso_id=self.kwargs.get('curso_pk'),
                pk=self.kwargs.get('avaliacao_pk')
            )
        return super().get_object()


# ===================== api v2 ==========================================

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    # PERMISSIONS
    # permission_classes = (permissions.DjangoModelPermissions)
    permission_classes = (EhSuperUsuario, permissions.DjangoModelPermissions)

    @action(detail=True, methods=['get'])
    def avaliacoes(self, request, pk=None):
        self.pagination_class.page_size = 1
        avaliacoes = Avaliacao.objects.filter(curso_id=pk)
        page = self.paginate_queryset(avaliacoes)

        if page is not None:
            serializer = AvaliacaoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AvaliacaoSerializer(avaliacoes.all(), many=True)
        return Response(serializer.data)


''' Viewset padao
class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
'''

# ViewSet customizada


class AvaliacaoViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
