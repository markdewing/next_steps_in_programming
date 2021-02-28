# Program Comprehension

Understanding a code base is a challenge.  What can we do to make it easier?

But first, a digression on "understanding" vs. "feeling of understanding".  The canonical example is listening to a lecture in school.
The teacher covers the material and does a sample problem.  After that you feel that you understand the material and feel confident.
Then you try one of the homework problems, and it quickly becomes clear that you did not understand it as well as you thought.
How am I supposed to start on the problem?  What are the important parts?
It's the working through the confusion and getting deeply involved in the material that leads to structuring the material in your mind.

When it comes to programs, what is meant by "understanding"?  The ability to predict the behavior in your head, or at least narrown it down quickly.
Either for the purposes of fixing a bug (behavior doesn't match expected), or adding new features.  
(I imagine the education literature has more on what "understanding" means - does that carry over to programming?)

This comes in when imaging graphical representations of a program - call graphs, data flow, timeline traces, visual programming, etc.  
Because we (or at least I) imagine the program in these terms once I understand it, I imagine that having this representation from the beginning
would mean it's easier to understand a program.   
I wonder if the value in some of these artifacts is the mental effort and engagement in creating them, and not so much the end product?

Similar to essential and incidental complexity, there is essential effort and incidental effort in understanding how a program works.
Are there tools we can make that minimize incidental effort, and facilitate the essential engagement and asking questions.
Typically to understand, one starts from an example or known state, and then makes changes to see what happens.
Along these lines, can we make tools that facilite understanding how changes in the program change its behavior?

# Possible tools

### Call graph
Call graph tools are usually used for performance profiling. What's missing from call graph tools for comprehension?

Hand written diagrams documenting the program at a high level are often a very coarse call graph.
It would be nice to mechanically generate these diagrams from program executation.
I envision annotations in the source that the tool would read to group functions together, and to omit unimportant functions.
Note this is different from automtically creating a high-level or hierarchical description (through graph analysis or ML).
Those type of techniques would be interesting for research, but ultimately they would be suggestions to the humans on how
the call graph might be organized.

What's also missing is interactive editing features of the graph.   Particularly in collapsing the graph in a hierarchical way.
Sometimes I would like to group functions together and replace them with a single box (with a different or simpler name than the function)

### Timeline

Another way to understand program execution is through a timeline.   
The built-in viewer in Chrome has a fairly simple JSON format makes it easy to create timeline visualizations.

The biggest problem I have is that it is difficult to maintain a hierarchical view of what's happening.  
I would like to have multiple timeline views open at once, with different magnifications, with lines showing the connections to the magnified regions.

The other issue is loops.  Often I'd like to collapse all the iterations of a loop to one or two, so it takes up less space (easier to get the hierarchical view).


### Data use
It would be nice to know the data that gets read and written in each function - both how much and where it comes from.
In a pure functional language, the function arguments and return value would be sufficient.   
Much code is written in C++, so the data can come from function arguments, member variables, or global variables.
Even each of these may have additional accesses through structure members.

