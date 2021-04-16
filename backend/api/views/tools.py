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
        THis module permit to use a cloud file like a local file
    """
    def __init__(self, auth, cloud_folder, tmp_folder, name=None):
        self.mega_api = Mega()
        self.mega_api.login(**auth)
        self.cloud_folder = self.mega_api.find(cloud_folder)[0]
        self.tmp_folder = tmp_folder
        self.packets = []
        self.name = name

    def write(self, data):
        filename = str(time.time())
        tmp_file = open(self.tmp_folder+'/'+filename, 'wb')
        tmp_file.write(data)
        tmp_file.close()
        cloud_file = self.mega_api.upload(self.tmp_folder+'/'+filename, self.cloud_folder)
        self.packets.append(self.mega_api.get_upload_link(cloud_file))
        os.remove(self.tmp_folder+'/'+filename)

    def read(self, x=None):
        if self.packets:
            dest_file = self.mega_api.download_url(self.packets.pop(0), str(self.tmp_folder))
            tmp_file = open(str(dest_file), 'rb')
            data = tmp_file.read()
            tmp_file.close()
            os.remove(str(dest_file))
            return data
        else:
            return b''

    def close(self):
        pass