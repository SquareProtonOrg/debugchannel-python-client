import json, urllib2, inspect, traceback

class DebugChannel:
    def __init__(self, url, port, channel):
        self.url = "%s:%s/%s" % (url, port, channel)

    def __call__(self, *args, **kwargs): return self.log(*args, **kwargs)

    def log(self, object):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'User-Agent': "Mozilla/5.0"} 
        req = urllib2.Request(self.url, json.dumps(self.wrap(self.normalize(object, set()))))
        map(lambda (x,y): req.add_header(x,y), headers.items())
        urllib2.urlopen(req)

    def wrap(self, object):
        return { "handler": "object", "args": [ object], "stacktrace": self.stackTrace(3) }

    def stackTrace(self, dropCount):
    	try: raise Exception()
    	except Exception, e:
    		f = lambda (m, l, f, c): {"location": m, "fn": "%s:%s" % (f,l)}
    		return list(reversed([f(elem) for elem in traceback.extract_stack()]))[dropCount:]	

    def normalize(self, object, history):
        if id(object) in history: return "RECURSION"
        newHistory = set(history).union([id(object)])
        if hasattr(object, '__dict__'):
            return {
                "class": ["%s,%s" % (x.__module__, x.__class__) for x in self.buildClassChain(object.__class__)],
                "properties": self.buildProperties(object, newHistory),
                "methods": self.buildMethods(object),
                "static": self.buildStaticProperties(object, newHistory),
                "constants": []
            }
        return {"scalar": object}

    def buildClassChain(self, clazz):
        if clazz == object.__class__: return [clazz]
        return [clazz] + [ elem for base in clazz.__bases__ for elem in self.buildClassChain(base)]

    def buildProperties(self, object, history):
        return {k: self.normalize(v, history) for k,v in object.__dict__.items()}

    def buildMethods(self, object):
        return {name: value.func_code.co_varnames[1:] for name,value in inspect.getmembers(object, inspect.ismethod)}

    def buildStaticProperties(self, object, history):
        return {k:self.normalize(v, history)
                for (k,v) in object.__class__.__dict__.items()
                if not (k[:2]+k[-2:] == "____" or inspect.ismethod(v) or inspect.isfunction(v))
        }