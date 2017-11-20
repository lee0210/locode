
_default_header = {
    'content-type': 'text/html',
}

def get_header(e):
    return e.get('LOCODE_HTTP_HEADER')

def set_header(e, header = _default_header):
    e['LOCODE_HTTP_HEADER'] = header
def set_content(e, content):
    e['LOCODE_HTTP_CONTENT'] = content
def set_status(e, status):
    e['LOCODE_HTTP_STATUS'] = status
