from django.http import JsonResponse
from mega import Mega
import time
import os


CODES = {
    100: 'Method not allow',
    200: '',
    400: 'Unique field violation',
    500: 'Data invalid',
    600: 'Access Denied',
}


def apiResponse(result=None, code=200, info=None):
    error = CODES[int(code / 100) * 100]
    return JsonResponse({
        'result': result,
        'code': code,
        'errors': [error] if not info else info,
    })



class MegaFile:
    """
        This module permit to use a cloud file like a local file
        auth and cloud_folder are optional for downloading
    """
    def __init__(self, auth={}, cloud_folder=None, tmp_folder=None, online_mode=1):
        self.online_mode = online_mode
        if self.online_mode:
            self.mega_api = Mega()
            self.mega_api.login(**auth)
            self.cloud_folder = self.mega_api.find(cloud_folder)[0] if cloud_folder else cloud_folder
        if tmp_folder != None:
            self.tmp_folder = tmp_folder
        else:
            raise ValueError("tmp_folder is required")
        self.packets = []

    def write(self, data):
        if not self.online_mode or self.cloud_folder != None:
            filename = str(time.time())
            tmp_file = open(self.tmp_folder+'/'+filename, 'wb')
            tmp_file.write(data)
            tmp_file.close()
            if self.online_mode:
                cloud_file = self.mega_api.upload(self.tmp_folder+'/'+filename, self.cloud_folder)
                self.packets.append(self.mega_api.get_upload_link(cloud_file))
                os.remove(self.tmp_folder+'/'+filename)
            else:
                self.packets.append(self.tmp_folder+'/'+filename)
        else:
            raise ValueError("cloud_folder is required for this operation")

    def read(self, x=None):
        if self.packets:
            if self.online_mode:
                dest_file = self.mega_api.download_url(self.packets.pop(0), str(self.tmp_folder))
            else:
                dest_file = self.packets.pop(0)
            tmp_file = open(str(dest_file), 'rb')
            data = tmp_file.read()
            tmp_file.close()
            if self.online_mode:
                os.remove(str(dest_file))
            return data
        else:
            return b''

    def close(self):
        pass