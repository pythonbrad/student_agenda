from django.http import JsonResponse


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
        'error': error if not info else info,
    })
