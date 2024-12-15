# In middleware.py
import base64
from cryptography.fernet import Fernet
from django.utils.deprecation import MiddlewareMixin

class EncryptionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def process_request(self, request):
        if request.method == 'POST' and 'content' in request.POST:
            encrypted_message = self.cipher_suite.encrypt(request.POST['content'].encode('utf-8'))
            request.POST['content'] = base64.urlsafe_b64encode(encrypted_message).decode('utf-8')

    def process_response(self, request, response):
        if response.status_code == 200 and 'content' in response.content.decode('utf-8'):
            decrypted_message = self.cipher_suite.decrypt(base64.urlsafe_b64decode(response.content.decode('utf-8')))
            response.content = decrypted_message.decode('utf-8')
        return response
