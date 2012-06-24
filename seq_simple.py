# simple test of seqai algo

import sys,difflib,thread,random,math,time,traceback
import collections

# COEFF_LIKE_TIME = 0.2 # time likeness coefficient



STATS = {"deepness":0, "LikeLink": 0, "CauseLink": 0, "groups": 0, "chunks":0}

class ListLike():
    def __init__(self, initlist = None):
        #self.data = collections.OrderedDict()
        if initlist is None:
            initlist = []
        self.s = {}
        self.l = initlist
        for ob in initlist:
            self.s[hash(ob)] = ob
    def append(self, obj):
        if not (hash(obj) in self.s):
            #self.s.add(ob)
            self.s[hash(obj)] = obj
            self.l.append(obj)
    def __len__(self):
        return len(self.l)
    def __getitem__(self, key):
        return self.l[key]


def Link_compare(x,y):
    return int((x.value - y.value)*1000)

class LikeLink():
    def __init__(self, lfrom, lto, value=0):
        if lfrom.timeStart > lto.timeStart:
            self.tofrom = [lto, lfrom]
        else:
            self.tofrom = [lfrom, lto]
        self.value = value
        STATS[self.__class__.__name__]+=1

    def checkme(self, el):
        if el in self.tofrom:
            return True
        return False

    def to(self, other):
        # use caller to identify?
        if self.tofrom[0] == other: return self.tofrom[1]
        if self.tofrom[1] == other: return self.tofrom[0]
        raise ValueError("Link .to() should be called with one of existing elements!")

    def __repr__(self):
        return "<%s Weight:%s From:%s To:%s>" % (self.__class__.__name__, self.value, repr(self.tofrom[0]), repr(self.tofrom[1]))

    def __cmp__(self, other):
        if self.tofrom == other.tofrom: return 0
        if self.value > other.value: return 1
        else: return -1

    def __hash__(self):
        return hash(str(hash(self.tofrom[0]))+str(hash(self.tofrom[1])))

class CauseLink(LikeLink):
    def cause(self):
        return self.tofrom[0]
    def effect(self):
        return self.tofrom[1]

# Chunk is a simplest data atom
class StringChunk():
    def __init__(self, data, timeIn, fname="", seek_start=0, seek_end=0, groups=None, fdata = None):
        self.data = data
        self.fdata = fdata # fdata is a fd-like object that may be seek()'d to data
        self.fname = fname # thi is a file name of where the text is in
        self.timeStart = timeIn
        self.timeEnd = timeIn # unused?
        self.groupsIn = groups
        STATS["chunks"]+=1

    def getData(self):
        "gets associated data"
        return self.data

    def getLikeness(self, chunk):
        if not hasattr(chunk, 'data'): return 0
        return difflib.SequenceMatcher(None, self.data, chunk.data).ratio()

    def __repr__(self):
        return "<StringChunk ts:%s, Data:'%s'>" % (self.timeStart, self.data)

    def __hash__(self):
        return hash(self.data)+self.timeStart+self.timeEnd

    def __eq__(self, other):
        if (self.data == other.data) and (self.timeStart == other.timeStart) and (self.timeEnd == other.timeEnd):
            return True
        return False

class Group():
    def __init__(self, elements):
        # do all computations here!
        self.timeStart = 2000000000
        self.timeEnd = -1
        self.elements = elements
        #self.links = []
        self.links = ListLike()
        self.weight = self.compute_weight() 
        STATS["groups"]+=1

    def __hash__(self):
        # only elements
        summ=0
        for ob in self.elements:
            summ += (ob.timeStart + ob.timeEnd)
        return summ
    
    def compute_weight(self):
        # get a link weight mean
        weight_acc = 0
        for el1 in self.elements:
            if el1.timeStart < self.timeStart: self.timeStart = el1.timeStart
            if el1.timeEnd > self.timeEnd: self.timeEnd = el1.timeEnd
            for el2 in self.elements:
                weight_acc += el1.getLikeness(el2)
        return weight_acc / len(self.elements)

    def getLikeness(self, group):
        #l_timeb = 1.0 / ((abs(self.timeStart - group.timeStart) + abs(self.timeEnd - group.timeEnd)) / 2.0+1);
        # compute mean likeness between all first-order elements??
        # how about comparing very large groups????? -> dive through all links and find if any is linking to current element, use that weight
        
        if group == self: return 1.0 # TODO: ensure 1.0 means exactly equal
        
        
        
        
        
        # ----------------------------------------------------------------------!!!!!!!!!!!!!!!!!!1
        # TODO why somebody may be asking to compare a group to a chunk! thats bad!
        if group.__class__.__name__ != "Group": return 0.0
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!TODO TODO TODO TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        
        
        
        
        # TODO check if we already have this likeness BEFORE calculating and not on the adding stage
        # TODO rethink this all!
        l_compb = 0
        for el1 in self.elements:
            for el2 in group.elements:
                    if (el1.__class__.__name__ != "Group") and (el2.__class__.__name__ != "Group"):
                        l_compb += el1.getLikeness(el2)
                    elif (el1.__class__.__name__ == "Group") and (el2.__class__.__name__ == "Group"):
                        # do not call likeness if not having links already
                        # for all other, do only check links
                        for l1 in el1.links:
                            for l2 in el2.links:
                                if l1.checkme(l2): # TODO HERE! checkme DOES NOT WORK THAT WAY ERRRRORRRRR!!!!!!
                                    l_compb += l1.value # use link weight?
                    else:
                        #if el1.__class__.__name == "Group":
                        #    el_tmp = el1
                        #    el1 = el2
                        #    el2 = el_tmp
                        #for el in el2.elements:
                        #    if
                        pass # no comparison exists between a group and a chunk!
        # TODO: check how counting only first-level elements affects the system??
        likeness = l_compb / (len(self.elements) + len(group.elements));
        if likeness < 0.1:
            return likeness
        newlink = LikeLink(self, group, likeness)
        #if not newlink in self.links:
        #    self.links.append(newlink)
        self.links.append(newlink)
        group.links.append(newlink) # two-way linking...!
        
        # TODO sort before wakeup once! this is very expensive!
        # self.links = sorted(self.links, Link_compare);
        return likeness

    def __repr__(self):
        return "<Group weight:%s, ts:%s, te:%s, elcount:%s, links:%s>" % (self.weight, self.timeStart, self.timeEnd, len(self.elements), len(self.links))

    def __eq__(self, other):
        # does this work??
        if self.elements == other.elements: return True
        return False

