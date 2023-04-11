from rest_framework import serializers
from  watchlist_app.models import WatchList,StreamPlatform,Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('watchlist',)
        #fields = '__all__'


class WatchListSerializer(serializers.ModelSerializer):
    #reviews = ReviewSerializer(many=True,read_only=True)
    platform = serializers.CharField(source = 'platform.name')
    class Meta:
        model = WatchList
        fields = '__all__'


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True,read_only=True)
    #watchlist = serializers.StringRelatedField(many=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'

# class MovieSerializer(serializers.ModelSerializer):
#     len_name = serializers.SerializerMethodField()
#     class Meta:
#         model = WatchList
#         fields = '__all__'
        #exclude = ['description']   
        #if we exclude this,it wont show this field in browsable api,(serialization)
        #and also it won't populate this field in databas.(deserialization)

    # def get_len_name(self,obj):
    #     return len(obj.name)

    # def validate_name(self,value):
    #     if Movie.objects.filter(name=value).exists():
    #         raise serializers.ValidationError(f'Movie with name {value} already exists')
    #     return value
    
    # def validate(self,data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError('Movie name and description cannot be the same')
    #     return data



# def description_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError('Description is too short!')


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField(validators=[description_length])
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         print(f'hit create in serializer')
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name',instance.name)
#         instance.description = validated_data.get('description',instance.description)
#         instance.active = validated_data.get('active',instance.active)
#         instance.save()
#         return instance
    
#     def validate_name(self,value):
#         if Movie.objects.filter(name=value).exists():
#             raise serializers.ValidationError(f'Movie with name {value} already exists')
#         return value
    
#     def validate(self,data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError('Movie name and description cannot be the same')
#         return data
    

    

    
