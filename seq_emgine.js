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


    /*
      partially use the same techniques as think() or dream(), with dream() using
      them more. Control the time spent on one-time thinking somehow?
    */ 
    
}


/*
  TODO TODO TODO most interesting part here!!!
  continuous_analyzer - iterates through database creating input sequences/clusters based on database
  contents (weights and conns?? how??) creating more contetnts actually...
*/


// todo: save/load json
// live profile each step..
