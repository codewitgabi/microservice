from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.urls import path
from ninja import NinjaAPI
import requests

api = NinjaAPI()

# services

services = {
    "user": "http://localhost:8001",
    "product": "http://localhost:8002",
}


def reverse_proxy(request: HttpRequest, service, path):
    if service not in services:
        raise Http404()

    target_url = f"{services[service]}/{path}"
    method = request.method
    headers = dict(request.headers)
    files = request.FILES
    data = request.body

    response = requests.request(
        method, target_url, headers=headers, data=data, files=files
    )
    return HttpResponse(
        response.content,
        status=response.status_code,
        content_type=response.headers.get("Content-Type"),
    )


@api.api_operation(
    ["GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS", "HEAD"],
    "/{service}/api/{path:path}",
)
def gateway(request: HttpRequest, service, path) -> HttpResponse:
    return reverse_proxy(request, service, path)
