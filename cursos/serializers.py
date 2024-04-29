from rest_framework import serializers
from .models import Curso, Avaliacao
from django.db.models import Avg


class AvaliacaoSerializer(serializers.ModelSerializer):

    class Meta:
        extra_kwargs = {
            'email': {'write_only': True}
        }
        model = Avaliacao
        fields = (
            'id',
            'curso',
            'nome',
            'email',
            'comentario',
            'avaliacao',
            'criacao',
            'ativo',
        )

    def validate_avaliacao(self, nota):
        if nota in range(1, 6):
            return nota
        raise serializers.ValidationError('A nota precisa ser entre 1 e 5')


class CursoSerializer(serializers.ModelSerializer):
    # 1 nested relationsip
    # avaliacoes = AvaliacaoSerializer(many=True, read_only=True)

    # 2 hyperlinked related fiel
    # avaliacoes = serializers.HyperlinkedRelatedField(
    #    many=True, read_only=True, view_name='avaliacao-detail')

    # 3 primary key Related field
    avaliacoes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # media avaliacoes
    media_avaliacoes = serializers.SerializerMethodField()

    class Meta:
        model = Curso
        fields = (
            'id',
            'titulo',
            'url',
            'criacao',
            'ativo',
            'avaliacoes',
            'media_avaliacoes'
        )

    def get_media_avaliacoes(self, obj):
        media = obj.avaliacoes.aggregate(
            Avg('avaliacao')).get('avaliacao__avg')
        if media is None:
            return 0
        return round(media * 2)/2
