#!/usr/bin/python3
from tokenize import generate_tokens,untokenize,tokenize
from io import StringIO
from token import tok_name,NAME


class TOKEN:
  def __init__(self,depth,str,num,begin,end):
    self.depth=depth
    self.str=str
    self.num=num
    self.begin=begin
    self.end=end

  def __str__(self):
    r="%d %7s (%2d)"%(self.depth,tok_name[self.num],self.num)
    for x in range(0,self.depth):
      r=r+" "
    r=r+self.str
    return r

  def __repr__(self):
#    return "'"+str(self.depth)+","+self.str+"'"
    return "'"+self.str+"'"

def decistmt(s):
    depth=0
    result = []
    priv=(-1,None)

    s=s.replace("\n", " ")
    g = generate_tokens(StringIO(s).readline)   # tokenize the string
    for toknum, tokval, begin, end, _  in g:
      if tokval=="{":
        depth=depth+1

      if tokval=="=" and priv.depth==depth and priv.str==":":
        begin=priv.begin  #todo: FIXME begin,end
        result.pop()
        tokval=":="

      priv=TOKEN(depth,tokval,toknum,begin,end)
      result.append( priv )

      if tokval=="}":
          depth=depth-1

    return result

class ELEMENT():
  def __init__(self,tokens):
    self.name="?"
    self.val=[]
    self.depth=tokens[0].depth

    self.begin=tokens[0].begin
    self.end=tokens[-1].end


#DEBUG:
#    print tokens

    if len(tokens)>2 and tokens[1].str==":=":
      self.name=tokens[0].str
      tokens.pop(0)
      tokens.pop(0)

    if len(tokens)==1:
      self.val=tokens[0].str
      return

    if tokens[0].str=="{" and tokens[-1].str=="}":

      self.depth=tokens[0].depth
      tokens.pop(0)
      tokens.pop(-1)

      self.tmp=[]
      for i,t in enumerate(tokens):
        if (t.str=="," and t.depth==self.depth) or i+1==len(tokens):
          if i+1==len(tokens): self.tmp.append(t) #bugfix
          if len(self.tmp)>0:
            if len(self.tmp)==1:
              self.val.append( self.tmp[0].str )
            else:
              self.val.append( ELEMENT(list(self.tmp)) )
          self.tmp=[]
        else:
          self.tmp.append(t)
      return

    raise Exception('Unexpected input for initing ELEMENT', str(tokens))

  def hasChildren(self):
    a=False
    for E in self.val:
      if isinstance(E, ELEMENT):
        return True
    return False

  def toString(self,pre):
    ret=""
    if type(self.val) is list:
      ret=self.name+'#'+str(len(self.val))
      for i,element in enumerate(self.val):
        if isinstance(element, ELEMENT):
          ret=ret+"\n"+element.printf(pre+self.name+"::")
        else:
          ret=ret+"\n"+pre+self.name+"="+str(element)
    else:
       ret=self.name+"="+str(self.val)
    return pre+ret

  def toDict(self):
    ret=dict()

    if self.hasChildren()==False:
      return self.val

    for j,E in enumerate(self.val):
      name=str(j)
      if isinstance(E, ELEMENT):
        if E.name!="?": name=E.name
        if type(E.val) is list:
          val=E.toDict()
        else:
          val=E.val
      else:
        val=E
      ret[name]=val
    return ret


#extract data only and split into arrays
def process(ret):
  RET=[]
  tmp=[]
  for i in range(0,len(ret)):
    r=ret[i]
    if r.depth==0: continue

    #add name if was set before "{"
    if len(tmp)==0 and i>2:
      if ret[i-1].str==":=" and ret[i-2].num == NAME:
        tmp.append(ret[i-2])
        tmp.append(ret[i-1])

    tmp.append(r)

    if r.depth==1 and r.str=="}":
      RET.append(ELEMENT(tmp))
      tmp=[]
  return RET


def ttcnlog2tree(data):
  tmp=decistmt(data)
  #debug
  #for r in ret:
  #  if r.depth==0: continue
  #  print(str(r))
  return process(tmp)

def ttcnlog2dict(data):

  tmp=ttcnlog2tree(data)

  RET=dict()
  for i,e in enumerate(tmp):
    name=str(i)
    if e.name!="?": name=e.name
    RET[name]=e.toDict()

  return RET;

############################################
if __name__=="__main__":
  data="""
   hello
   DAWID{ a := 0, b := "d\\"upa", c := omit, d := { 1, 2, 3 }, d2 := { a:= false, b:= {1} }, e := false, f := { {}, { 1.0 }, { 0x2, 12 }, { 3.0, 3, 3 } } }
   ass:={1,2,3}
   """

  print("input: %s"%data)

  from pprint import pprint
  pprint(ttcnlog2dict(data))
############################################



