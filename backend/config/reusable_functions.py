from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# filter null value from the dictionary
def cleanNullTerms(d):
    if isinstance(d, dict):
        return {
            k: v 
            for k, v in ((k, cleanNullTerms(v)) for k, v in d.items())
            if v
        }
    if isinstance(d, list):
        return [v for v in map(cleanNullTerms, d) if v]
    return d

# generic format for 4xx errors
def errorCode(code, title, detail):
    error = {
            "errors": [
                {
                    "code": "urn:au-cds:error:cds-all:" + code,
                    "title": title,
                    "detail": detail,
                    "meta": {}
                }
            ]
        }
    return error

# handle all combination of headers error
def checkHeaderError(request):
    headerXV = request.headers.get('x-v')
    if 'x-v' not in request.headers:
        errorResponse = errorCode('Header/Missing', 'Missing Required Header', 'x-v')
        return Response(errorResponse, status=status.HTTP_400_BAD_REQUEST)
    elif headerXV == "" or headerXV.isdigit() == False:
        errorResponse = errorCode('Header/InvalidVersion', 'Invalid Version', 'Invalid x-v Requested')
        return Response(errorResponse, status=status.HTTP_400_BAD_REQUEST)
    elif headerXV != "3":
        errorResponse = errorCode('Header/UnsupportedVersion', 'Unsupported Version', 'Requested x-v version is not supported')
        return Response(errorResponse, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return False

# handle 404 not found for invalid urls
@api_view()
def resourceNotFoundError(request):
    errorResponse = errorCode('Resource/NotFound', 'Resource Not Found', 'Requested resource is not available in the specification. No matching resource found for given API Request')
    return Response(errorResponse, status=status.HTTP_404_NOT_FOUND)