def coma_link_iter(lgroups):
#    while True:
        # now walk through groups to find links?
        # use a fully-random link search now...
        g1 = random.choice(lgroups)
        g2 = random.choice(lgroups)
        g1.getLikeness(g2) 

def coma_group_iter(lgroups):
        # follow links to find loops, stars and 
        # choose random deepness
        max_deep = random.randint(2, 100)
        deep = 0
        curGroup = random.choice(lgroups)
        l_elements=[curGroup]
        while deep < max_deep:
            #if curGroup.__class__.__name__ != "Group": break # TODO: unnessessary check?
            if len(curGroup.links) == 0: break
            curGroup=(random.choice(curGroup.links)).to(curGroup)
            l_elements.append(curGroup)
            deep+=1
        # TODO: filter out 'bad' groups? or clean garbage?
        if len(l_elements) > 1:
            lgroups.append(Group(elements=l_elements)) # TODO: do not append group-of one group-of one group!
            STATS["deepness"]+=deep

def dream_iter(lgroups):
        "dreaming is following input time links and creating paths"
        # change causelink value if context follows more times?
        # TODO: follow only groups that weight more? hmm.. or less? whatever optimization is NOT NOW anyways
        max_deep = random.randint(2, 100)
        deep = 0
        curGroup = random.choice(lgroups)
        l_elements=[curGroup]
        while deep < max_deep:
            nextGroup=random.choice(lgroups)
            clink = CauseLink(curGroup, nextGroup)
            curGroup.links.append(clink) # random cause-consequence? hehe ;-)
            nextGroup.links.append(clink) # two-way linking!
            curGroup = nextGroup
            deep+=1

# context should add cause-consequence links immediately!

def main():
    "will parse input filename into a holosemantic(?) space"
    fdata = file(sys.argv[1]).read()
    fdata = fdata.split()

    global lgroups
    lgroups = ListLike()
    print "Initializing lgroups from %s samples" % len(fdata)
    sys.stdout.flush()
    ic = 0
    i = 0
    try:
            for s in fdata:
                lgroups.append( Group( [ StringChunk(data=s, timeIn=ic) ] ) )
                ic += len(s)
                i += 1
                if (i % 1000) == 0: print "Samples parsed:", i
    except KeyboardInterrupt:
        print "Interrupted at"
        traceback.print_exc()
        STATS["deepness"] = float(STATS["deepness"])/float(i) # compute average!
        print STATS
    i=0
    print "Done, starting dreaming"
    sys.stdout.flush()
    ts = time.time()
    try:
        while i<50000:
            coma_link_iter(lgroups)
            coma_group_iter(lgroups)
            dream_iter(lgroups)
            i+=1
    except KeyboardInterrupt:
        traceback.print_exc()
        tt = time.time()
        print "Done;", i, "iterations", tt-ts, "seconds", float(i)/(tt-ts), "it/s"
        STATS["deepness"] = float(STATS["deepness"])/float(i) # compute average!
        print STATS
        try:
            ibrowse(lgroups)
        except KeyboardInterrupt:
            print "Bye!"
    print "Run time: %s seconds" % (str(time.time()-ts))
    ibrowse(lgroups)

def print_group(group):
    print repr(group)
    i=0
    for e in group.elements:
        print "-- E:",repr(e)
        i+=1
        if i>5:break
    if i>5: print "-- E: ..."
    i=0
    for e in group.links:
        print "-- L:",repr(e)
        i+=1
        if i>5:break
    if i>5: print "-- L: ..."

def ibrowse(lgroups):
    x = 0
    cur = lgroups
    cpath = "> "
    while x!=-1:
        print cpath
        print "Groups:", len(cur)
        try:
            for i in range(0,5):
                print "-------------------"
                try:
                    print_group(cur[i])
                except:
                    pass
            print "======="
            for i in range(1000,1005):
                print "-------------------"
                try:
                    print_group(cur[i])
                except:
                    pass
                print ""
        except IndexError:
            pass
        x = int(raw_input("Group number: "))
        cpath += repr(cur[x]) + " > "
        cur = cur[x].elements

    ibrowse(lgroups)

if __name__ == "__main__":
    main()

