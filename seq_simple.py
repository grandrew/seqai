# simple test of seqai algo

import sys,difflib,thread,random,math,time
import collections

# COEFF_LIKE_TIME = 0.2 # time likeness coefficient



STATS = {"links": 0, "groups": 0, "chunks":0}

class ListLike():
    def __init__(self, initlist = []):
        self.data = collections.OrderedDict()
        for ob in initlist:
            self.data[hash(ob)] = ob
    def append(self, ob):
        if not hash(ob) in self.data: 
            self.data[hash(ob)] = ob
    def __len__(self):
        return len(self.data)
    def __getitem__(self, key):
        return self.data[key]

# Chunk is a simplest data atom

def Link_compare(x,y):
    return int((x.value - y.value)*1000)

class LikeLink():
    def __init__(self, lfrom, lto, value=0):
        if lfrom.timeStart > lto.timeStart:
            self.tofrom = [lto, lfrom]
        else:
            self.tofrom = [lfrom, lto]
        self.value = value
        STATS["links"]+=1

    def checkme(self, el):
        if el in self.tofrom:
            return True
        return False

    def __repr__(self):
        return "<%s Weight:%s From:%s To:%s>" % (self.__class__.__name__, self.value, repr(self.tofrom[0]), repr(self.tofrom[1]))

    def __cmp__(self, other):
        if self.tofrom == other.tofrom: return 0
        if self.value > other.value: return 1
        else: return -1

class CauseLink(LikeLink):
    pass # OMG ?!

class StringChunk():
    def __init__(self, data, timeIn, fname="", seek_start=0, seek_end=0, groups=[], fdata = None):
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

    def __cmp__(self, other):
        if (self.data == self.other) and (self.timeStart == other.timeStart) and (self.timeEnd == other.timeEnd):
            return 0
        rv = self.value - other.value
        if rv == 0: return 1
        else: return rv

class Group():
    def __init__(self, elements):
        # do all computations here!
        self.timeStart = 2000000000
        self.timeEnd = -1
        self.elements = elements
        self.links = []
        self.weight = self.compute_weight() 
        STATS["groups"]+=1

    def __hash__(self):
        # only elements
        sum=0
        for ob in self.elements:
            sum += ob.timeStart + ob.timeEnd
        return sum
    
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
        
        # TODO why somebody may be asking to compare a group to a chunk! thats bad!
        if group == self: return 1.0 # TODO: ensure 1.0 means exactly equal
        if group.__class__.__name__ != "Group": return 0.0
        
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
                                if l1.checkme(l2):
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
        # likeness = (COEFF_LIKE_TIME * l_timeb + l_compb) / (len(self.elements) + len(group.elements));
        likeness = l_compb / (len(self.elements) + len(group.elements));
        if likeness < 0.1:
            return likeness
        newlink = LikeLink(self, group, likeness)
        if not newlink in self.links:
            self.links.append(newlink)
        self.links = sorted(self.links, Link_compare);
        return likeness

    def __repr__(self):
        return "<Group weight:%s, ts:%s, te:%s, elcount:%s, links:%s>" % (self.weight, self.timeStart, self.timeEnd, len(self.elements), len(self.links))

    def __eq__(self, other):
        # TODO TODO HERE
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
            # several different algorithms for different search
            # find all snips
            # also set up a group weight based on int links count
            # or just continue to drop small or lined groups?
            # OR maybe this thing should just FILTER OUT bad groups
            if curGroup.__class__.__name__ != "Group": break
            curGroup=random.choice(curGroup.elements)
            l_elements.append(curGroup)
            deep=+1
        lgroups.append(Group(elements=l_elements)) # TODO: do not append group-of one group-of one group!

def dream_iter(lgroups):
    "dreaming is following input time links and creating paths"
    # TODO HERE: remove code that dreams in coma and implement true dreaming
    # we need to distinguish eam paths and somehow implement relative timestamps
    # implement CauseCons class
    pass

def main():
    "will parse input filename into a holosemantic(?) space"
    fdata = file(sys.argv[1]).read()
    fdata = fdata.split()

    global lgroups
    lgroups = ListLike()

    ic = 0
    for s in fdata:
        lgroups.append( Group(elements=[StringChunk(data=s, timeIn=ic)]) )
        ic += len(s)
    i=0
    ts = time.time()
    try:
        while i<50000:
            coma_link_iter(lgroups)
            coma_group_iter(lgroups)
            i+=1
    except KeyboardInterrupt:
        print "Done;", i, "iterations"
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

