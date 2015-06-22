##Programming by Transformations
  
  A computer program could be described by a series of transformations from an initial empty project to the final program.  Start with 'main() { return 0;}'.  Next step, 'Add function call to foo and definition of foo and body', etc.  What if the actual representation for the program was this list of transformations, rather than the final source.

   A program in an existing Version Control System (VCS) is stored somewhat like this (for well-written check-ins, anyway). Changes always get applied by appending to the end of the chain.  The idea is that new functionality or bug fixes could be made modifying or adding transformations anywhere along the chain.  To allow changes at any point along the chain, and have subsequent transformations apply cleanly, using textual diffs (like existing VCS's) will not work well.  It would need to use transformations at the AST level.  Probably even arbitrary AST transformations would not be allowed - a more tightly constrained set of transformations would be needed.

   Refactoring has given us ways to talk about patterns of program changes, though its concerned with changes that preserve program behavior (but enable changes in the future).   Additional patterns of changes would be needed that add functionality.  Defining a proper set of transformations, and how to name and understand them, is really the crux of what would make this scheme work

   One motivation is to aid program comprehension.  Ideally the transformations would be structured to add the most important parts of the program first, and add more localized or special case pieces later.  Educational descriptions of algorithms or features usually start with a simple example and add complexity in a logical progression.  Which is great for small programs, but this sort of logical progression is missing just when you need it most for undestanding a large code base.

 Another motivation is from scientific computing - when deriving equations and algorithms, it's usually done through a series of steps applying a transformation to the previous result (take a derivative, move terms around, etc.)  It might be useful to represent scientific programs themselves closer to this style.

   One (slighty more) concrete application might be error handling code.  It generally takes a lot of space, and is necessary, but makes it much harder to understand the underlying code flow.   The idea would be to introduce the basic code flow as one transformation step, and add the error handling in a separate transformation step.

   Convential VCS's record history as it was done.  Git allows some more flexibility - a series of checkins can be stored as history, or modified to make a 'nicer' path.  But one has to make a choice.  This would allow both simultaneously - the sequence of transformations could be modified anywhere along it (somewhat like a history, except recording how you wish you had written the program given what you learned after writing the program. It's more like a progression from global to local behavior), and the history of changes to this sequence would also be stored (in source control)


   Some potential problems:
    - Thinking in terms of transformations (diffs) rather than actual code is hard.   Even with tool support to show some representation after each step, this might be hard.
    - To provide value, changes needs to be made at any point in the chain, and subsequent transformations need to apply without too many additional changes.  This might get too complex for realistic programs.

### Sources of Inspiration for Transforms.
We want the transforms to be informative in the domain, easy to reason about, and should easily reapply if the code changes.

* Text diffs from existing check-ins.
  This will quickly fail the last criteria (changes will not reapply if changes are made upstream).  However, this will inform the sort of needed AST transforms.
* Refactoring.  See the catalog at http://refactoring.com/catalog/
* Aspect-Oriented Programming ( https://en.wikipedia.org/wiki/Aspect-oriented_programming )
* PIN binary instrumentation ( https://software.intel.com/en-us/articles/pin-a-dynamic-binary-instrumentation-tool )

### Simple Example
Start with some Python code to open and close a file (call this V1)
````python
f = open("file.txt", "r")
f.close()
````

Now add some exception handling (in case the file doesn't exist or is not readable) (call this V2)
````python
try:
    f = open("file.txt", "r")
    f.close()
except IOError as e:
    print 'Unable to open file: %s' % str(e)
````

Sometime later, we learn about the context manager feature in Python, that will automatically close the file for us.  Modify V1 to get (call this V3)
````python
with open("file.txt", "r") as f:
    pass
````

The code with exception handling will look like (call this V4)
````python
try:
    with open("file.txt", "r") as f:
        pass
except:
    print 'Unable to open file: %s' % str(e)
````

In traditional development, the history would look like V1 -> V2 (add exception handling) -> V4 (context manager and exception handling).

In the proposed scheme, the code would initially be stored as the flow V1 -> V2 (add exception handling).   The change to use a context manager would be made in the first node (change V1 to V3).  The final flow is then V3 -> V4.
History then looks like

1. V1 -> V2
2. V3 -> V4

Alternately, one could also add a node to store the flow V1 -> V3 (context manager) -> V4 (context manager and exception handling), but this doesn't seem as informative.  It's useful for learning the Python feature, but not so useful for understanding the program)

Ideally the transformation to add the exception handling could be specified in a generic way - label or identify the code that opens and processes the file, and then add the exception handling code around it.  Then the same transformation could be used for V1->V2 and V3->V4.

