##Programming by Transformations
  
  A computer program could be described by a series of transformations from an initial empty project to the final program.  Start with 'main() { return 0;}'.  Next step, 'Add function call to foo and definition of foo and body', etc.  What if the actual representation for the program was this list of transformations, rather than the final source.

   A program in an existing VCS is stored somewhat like this (for well-written check-ins, anyway), but the changes always get applied by appending to the end of the chain.  The idea is that new functionality or bug fixes could be made modifying or adding transformations anywhere along the chain.  To allow changes at any point along the chain, and have subsequent transformations apply cleanly, using textual diffs (like existing VCS's) will not work well.  It would need to use transformations at the AST level.  Probably even arbitrary AST transformations would not be allowed - a more tightly constrained set of transformations would be needed.

   Refactoring has given us ways to talk about patterns of program changes, though its concerned with changes that preserve program behavior (but enable changes in the future).   Additional patterns of changes would be needed that add functionality.  Defining a proper set of transformations, and how to name and understand them, is really the crux of what would make this scheme work

   One motivation is to aid program comprehension.  Ideally the transformations would be structured to add the most important parts of the program first, and add more localized or special case pieces later.  Educational descriptions of algorithms or features usually start with a simple example and add complexity in a logical progression.  Which is great for small programs, but this sort of logical progression is missing just when you need it most for undestanding a large code base.

 Another motivation is from scientific computing - when deriving equations and algorithms, it's usually done through a series of steps applying a transformation to the previous result (take a derivative, move terms around, etc.)  It might be useful to represent scientific programs themselves closer to this style. (And thinking about this is where the idea came from in the first place).

   Even more speculatively, it might shed some light on where complexity comes from in computer programs. (Do you ever look at code - especially your own - and wonder 'Where did all this #!&.^@ code come from and why is is needed?'  But then looking at each piece - it's all there for a reason.

   One (slighty more) concrete application might be error handling code.  It generally takes a lot of space, and is necessary, but makes it much harder to understand the underlying code flow.   The idea would be to introduce the basic code flow as one transformation step, and add the error handling in a separate transformation step.

   Convential VCS's record history as it was done.  Git allows some more flexibility - a series of checkins can be stored as history, or modified to make a 'nicer' path.  But one has to make a choice.  This would allow both simultaneously - the sequence of transformations could be modified anywhere along it (kinda like a history, except recording how you wish you had written the program given what you learned after writing the program. It's more like a progression from global to local behavior), and the history of changes to this sequence would also be stored (in source control)


   Some potential problems:
    - Thinking in terms of transformations (diffs) rather than actual code is hard.   Even with tool support to show some representation after each step, this might be hard.
    - To provide value, changes needs to be made at any point in the chain, and subsequent transformations need to apply without too many additional changes.  This might get too complex for realistic programs.

### Sources of Inspiration for Transforms.
We want the transforms to be informative in the domain, easy to reason about, and should easily reapply if the code changes.

1. Text diffs from existing check-ins
  This will quickly fail the last criteria (changes will not reapply if changes are made upstream)
  
2. Aspect-Oriented Programming

3. PIN instrumentation
