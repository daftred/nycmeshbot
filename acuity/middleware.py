from django.conf import settings

class AcuityMiddleware(object):
    def process_request(request):
        print("process_request: {}".format(request))
        return None

    def process_view(request, view_func, view_args, view_kwargs):
        return None

    def process_template_response(request, response):
        print("process_template_response - request: {}".format(request))
        print("process_template_response - response: {}".format(response))
        return None

    def process_response(request, response):
        print("process_response - request: {}".format(request))
        print("process_response - response: {}".format(response))
        return None
