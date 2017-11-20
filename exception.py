import .http

def handle(e):
    http.set_header(e)
    http.set_status(e, '502 ')
    http.set_content(e, 'Oops, Service Unavailable')
