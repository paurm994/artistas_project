import logging

class LogPostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('django.request')

    def __call__(self, request):
        # Aquí puedes registrar la información del POST y la URL
        if request.method == 'POST':
            self.logger.info(f"POST request to {request.path}")
            self.logger.info(f"POST data: {request.POST}")

        # Llamar al siguiente middleware o vista
        response = self.get_response(request)
        return response