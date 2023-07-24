from django.utils import timezone
from datetime import datetime
from .utils import find_string_between_substrings


class NewCommentSessionCleaner:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # delete attachments if navigate away of ticket page
        if "tickets/in/" not in request.get_full_path():
            if "attachments" in request.session:
                del request.session["attachments"]
        # delete attachments if more than 10 minutes since uploaded
        # TODO:
        ## add created_at to models, and check time delta with database records
        ## use timezone aware approach
        else:
            if "attachments" in request.session:
                date_format = "%Y-%m-%d %H:%M:%S"
                attachments = request.session["attachments"]
                for ticket_id in attachments:
                    attachment_index = 0
                    for attachment in attachments[ticket_id]:
                        created_at = datetime.strptime(attachment["created"], date_format)
                        now = datetime.now()
                        minutes_since_creation = (now - created_at).total_seconds() / 60
                        if minutes_since_creation > 10:
                            del attachments[ticket_id][attachment_index]
                    attachment_index += 1
                request.session["attachments"] = attachments

        response = self.get_response(request)

        return response
