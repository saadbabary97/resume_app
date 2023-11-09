from django.contrib import admin
from test_app.models import Portfolio, Education, WorkExperience ,Skill ,Hobby

class PortfolioListAdmin(admin.ModelAdmin):
    list_display = ('user_name','full_name','address','phone_number','email'
               , 'additional_information')
    search_fields = ('user__email',)
    ordering = ()

class EducationAdmin(admin.ModelAdmin):
    list_display = ('id', 'school_name', 'college_name', 'degree')

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'position', 'experience')

class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'skill_name',)

class HobbyAdmin(admin.ModelAdmin):
    list_display = ('id', 'hobby_name',)


admin.site.register(Portfolio, PortfolioListAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Hobby, HobbyAdmin)
# Register your models here.
