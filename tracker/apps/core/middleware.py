from .utils import find_string_between_substrings


class NewCommentSessionCleaner:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "tickets/in/" not in request.get_full_path():
            if "attachments" in request.session:
                del request.session["attachments"]

        response = self.get_response(request)

        return response
