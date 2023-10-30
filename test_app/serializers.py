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

    # def create(self, validated_data):
    #     educations_data = validated_data.pop('educations')
    #     work_experiences_data = validated_data.pop('work_experiences')
    #     skills_data = validated_data.pop('skills')
    #     hobbies_data = validated_data.pop('hobbies')

    #     portfolio = Portfolio.objects.create(**validated_data)

    #     for education_data in educations_data:
    #         Education.objects.create(portfolio=portfolio, **education_data)

    #     for work_experience_data in work_experiences_data:
    #         WorkExperience.objects.create(portfolio=portfolio, **work_experience_data)

    #     for skill_data in skills_data:
    #         Skill.objects.create(portfolio=portfolio, **skill_data)

    #     for hobby_data in hobbies_data:
    #         Hobby.objects.create(portfolio=portfolio, **hobby_data)

    #     return portfolio
