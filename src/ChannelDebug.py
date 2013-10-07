import urllib2
import json
from urllib2 import Request
import inspect

class ChannelDebug:

    def __init__(self, url, port, channel):
        self.url = "%s:%s/%s" % (url, port, channel)

    def call(self, *args, **kwargs): return self.log(*args, **kwargs)

    def log(self, object):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': "Mozilla/5.0"
        }
        result = self.wrap(self.normalize(object))
        jsonCode = json.dumps(result)
        req = Request(self.url, jsonCode)
        map(lambda (x,y): req.add_header(x,y), headers.items())
        response = urllib2.urlopen(req)
        responseText = response.read()
        try:
            return json.loads(responseText)
        except Exception:
            return responseText

    def wrap(self, object):
        self.stackTrace()
        return {
            "handler": "object",
            "args": [ object],
            "stacktrace": self.stackTrace()
        }

    def stackTrace(self):
        return []

    def normalize(self, object):
        if hasattr(object, '__dict__'):
            return {
                "class": map(lambda x: x.__module__ + "." + x.__name__, self.buildClassChain(object.__class__)),
                "properties": self.buildProperties(object),
                "methods": self.buildMethods(object),
                "static": self.buildStaticProperties(object),
                "constants": []
            }
        else:
            return {"scalar": object}

    def buildClassChain(self, clazz):
        if clazz == object.__class__: return [clazz]

        results = [clazz]
        for base in clazz.__bases__:
            chain = self.buildClassChain(base)
            results.extend(chain)

        return results

    def buildProperties(self, object):
        return {k: self.normalize(v) for k,v in object.__dict__.items()}


    def buildMethods(self, object):
        members = {}
        for name, value in  inspect.getmembers(object, inspect.ismethod):
            members[name] = value.func_code.co_varnames[1:]
        return members

    def buildStaticProperties(self, object):
        return {k:self.normalize(v)
                for (k,v) in object.__class__.__dict__.items()
                if not (k.startswith("__") or k.endswith("__") or inspect.ismethod(v) or inspect.isfunction(v))
        }

