from django.contrib import admin
from .models import *

# Register your models here.
# Register AttachmentFile
admin.site.register(IMAP)
admin.site.register(Property)
admin.site.register(Status)
admin.site.register(Customer)
admin.site.register(CustomerMemo)
admin.site.register(MailTemplate)
admin.site.register(Mail)
admin.site.register(MailDomain)