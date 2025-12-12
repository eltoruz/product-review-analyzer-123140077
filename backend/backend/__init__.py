from pyramid.config import Configurator
from pyramid.events import NewResponse
from pyramid.response import Response

def add_cors_headers(event):
    response = event.response
    response.headers.update({
        'Access-Control-Allow-Origin': 'http://localhost:3000',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Credentials': 'true'
    })

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    
    # Add CORS subscriber FIRST
    config.add_subscriber(add_cors_headers, NewResponse)
    
    # Scan untuk load semua views
    config.scan()
    
    return config.make_wsgi_app()