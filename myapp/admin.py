from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string
from .models import Question,Choice,Email,People,PeopleQuestions,EmailToken
from django.core.mail import send_mail
from django.contrib.auth.models import Group,User

class PeopleAvg(admin.ModelAdmin):
    list_display = ('id_test','extraversion','agreeableness','coscientiousness','openness','neuroticism')

class EmailTokenOne(admin.ModelAdmin):
    list_display = ('id_test','mail')

admin.site.register(People,PeopleAvg)

class PeopleQ(admin.ModelAdmin):
    list_display = ('id_test','question','score','cat')

admin.site.register(PeopleQuestions,PeopleQ)

class ChoiceinLine(admin.TabularInline):
    model = Choice
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text','cat')
    fieldsets = [
            (None,{'fields': ['question_text']}),
            ('Categoria', {'fields': ['cat']})
                ]
    inlines = [ChoiceinLine]
admin.site.register(Question, QuestionAdmin)

class Field_mail(admin.TabularInline):
    model = Email

class Send_email(admin.ModelAdmin):
    change_form_template = "admin/change_.html"
    def response_change(self, request, obj):
        if "send-mail" in request.POST:
            #take the emails from text area anc send to people with different token
            email_to_send = request.POST.get('email').split(',')
            print(email_to_send)
            for email in email_to_send:
                id = get_random_string(length=6)
                oggetto = request.POST.get('oggetto')
                text_to_send = request.POST.get('text')
                send_mail(oggetto,
                      text_to_send + id,
                      "michele.dinanni1@gmail.com",
                      recipient_list=[email],
                      fail_silently=False)
                #save the token and the email in EmailToken table
                q = EmailToken(id_test=id,mail=email)
                q.save()
            self.message_user(request, "The email has been sent!")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

admin.site.register(Email,Send_email)
admin.site.register(EmailToken,EmailTokenOne)

#remove Group and User from Admin page
admin.site.unregister(User)
admin.site.unregister(Group)