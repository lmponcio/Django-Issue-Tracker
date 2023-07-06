from django.contrib import admin

from .models import TicketStatus, Ticket, TicketComment

admin.site.register(TicketStatus)
admin.site.register(Ticket)
admin.site.register(TicketComment)
