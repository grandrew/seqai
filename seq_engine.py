#!/bin/python
import ZODB
import transaction
import persistent

import time,os
import difflib


from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
storage = FileStorage('SeqAIData.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

TIMEFADE = 3.0

TYPE_TIME = 0

rawfd = file(os.path.expanduser("~/seq_engine.raw"), "a")

iDataCounter = rawfd.tell()
prevSeconds = time.time()

def act():
    # act 'ticks' ordering the system to do something
    # either switch to another solution opportunity
    # or give at last the answer/action
    # act ticks period are dependent on input environment
    
    # the system should act based on latest input analysis
    # and based on current model loaded
    # action is taken on 'what's currently going on' model
    # we search for actions patterns, and if no actions seen
    # we try any actions we can take, mostly randomly but trying to
    # do some correlation
    pass

"""
Technical implementation.
1. Divide input data to racks: use 2GB of data to allow for easier addressing using video card.
- append- write all data to a file
- do first split of input data using sax-like algorithm
  for each input type we will use separate raw database but will unite on upper layers (how?)
- create immediate real-time link while parsing, compare with
  clock
- have a separate input-link, immediate analyze/act and dream process
- pass chunks from input analyzer to dream buffer
- need an algorithm to continuously analyze all data
- input analyzer should link current input so that it creates current context, the links should fade afterwards?? It is called current state.
- ??? output somehow connected with input. Output data is stored in chunks the same way, BUT how will we get abstract mind???
  Send output signal and create link to input (current)
  Long-term connections can be inferred by watching links (ontology) of output and input patterns
- ??? act module!!
  Acting is a built-in algorithm which tries to optimize for something?
"""

# ZODB seems to be OK for this task.. or postgres ??

# chunk is always the smallest input atom
# TODO: chunk does NOT have links!!!
#       only group of one chunk may have links
#       also chunk is atomic - no TimeStart and end!
#       chunk is actually just data...
class Chunk(persistent.Persistent):
    # TODO: this is all in question!
    def __init__(self, data, timeIn, links=[], groups=[]):
        self.data = data
        self.timeStart = timeIn
        self.timeEnd = timeIn
        self.links = []
        self.groupsIn = []
    
    def getData(self):
        "gets associated data"
        # TODO!!! get data if compressed!
        return self.d
    
    def getLikeness(self, chunk):
        return difflib.SequenceMatcher(None, self.d, chunk.d).ratio()
        
    def setLink(self, link):
        self.links.append(link)
    
    def createDualLink(self, chunk, weight):
        l = Link(self, chunk, weight)
        self.setLink(l)
        chunk.setLink(l)
        

class Link(persistent.Persistent):
    def __init__(self, cfrom, to, weight):
        self.chunk = to
        self.linkfrom = cfrom
        self.weight = weight
        self.accessCount = 0
    
    def to(self, ref=None):
        if ref is None:
            self.accessCount+=1
            return self.chunk
        else:
            if ref == self.chunk:
                return self.linkfrom
            else:
                return self.chunk

class LinkTime(Link):
    def __init__(self):
        pass

class LinkAlike(Link):
    def __init__(self):
        pass


class Group(persistent.Persistent):
    def __init__(self, lElements=[], lLinks=[], lGroups=[], timeStart=0, timeEnd=0):
        self.elements = lElements
        self.groupsIn = lGroups
        self.links = lLinks
        self.timeStart = time.time()*2 # OUPS!!
        self.timeEnd = 0
        self.weight = 0 # TODO: compute!?
        
    def getLikeliness(self, group):
        pass
    
    def addElement(self, el):
        self.elements.append(el)
        el.groupsIn.append(self)
        if self.timeStart > el.timeStart:
            self.timeStart = el.timeStart
        if self.timeEnd < el.timeEnd:
            self.timeEnd = el.timeEnd
    # TODO: remove element?

CONTEXT = [] # is the current context which we are trying to regress and keep in sync
BUF_IACT = []
BUF_DREAM = []

global CONTEXT
global prevChunk
global iDataCounter


def compute_params():
    pass

oldChunks = []

def input(s):
    # analyze input stream: tick-value with similarity search
    #ts = time.time()
    #schedule_process(s, ts) # TODO: process from within standard processing time
    global prevChunk
    global iDataCounter
    global BUF_IACT
    global BUF_DREAM
    global prevSeconds
    global oldChunks

    # parse input string to atomic chunks!
    lChunks = []
    # chapters and paragraphs are like if we introduced time division between inputs
    global s_word
    
    lwords = []
    lparagraphs = []
    lchapters = []
    
    iNCp = 0 # \n counter
    iByte = offset # byte counter
    for b in s:
        if b == "\n":
            iNCp+=1
        if b == " " or b == "\t" or b == "\n": # and no word-wrap allowed!
            # TODO: drop counters, add wordbuf to word
            if len(s_word) > 0:
                # create chunk now
                # TODO HERE: compute links to other chunks
                #   and link other chunks to this chunk
                chunk = Chunk(s_word, time.time(), [], [])
            
            # drop wordbuf to ""
            s_word=""
        else:
            if iNCp == 1: # paragraph detected, next word coming
                # create paragraph group
                iNCp = 0
            elif iNCp > 1: # chapter detected (?)
                # create chapter group
            s_word+=b
            iNCp = 0
        iByte++

    chunk = Chunk();
    
    chunk.timeIn = time.time()
    chunk.timeDiff = chunk.timeIn - prevSeconds
    chunk.data = 
    
    link = Link()
    link.chunk = prevChunk
    link.distance = chunk.timeDiff / TIMEFADE
    link.linkType = TYPE_TIME
    chunk.links.append(link)

    # !!!! TODO: in analyzer, if this chunk is identical to other chunk,
    #    1. set diff to 0, remove data, getData SHOULD then know how to get its data
    #    2. compress the whole input - either drop or say it is identical to other group
    #    3. set string-group repeat weight heigher!!!
    # chunk.compress() # TODO: compress chunk using the data provided in links! (lossless?)
    # TODO: when all data is compressed -> no need for data-logfile?
    
    # TODO: pass the chunk to immediate act
    BUF_IACT.append(chunk) # acquire lock, safe-append, release

    # TODO: pass to dream buffer LATER!!!
    BUF_DREAM.append(chunk) # TODO: do it after ACT buffer has completed actions
    
    prevSeconds = time.time()
    prevChunk = chunk

s_chapter = ""
s_paragraph = ""
s_word = ""

def saxlike(s, offset):
    # if the word is too large, will produce several new words by splitting at middle
    # for text, use:
    #     chapter, paragraph, word
    global s_chapter
    global s_paragraph
    global s_word
    
    lwords = []
    lparagraphs = []
    lchapters = []
    
    iNCp = 0 # paragraph - \n counter
    iNCc = 0 # chapter..
    iByte = offset # byte counter
    for b in s:
        if b == "\n":
            iNCp++
            iNCc++
        elif b == " " or b == "\t": # other whitesace??
            # TODO: drop counters, add wordbuf to word
            iNCp=0
            iNCc=0
            lwords.append({"data": s_word, "start": iByte-len(s_word), "end": iByte})
            # drop wordbuf to ""
            s_word=""
        else:
            if iNCp == 1: # paragraph detected, next word coming
                lparagraphs.append(s_paragraph)
                s_paragraph = ""
                iNCp = 0
            elif iNCp > 1: # chapter detected (?)
                # TODO HERE: how to sustain byte-flow order ?? we will feed this to input analyzer
                # and IA should make use of the order to connect?? THINK!
            s_chapter+=b
            s_paragraph+=b
            s_word+=b
        iByte++

def thread_act():
    # get from BUF_IACT
    # connect to CONTEXT
    # fade-out old CONTEXT chunks
    # TODO: perform actions??
    pass

def thread_dream():
    # parse dream buffer,
    # analyze further (maybe in other threads? separate thread for each "level" ?)
    # try to connect chunk groups into 'actions' using their timelines
    pass

def string_match(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).ratio()

# the new algorithm from the old:
# - create marks to mark chunk start and chunk end 
# >> raw (L0) chunk is actually data start(absolute or -length), length, input datetime, input lag, links with weights) links are also linking time frames and within raw input chunk links have more weight
# >> L1 chunk is M1 linked chunks (in any direction) that are treated as one chunk with top N links better is when links are to the same chunk inside L1 chunk since weight is summarized
# >> Ln chunk is M2 L1 chunks closely linked
# good chunks have many internal links and less good external links
# good links are links to objects that have not very much links to and from
# when the amount of links becomes too much - drop its processing
# TODO: link weight and links amount? weight is more within one bigger chunk, less between chunks

def string_subchunk(sInput):
    # return possible sub-chunks (?)
    # todo: data-independent
    lWords = sInput.split()
    pass

def parametrize_chunk(chunk):
    # how to parametrize:
    # - calculate basic params
    # - compute matching against previous input or context(?)
    #  for string:
    #   - total chunk compare
    #   - divide by words, compare words, link
    #   - compare by commas and other syms
    #   - compare by random 
    # - create subchunks!!! the above is subchunkink
    # - recalculate other input's parameters
    # - the chunk then re-parametrized again later

    # mean value
    # chunk length
    # deviation
    # time of arrival
    # time diff previous chunk, us
    # time diff next chunk, us
    # number of silences

    # number of matches 90%
    # number of matches 60%
    # number of matches 30%
    # each match with number of times hit
    # delovie linii sankt-peterburg laguna piter 8 496 758 33 68

def chunk_compare():
    # compare chunks by several parameters
    # change parameters during compare:
    # mean_likeness
    # times_hit
    # previous_match (??)
    # when best-match chunk found, adjust weights
