import xml.sax

class xml_handler(xml.sax.ContentHandler):
    def __init__(self):
        self.rt = {}
    def startElement(self, tag, attr):
        self.current_tag = tag 
        self.rt[tag] = ''
    def endElement(self, tag):
        self.current_tag = None
    def characters(self, content):
        if self.current_tag is not None:
            self.rt[self.current_tag] += content
    @property
    def result(self):
        return self.rt

def parse_xml(xml_text, charset='utf-8'):
    if isinstance(xml_text, (bytes, bytearray)):
        xml_text = xml_text.decode(charset)
    handler = xml_handler()
    xml.sax.parseString(xml_text, handler)
    return handler.result

class simple_xml(object):
    def __init__(self):
        self.root = 'xml'
        self.tags = {}
    def root(self, root):
        self.root = root
        return self
    def add_tag(self, tag, content, CDATA = True):
        if CDATA:
            content = '<![CDATA[%s]]>' % content
        self.tags[tag] = content
        return self
    @property
    def text(self):
        return '<{root}>{content}</{root}>'.format(root = self.root, content = ''.join(['<{tag}>{content}</{tag}>'.format(tag = k, content = v) for k, v in self.tags.items()]))

if __name__ == '__main__':
    xml = simple_xml().add_tag('ToUserName', 'Test To User Name') \
                      .add_tag('FromUserName', '测试').text
    print(xml)
