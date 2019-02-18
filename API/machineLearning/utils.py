import itertools
import operator
import pickle

#Loads a object
def loadObj(name ):
    with open('./' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def findInDict (list, key, value):
    cont = 0
    for dict in list:
        if dict[key] == value:
            return cont
        cont += 1
    return None

#Finds the most commom item in a list
def mostCommon(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]