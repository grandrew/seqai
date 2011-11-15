#!/bin/python

import time
import difflib

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

# the system reads input once in time resolution
def input(s):
    # analyze input stream: tick-value with similarity search
    ts = time.time()
    schedule_process(s, ts) # TODO: process from within standard processing time

def dream():
    # continuously process database:
    # first, represent all data in unified format

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
