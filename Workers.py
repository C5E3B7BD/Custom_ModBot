class Helpers:
    def __init__(self):
        #null
        x=[]
    def makeUnique(seq, idfun=None):
       #Credit for this function goes to Peter Bengtsson
       #http://www.peterbe.com/
       if idfun is None:
           def idfun(x): return x
       seen = {}
       result = []
       for item in seq:
           marker = idfun(item)
           if marker in seen: continue
           seen[marker] = 1
           result.append(item)
       return result
