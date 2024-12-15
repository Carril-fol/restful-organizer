from asgiref.wsgi import WsgiToAsgi
import uvicorn

def start_server(app_wsgi):
    app_asgi = WsgiToAsgi(app_wsgi)
    uvicorn.run(app_asgi, host="0.0.0.0", port=8000)