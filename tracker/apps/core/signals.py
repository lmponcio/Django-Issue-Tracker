from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import TicketCommentFile, TicketComment, Ticket
from datetime import timedelta


@receiver(post_save, sender=TicketComment)
def callback_comment_created(sender, **kwargs):
    """Receiver function to execute operations after a comment record is created

    If orphan file records present in database (created more than ten minutes ago,
    and with NULL in the comment column, so not linkied to a specific comment),
    they will be deleted.
    """
    ten_minutes_ago = timezone.now() - timedelta(minutes=10)
    orphan_files = TicketCommentFile.objects.filter(comment=None).filter(created__lte=ten_minutes_ago)
    orphan_files.delete()


@receiver(pre_save, sender=Ticket)
def callback_ticket_created(sender, **kwargs):
    """Receiver function to execute operations before a ticket record is created

    If status is changing from open to closed, the close date is set to now
    """
    ticket_instance = kwargs["instance"]
    if ticket_instance.id:  # ticket already in database
        ticket_db = Ticket.objects.get(id=ticket_instance.id)
        if ticket_instance.status.__str__() == "Closed" and ticket_db.status.__str__() == "Open":
            kwargs["instance"].close_date = timezone.now()  # modifying instance to be saved
