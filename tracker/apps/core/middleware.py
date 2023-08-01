from django.utils import timezone
from datetime import timedelta
from .utils import find_string_between_substrings
from tracker.apps.core.models import TicketCommentFile


class NewCommentSessionCleaner:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # delete attachment session variables if navigate away of ticket page
        full_path = request.get_full_path()
        if "tickets/in/" not in full_path:
            if "attachments" in request.session:
                del request.session["attachments"]
        # delete attachment session variables if more than 10 minutes since uploaded
        else:
            if "attachments" in request.session:
                ticket_id = find_string_between_substrings(full_path, "tickets/in/", "/")
                attachments = request.session["attachments"]
                if ticket_id in attachments:
                    ten_minutes_ago = timezone.now() - timedelta(minutes=10)
                    attachment_index = 0
                    for attachment in attachments[ticket_id]:
                        file = TicketCommentFile.objects.get(id=attachment["id"])
                        if file.created < ten_minutes_ago:
                            del attachments[ticket_id][attachment_index]
                        attachment_index += 1
                    request.session["attachments"] = attachments

        response = self.get_response(request)

        return response
