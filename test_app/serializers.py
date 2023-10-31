from rest_framework import serializers
from test_app.models import Education, WorkExperience, Skill, Hobby, Portfolio

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
