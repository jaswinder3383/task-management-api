
class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Debug information
        print(f"Request Method: {request.method}")
        print(f"Request Headers: {request.headers}")
        print(f"Authorization Header: {request.META.get('HTTP_AUTHORIZATION')}")
        print(f"User: {request.user}")

        response = self.get_response(request)
        return response
