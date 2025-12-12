# myproject/cors.py

def add_cors_headers(request, response):
    response.headers.update({
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS, PUT, DELETE",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    })
    return response


def cors_tween_factory(handler, registry):
    def cors_tween(request):
        # OPTIONS method for preflight
        if request.method == "OPTIONS":
            response = Response()
            add_cors_headers(request, response)
            return response

        response = handler(request)
        add_cors_headers(request, response)
        return response

    return cors_tween
