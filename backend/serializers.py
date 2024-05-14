from rest_framework import serializers
from .models import Article


# https://www.django-rest-framework.org/tutorial/1-serialization/

# 1
# class ArticleSerializers(serializers.Serializer):
#     title = serializers.CharField(max_length=200)
#     description = serializers.CharField()
#     slug = serializers.SlugField(max_length=250)
#     published = serializers.DateTimeField(read_only=True)
#
#     def create(self, validated_data):
#         return Article.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.slug = validated_data.get('slug', instance.slug)
#         instance.published = validated_data.get('published', instance.published)
#         instance.save()
#         return instance


# 2
class ArticleModelSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = '__all__'

# 3
# class ArticleHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Article
#         fields = ['title', 'description', 'slug', 'published']
