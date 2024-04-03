from rest_framework import serializers
from .models import Studio, Genre, Movie
from user.serializers import DirectorSerializer
from user.models import Director


class StudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Studio
        fields = '__all__'



# class StudioSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField()
#     updated = serializers.DateField(read_only=True)
#     created = serializers.DateField(read_only=True)

#     def create(self, validated_data):
#         studio = Studio.objects.create(**validated_data)
#         return studio
    
#     def update(self, instance, validated_data):
#         instance.title = validated_data['title']
#         instance.save()
#         return instance



class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'
        # fields = ['id', 'title', 'updated']
        # exclude = ['updated']



class MovieSerializer(serializers.ModelSerializer):
    director_info = DirectorSerializer(source="director", read_only=True)
    studio = serializers.CharField(source='director.studio.title', read_only=True)
    # director = serializers.PrimaryKeyRelatedField(queryset=Director.objects.all(), write_only=True)
    genres_info = GenreSerializer(many=True, source='genres', read_only=True)
    class Meta:
        model = Movie
        exclude = ['director']
        extra_kwargs = {
            'genres': {'write_only': True},
        }

    def validate_title(self, value):
        if not value.istitle():
            raise serializers.ValidationError('Title must be capitalized')
        return value
    
    def validate(self, data):
        if "title" in data and "description" in data and data['title'].lower() in data['description'].lower():
            raise serializers.ValidationError("Title can't be used in description")
        return data
    
    def create(self, validated_data):
        director = self.context['request'].user.director
        genres = validated_data.pop('genres')
        movie = Movie.objects.create(director=director, **validated_data)
        movie.genres.set(genres)
        movie.save() 
        return movie