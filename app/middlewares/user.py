class ProfileMiddleware:
    def process_request(self, request):
        print('username: ', request.user.username)
        print('method: ', request.method)