#!/usr/bin/env python
#
# Simple HTTP server that also provides a way to update its contents with that
# of some publicly-accessible ZIP file hosted on Dropbox or Google Drive.
#
# Author: me@olegvaskevich.com (Oleg Vaskevich)

import os
import shutil
import SocketServer
import traceback
from SimpleHTTPServer import SimpleHTTPRequestHandler
from StringIO import StringIO
from urllib import urlopen
from zipfile import ZipFile

PORT = int(os.getenv('APP_PORT', '80'))
STORE_PATH = os.getenv('APP_STORE_PATH', '/var/www')
RELOAD_URL = os.getenv('APP_RELOAD_PATH', '/reload_now')
ARCHIVE_URL = os.getenv('APP_ARCHIVE_URL', None)

class CloudZipProxyHost(SimpleHTTPRequestHandler):
    def __init__(self, req, client_addr, server):
        SimpleHTTPRequestHandler.__init__(self, req, client_addr, server)
        self.extensions_map[''] = 'text/plain'

    def clearDirContents(self, path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            for child in os.listdir(path):
                childPath = os.path.join(path, child)
                if os.path.isfile(childPath):
                    os.remove(childPath)
                elif os.path.isdir(childPath):
                    shutil.rmtree(childPath)

    def reloadFromDrive(self):
        if not ARCHIVE_URL:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(('<html><body><p><b>Please set the <code> '
                              '<code>ARCHIVE_URL</code> environment'
                              'variable.'))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            try:
                # Download ZIP.
                self.wfile.write(('<html><body><ul><li><b>Downloading ZIP file'
                                  '...</b></li>'))
                zipfile = ZipFile(StringIO(urlopen(ARCHIVE_URL).read()))

                # Clear out directory.
                self.wfile.write('<li><b>Clearing directory...</b></li>')
                self.clearDirContents(STORE_PATH)

                # Extract all the files in it.
                self.wfile.write('<li><b>Extracting ZIP...</b></li>')
                for file in zipfile.namelist():
                    self.wfile.write('<li>Extracting %s</li>' % file)
                    zipfile.extract(file, STORE_PATH)
            except:
                self.wfile.write(('<li><b>Error:</b><pre><code>%s</code></pre>'
                                  '</li>') \
                    % traceback.format_exc())
            else:
                self.wfile.write('<li><a href="/"><b><i>Done!</i></b></a></li>')

            self.wfile.write('</ul></body></html>')

    def do_GET(self):
        if self.path == RELOAD_URL:
            print 'Reloading...'
            self.reloadFromDrive()
        else:
            SimpleHTTPRequestHandler.do_GET(self)
        

if __name__ == '__main__':
    os.chdir(STORE_PATH)
    httpd = SocketServer.TCPServer(('', PORT), CloudZipProxyHost)
    print 'SimpleFileDrop is running on port %d. Use \'%s\' to reload.' \
        % (PORT, RELOAD_URL)
    httpd.serve_forever()

