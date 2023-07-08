from django.contrib import admin

from .models import TicketStatus, TicketLabel, Ticket, TicketComment

admin.site.register(TicketStatus)
admin.site.register(TicketLabel)
admin.site.register(Ticket)
admin.site.register(TicketComment)
