from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import TicketCommentFile
from .models import TicketComment
from datetime import timedelta


@receiver(post_save, sender=TicketComment)
def callback_comment_created(sender, **kwargs):
    """Receiver function to execute operations when a comment record is created

    If orphan file records present in database (created more than ten minutes ago,
    and with NULL in the comment column, so not linkied to a specific comment),
    they will be deleted.
    """
    ten_minutes_ago = timezone.now() - timedelta(minutes=10)
    orphan_files = TicketCommentFile.objects.filter(comment=None).filter(created__lte=ten_minutes_ago)
    orphan_files.delete()
    print("The script would erase", orphan_files)
