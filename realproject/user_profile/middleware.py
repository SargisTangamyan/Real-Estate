class LogRequestFilesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the files in the request
        if request.method == 'POST' and request.FILES:
            for filename, file in request.FILES.items():
                print(f"File uploaded: {filename}, Size: {file.size} bytes")

        response = self.get_response(request)
        return response