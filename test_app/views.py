from django.shortcuts import render
from test_app.serializers import PortfolioSerializer, EducationSerializer, SkillSerializer, HobbySerializer, WorkExperienceSerializer
from test_app.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
def portfolio_detail(request, portfolio_id):
    try:
        obj = Portfolio.objects.get(id=portfolio_id)
    except Portfolio.DoesNotExist:
        return Response({'error': 'Portfolio not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PortfolioSerializer(obj)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_portfolio(request):
    serializer = PortfolioSerializer(data=request.data)
    if serializer.is_valid():
        portfolio_instance = serializer.save()
        educations_data = request.data.get('educations', [])
        work_experiences_data = request.data.get('work_experiences', [])
        skills_data = request.data.get('skills', [])
        hobbies_data = request.data.get('hobbies', [])

        for education_data in educations_data:
            education_data['portfolio'] = portfolio_instance  
            education_serializer = EducationSerializer(data=education_data)
            if education_serializer.is_valid():
                education_serializer.save()

        for work_experience_data in work_experiences_data:
            work_experience_data['portfolio'] = portfolio_instance
            work_experience_serializer = WorkExperienceSerializer(data=work_experience_data)
            if work_experience_serializer.is_valid():
                work_experience_serializer.save()

        for skill_data in skills_data:
            skill_data['portfolio'] = portfolio_instance
            skill_serializer = SkillSerializer(data=skill_data)
            if skill_serializer.is_valid():
                skill_serializer.save()

        for hobby_data in hobbies_data:
            hobby_data['portfolio'] = portfolio_instance
            hobby_serializer = HobbySerializer(data=hobby_data)
            if hobby_serializer.is_valid():
                hobby_serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_portfolio(request, portfolio_id):
    portfolio = Portfolio.objects.get(id=portfolio_id)
    serializer = PortfolioSerializer(portfolio, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#post for education
@api_view(['POST'])
@permission_classes([AllowAny])
def create_education(request):
    username = request.data.get('username') 
    try:
        user = Portfolio.objects.get(user_name=username)
        print('<><<><>',user)
    except Portfolio.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = EducationSerializer(data=request.data)
    if serializer.is_valid():
        education = serializer.save()
        user.educations.add(education)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_education(request, id):
    education_id = request.data.get('id') 
    try:
        education = Education.objects.get(id=education_id)
    except Education.DoesNotExist:
        return Response({'error': 'Education not found.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = EducationSerializer(education, data=request.data, partial=True) 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_education(request, id):
    try:
        education = Education.objects.get(id=id)
        education.delete()
    except Education.DoesNotExist:
        return Response({'error': 'Education entry not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'message': 'Education entry deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


#post of skill
@api_view(['POST'])
@permission_classes([AllowAny])
def create_skill(request):
    username = request.data.get('username') 
    try:
        user = Portfolio.objects.get(user_name=username)
        print('<><<><>',user)
    except Portfolio.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = SkillSerializer(data=request.data)
    if serializer.is_valid():
        skill = serializer.save()
        user.skills.add(skill)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_skill(request, id):
    skill_id = request.data.get('id') 
    try:
        skill = Skill.objects.get(id=skill_id)
    except Skill.DoesNotExist:
        return Response({'error': 'Skill not found.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = SkillSerializer(skill, data=request.data, partial=True) 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_skill(request, id):
    try:
        skill = Skill.objects.get(id=id)
        skill.delete()  
    except Skill.DoesNotExist:
        return Response({'error': 'Skill entry not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'message': 'Skill entry deleted successfully'}, status=status.HTTP_200_OK)



#post for Hobby

@api_view(['POST'])
@permission_classes([AllowAny])
def create_hobby(request):
    username = request.data.get('username') 
    try:
        user = Portfolio.objects.get(user_name=username)
    except Portfolio.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = HobbySerializer(data=request.data)
    if serializer.is_valid():
        hobby = serializer.save()
        user.hobbies.add(hobby)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_hobby(request, id):
    hobby_id = request.data.get('id') 
    try:
        hobby = Hobby.objects.get(id=hobby_id)
    except Hobby.DoesNotExist:
        return Response({'error': 'Hobby not found.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = HobbySerializer(hobby, data=request.data, partial=True) 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_hobby(request, id):
    try:
        hobby = Hobby.objects.get(id=id)
        hobby.delete()
    except Hobby.DoesNotExist:
        return Response({'error': 'Hobby entry not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'message': 'Hobby entry deleted successfully'}, status=status.HTTP_200_OK)


#post for Experience

@api_view(['POST'])
@permission_classes([AllowAny])
def create_experience(request):
    username = request.data.get('username', None)
    try:
        user = Portfolio.objects.get(user_name=username) 
    except:
        return Response({'error':'User not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = WorkExperienceSerializer(data = request.data)
    if serializer.is_valid():
        experience = serializer.save()
        user.work_experiences.add(experience)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_experience(request, id):
    experience_id = request.data.get('id') 
    try:
        experience = WorkExperience.objects.get(id=experience_id)
    except WorkExperience.DoesNotExist:
        return Response({'error': 'Experience not found.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = WorkExperienceSerializer(experience, data=request.data, partial=True) 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_experience(request, id):
    try:
        experience = WorkExperience.objects.get(id=id)
        experience.delete()
    except WorkExperience.DoesNotExist:
        return Response({'error': 'WorkExperience entry not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'message': 'WorkExperience entry deleted successfully'}, status=status.HTTP_200_OK)