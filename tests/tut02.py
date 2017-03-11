import random
import string

import cherrypy


class StringGenerator(object):

    @cherrypy.expose
    def generate(self):
        return ''.join(random.sample(string.hexdigits, 8))


    @cherrypy.expose
    def index(self):
        return "Hello world!"



if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator())