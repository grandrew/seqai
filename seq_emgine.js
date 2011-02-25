// seq_engine.js

/*
we take input stream(s), remember and compare them
- comparison gives weight
- creating maps and clusters of compared things
- then we start to compare clusters (?)
  - how amny elements in cluster, connections, other params as mean weight
  - what are the elements in there
somehow analyze time
store ssequence as zip? data+some diff?
somehow treat clusters same as data??
*/

MAXBYTES = 2048; // bytes maximum similarity seearch..?

// long-running buffer
var buf = new Array();
/*
  read and understand sequence - "input mode" or "direct reaction"
  only one argument is allowed - the current sequence in form of array
*/
function input(s) {
    // the second input is always time??
    // for each sequence read, record time, then use time diffs to compare too...

    var ts = (new Date()).getTime();
    
    // TODO: define this simd format: seq chunk, what parts are similar to what
    // like
    // later - also note the date/time and compare
    // this fn will communicate with DB...
    
    // 2011-02-25: first, properly index the input signal (extremum patterns, etc.), then perform a quick-search
    
    var simd = find_similarities(s, ts);
    db_record(simd); // TODO: write into db for later searching, index found data
                     // this method should also start dropping unused simds with less connections
                     // here also the weight is added to conn's
    act(simd); 
}

/*
  The following are to be run in thread-per-cpu, within chosen time intervals.
*/

// continuous analyzing the database in desired topics
function think() {

}

// in-depth inputs analysis
function dream() {

}

/*
  take some actions based on input sequence
*/
function act(simd) {
    // output something to somewhere, get the output and result as next seq
    // ask human?
    // program on LISP? C++ interpreter?
}

function find_similarities(s, ts) {
    // only detect whether we have string or numbers data
}

function find_similarities_string(s, ts) {
  // first, based on input data - either string or int or real
  // detect basic delimeter (like whitespace)
  // whitespace will be first, then punctuation chars
  // TODO: is it possible to auto-detect best delimeters?
  
  // delimeterless algorithm:
  // choose a window of 2 bytes, then increase to MAXBytes
  // now search trough DB/index for similarities, in different form inside the window
  // after some db size, start following/searching sims in docs(stored seqs/simd) with only 
  // heavy conns found at first 'glance' to database
  // invent optimal glance algorithm...

  // when no seq is given, analyze further in DB.thus store in simd info on stopped size and DB
  // /traverse or brute/ position 
}

function find_similarities_real(s, ts) {
    // compute std deviation here,
    // sync on extremums
    // index extremum patterns w/reasonable resolution?
}

/*
  TODO TODO TODO most interesting part here!!!
  continuous_analyzer - iterates through database creating input sequences/clusters based on database
  contents (weights and conns?? how??) creating more contetnts actually...
*/


// todo: save/load json
// live profile each step..

// misc

function levenshtein (s1, s2) {
    // http://kevin.vanzonneveld.net
    // +            original by: Carlos R. L. Rodrigues (http://www.jsfromhell.com)
    // +            bugfixed by: Onno Marsman
    // +             revised by: Andrea Giammarchi (http://webreflection.blogspot.com)
    // + reimplemented by: Brett Zamir (http://brett-zamir.me)
    // + reimplemented by: Alexander M Beedie
    // *                example 1: levenshtein('Kevin van Zonneveld', 'Kevin van Sommeveld');
    // *                returns 1: 3
    if (s1 == s2) {
        return 0;
    }

    var s1_len = s1.length;
    var s2_len = s2.length;
    if (s1_len === 0) {
        return s2_len;
    }
    if (s2_len === 0) {
        return s1_len;
    }

    // BEGIN STATIC
    var split = false;
    try {
        split = !('0')[0];
    } catch (e) {
        split = true; // Earlier IE may not support access by string index
    }
    // END STATIC
    if (split) {
        s1 = s1.split('');
        s2 = s2.split('');
    }

    var v0 = new Array(s1_len + 1);
    var v1 = new Array(s1_len + 1);

    var s1_idx = 0,
        s2_idx = 0,
        cost = 0;
    for (s1_idx = 0; s1_idx < s1_len + 1; s1_idx++) {
        v0[s1_idx] = s1_idx;
    }
    var char_s1 = '',
        char_s2 = '';
    for (s2_idx = 1; s2_idx <= s2_len; s2_idx++) {
        v1[0] = s2_idx;
        char_s2 = s2[s2_idx - 1];

        for (s1_idx = 0; s1_idx < s1_len; s1_idx++) {
            char_s1 = s1[s1_idx];
            cost = (char_s1 == char_s2) ? 0 : 1;
            var m_min = v0[s1_idx + 1] + 1;
            var b = v1[s1_idx] + 1;
            var c = v0[s1_idx] + cost;
            if (b < m_min) {
                m_min = b;
            }
            if (c < m_min) {
                m_min = c;
            }
            v1[s1_idx + 1] = m_min;
        }
        var v_tmp = v0;
        v0 = v1;
        v1 = v_tmp;
    }
    return v0[s1_len];
}

