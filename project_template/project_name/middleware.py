from django.conf import settings

class {{ project_capitalized_name }}Middleware(object):
    def process_request(request):
        request.settings = settings
