from onnxruntime import print_debug_info
import requests
import json

#PROPERTIES = '.telegram_keys'

class TelegramBot():
    def __init__(self, properties_path='./telegram_keys'):
        self._token = None
        self._group = None
        self._channel = None

        with open(properties_path, 'r') as file_reader:
            params = json.load(file_reader)
            self._token = params['token']
            self._group = params['group']
            self._channel = params['channel']

    def get_me(self):
        url = f"https://api.telegram.org/bot{self._token}/getMe"
        response = requests.get(url)

        if response.status_code == 200:
            salida = json.loads(response.text)
            return salida
        return None

    def get_updates(self):
        url = f"https://api.telegram.org/bot{self._token}/getUpdates"
        print(url)
        response = requests.get(url)

        if response.status_code == 200:
            salida = json.loads(response.text)
            return salida
        return None
    
    def send_message(self, chat_id, message):
        url = f"https://api.telegram.org/bot{self._token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        response = requests.post(url, data)

        if response.status_code == 200:
            salida = json.loads(response.text)
            return salida
        msg = f"Error code: {response.status_code}. Description: {response.text}"
        return Exception(msg)
    
    def send_message_to_group(self, message):
        try:
            return self.send_message(self._group, message)
        except Exception as e:
            print(e)
        return None
    
    def send_message_to_channel(self, message):
        try:
            print('ha sido llamada la funcion de enviar')
            return self.send_message(self._channel, message)
        except Exception as e:
            print(e)
        return None
    
    def send_photo(self, chat_id, filename, caption):
        url = f"https://api.telegram.org/bot{self._token}/sendPhoto"
        data = {"chat_id": chat_id, "caption": caption}
        files = {"photo": (filename, open(filename, 'rb'))}
        response = requests.post(url, data=data, files=files)

        if response.status_code == 200:
            salida = json.loads(response.text)
            return salida
        
        error = json.loads(response.text)
        error_code = error['error_code']
        description = error['description']
        msg = f"Error: {error_code}. Description: {description}"
        return Exception(msg)
    
    def send_photo_to_group(self, filename, caption):
        try:
            return self.send_photo(self._group, filename, caption)
        except Exception as e:
            print(e)
        return None

    def send_photo_to_channel(self, filename, caption):
        try:
            return self.send_photo(self._channel, filename, caption)
        except Exception as e:
            print(e)
        return None

    def test(self):
        print('Success')
