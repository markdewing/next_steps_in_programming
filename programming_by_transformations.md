## Programming by Transformations
  
  The goal is to describe a computer program by a series of transformations from an initial empty project to the final program.   Even further, the actual representation for the program will be this list of transformations, rather than the final source.

   A program in an existing Version Control System (VCS) is stored somewhat like this, except changes always get applied by appending to the end of the chain.  The proposed idea is that new functionality or bug fixes are made by modifying or adding transformations anywhere along the chain.  
   
A simple ASCII diagram for history in a VCS
  
  `[Initial commit, version 1] -> [Version 2] -> [Version 3]`
  
The next check-in adds a version and the history looks like
  
  `[Initial commit, version 1] -> [Version 2] -> [Version 3] -> [Version 4]`

In the proposed scheme, there is a chain of transformations between versions
  
  `[Version 1] -> [Version 2] -> [Version 3]`
  
Each transformation is a refinement to the program (adding features, special cases, error handling, or other complexity).   History and VCS still exist, but the diagram takes on a two-dimensional shape (this idea might be called "2-D version control)". (In the following diagram, the history is the numbered items)
  
  1. `[Version 1] -> [Version 2] -> [Version 3]`
  2. `[Version 1] -> [Version 2a] -> [Version 3]`  (Change a node in the middle)
  3. `[Version 1] -> [Version 2a] -> [Version 3] -> [Version 4]`  (New nodes can be appended, just like traditional development)
  

To allow changes at any point along the chain, and have subsequent transformations apply cleanly, textual diffs (like existing VCS's) will not work well.  Transformations at the AST level will be needed.  Probably even arbitrary AST transformations would not be that useful - a more tightly constrained set of transformations would be needed.
  
   The transformations between versions become the focus of the development.  I'm curious as to how changing this focus will change how I view programming ("All programming becomes meta-programming"?).  The full representation of the program at each node is important to connect with existing programming practice, and we still need to read something in a linear order for best comprehension.  Structured or projectional editors seem like the best way to manage the representation.

   Refactoring has given us ways to talk about patterns of program changes, though it's concerned with changes that preserve program behavior (but enable changes in the future).   Additional patterns of changes would be needed that add functionality.  Defining a proper set of transformations, and how to name and understand them, is really the crux of what would make this scheme work.

   One motivation is to aid program comprehension.  Ideally the transformations would be structured to add the most important parts of the program first, and add more localized or special case pieces later.  Educational descriptions of algorithms or features usually start with a simple example and add complexity in a logical progression.  Which is great for small programs, but this sort of logical progression is missing just when you need it most - for understanding a large code base.

Another motivation is from scientific computing - when deriving equations and algorithms, it's usually done through a series of steps applying a transformation to the previous result (take a derivative, move terms around, etc.)  It might be useful to represent scientific programs themselves closer to this style.

Another application might be error handling code.  It generally takes a lot of space, and is necessary, but makes it much harder to understand the underlying code flow.   The idea would be to introduce the basic code flow as one transformation step, and add the error handling in a separate transformation step.

Convential VCS's record history as it was done.  Git allows some more flexibility - a series of checkins can be stored as history, or modified to make a 'nicer' path.  But one has to make a choice.  This would allow both simultaneously - the sequence of transformations could be modified anywhere along it (somewhat like a history, except recording how you wish you had written the program given what you learned after writing the program. It's more like a progression from global to local behavior), and the history of changes to this sequence would also be stored (in source control).


Some potential problems:
  - Thinking in terms of transformations (diffs) rather than actual code is hard.   Even with tool support to show some representation after each step, this might be hard.
  - To provide value, changes needs to be made at any point in the chain, and subsequent transformations need to apply without too many additional changes.  This might get too complex for realistic programs.

### Sources of Inspiration for Transforms.
We want the transforms to be informative in the domain, easy to reason about, and should easily reapply if the code changes.

* Text diffs from existing check-ins.
  This will quickly fail the last criteria (changes will not reapply if changes are made upstream).  However, this will inform the sort of needed AST transforms.
* Refactoring.  See the catalog at http://refactoring.com/catalog/
* Semantic diff tools (such as ChangeDistiller http://www.ifi.uzh.ch/seal/research/tools/changeDistiller.html )
* Aspect-Oriented Programming ( https://en.wikipedia.org/wiki/Aspect-oriented_programming )
* PIN binary instrumentation ( https://software.intel.com/en-us/articles/pin-a-dynamic-binary-instrumentation-tool )
* [Program slicing]( https://en.wikipedia.org/wiki/Program_slicing ).  This talk by Alan Shreve about ["Idealized Commit Logs: Code Simpliciation via Program Slicing"](https://www.youtube.com/watch?v=dSqLt8BgbRQ).  A sequence of tests combined with program slicing generates a sequence of minimal programs of increasing complexity that defines an "idealized commit log".

### Analogy with drawing programs
There are paint type programs, like MS Paint, where the canvas is a set of pixels.
Drawing operations update the pixels on the canvas, but retain no further relationship between the pixels.
There is a linear undo buffer where operations can be undone in sequence.

The other type of drawing program is a vector drawing program, like Inkscape or the Powerpoint diagram editor.
The final image is composed of set of objects.  Points that comprise an object retain the relationships between them.
Later, the object can be edited as the object, such as resizing or rotating.   An undo buffer is also present.

Current VCS's operate much like a paint-type program - the source code text is the canvas, and changes in a commit retain no further relationship to one another.    The VCS history is equivalent to the undo buffer.

What we want is a VCS that operates more like a vector drawing program - changes in a commit retain some relationship to one another, and can be manipulated as group later on.

## Related Fields

### Refinement Calculus
Refinement calculus (https://en.wikipedia.org/wiki/Refinement_calculus) is used for converting a formal specification to an executable program through a series of steps.

### Refactoring

### Literate Programming
[Literate programming](https://en.wikipedia.org/wiki/Literate_programming) structures the program as narration to communicate with people about a program. The use of macros enables the program to be described in a different order than the compiler requires.  Or parts that are important but not central (like error handling or instrumentation) can be hidden. The problem is that the literate program must still contend with the program in its full complexity.

These approaches could be used together - a literate program can built up from simple to complex through transformations just like a non-literate program.  The main difference seems to be how changes are abstracted. Literate programs must have everything present, even if abstracted and labeled. Abstractions (macros) are built around textual substitution.  Programming by transformations doesn't require labels, but then needs another way to identify locations to change (pattern matching, etc.)

### Software Product Line
Software product line engineering relates to creating and maintaining a set of similar software (https://en.wikipedia.org/wiki/Software_product_line).

## Other Projects

### Expressions of Change
The [Expressions of Change](https://www.expressionsofchange.org/) site describes a sabbatical project by Klaas van Schelven with similar ideas, but with more theoretical grounding.  The post on [applying version control to itself](https://www.expressionsofchange.org/self-applicability/) arrives at a similar point as the 2D version control idea above.   The project explores building a language where changes are primitive building blocks.  The language is simple and based on S-expressions in order to focus on the formal aspects of program change and construction. The project also has a structured editor for creating and viewing the changes.

### Layers
Kartik Agaram has a similar idea by building programs in layers.  See the post ["A new way to organize programs"](http://akkartik.name/post/wart-layers). The technique seems to extend pretty cleanly from literate programming (the tool to do the replacements is called 'tangle'). It uses textual diffs to describe the changes, which surprised me at how far it could go. The change locations are described via matching of lines (usually in comments).   As an application and an example, the [Mu project](https://github.com/akkartik/mu) uses layers to build a simplified X86 assembly language and virtual machine to create a more comprehensible computing system.

### Comby
The Comby tool has a general syntax for matching and expressing program transformations. There is a nice live editor at https://comby.live/ .  The homepage ( https://comby.dev/ ) documents the syntax.
To learn more, watch the Strange Loop 2019 talk available on Youtube: ["Parser Parser Combinators for Program Transformation"](https://www.youtube.com/watch?v=JMZLBB_BFNg) by Rijnard van Tonder.

### Atomist
The Atomist approach is similar and looks very interesting. Code (https://github.com/atomist) and docs (http://docs.atomist.com/).   Some description here: https://the-composition.com/software-that-writes-and-evolves-software-953578a6fc36 .   It uses 'generators' to create initial code and 'editors' to manipulate existing code or projects in a structured manner.

These transformations (editors and generators) are expression in DSL called 'rug'.   The rug DSL currently works on regular expression-type matching in files, and file manipulations (create, delete, rename).  There are some language-specific file handlers (though it's not clear from the documentation if these are a full parser for the target language or not). There is also support for microgrammars for manipulating more structured content.

So far the focus of examples and editors seems to be on development and deployment of web applications and microservices.  For instance, a generator for creating a new Python project (directory layout and initial files).  The editors seem to operator more on the repository level than on the code level. (Not to say there aren't some code transformations, but they don't seem to be as numerous)



## Example

A [simple Python example](prog_by_trans_example.md).

