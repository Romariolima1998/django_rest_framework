from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register('cursos', views.CursoViewSet)
router.register('avaliacoes', views.AvaliacaoViewSet)

urlpatterns = [
    path('cursos/', views.CursosAPIView.as_view(), name='cursos'),
    path('cursos/<int:pk>/', views.CursoAPIView.as_view(), name='curso'),

    path('cursos/<int:curso_pk>/avaliacoes/',
         views.AvaliacoesAPIView.as_view(), name='curso_avaliaçoes'),

    path('cursos/<int:curso_pk>/avaliacoes/<int:avaliacao_pk>/',
         views.AvaliacaoAPIView.as_view(), name='curso_avaliaçao'),

    path('avaliacoes/', views.AvaliacoesAPIView.as_view(), name='avaliacoes'),

    path(
        'avaliacoes/<int:pk>/',
        views.AvaliacaoAPIView.as_view(), name='avaliacao')
]
