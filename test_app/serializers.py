from django.forms import ValidationError
from rest_framework import serializers
from test_app.models import Education, WorkExperience, Skill, Hobby, Portfolio
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = '__all__'

class PortfolioSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True)
    work_experiences = WorkExperienceSerializer(many=True)
    skills = SkillSerializer(many=True)
    hobbies = HobbySerializer(many=True)

    class Meta:
        model = Portfolio
        fields = '__all__'


User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password') 

    def create(self, validated_data):
        password = validated_data.pop('password')
        
        user = User(**validated_data)
        user.set_password(password)  
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        print(f"Email: {email}, Password: {password}")
        user = User.objects.filter(email=email).first()

        user = authenticate(username=user.username, password=password)
        if user is not None:
            print(f"Authentication successful: {user}")
            return user
        else:
            print("Authentication failed: Invalid credentials")
            raise ValidationError('Invalid credentials. Please check your email and password.')
    
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('email', 'username')