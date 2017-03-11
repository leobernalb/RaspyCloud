import cherrypy
from jsonrpc2 import JsonRpc

cherrypy.config.update({'server.socket_port': 8081})
cherrypy.engine.restart()

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"


if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())