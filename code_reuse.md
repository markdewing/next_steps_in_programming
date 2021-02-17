# Code Reuse

The main mode of code reuse is through libraries.  However there are several downsides to using a library.

1. It introduces an additional dependency into a project.  The library's dependencies are now your project's dependencies.
2. Modifications or enhancements to the library require understanding a different code base
3. Projects tend to grow - in features, in breadth of support, etc.   This may not be needed in your project.  And this can cause problems from added dependencies.
Or simplying making the library harder to understand for customizations.
4. Need to integrate the entire library even if only part of the functionality is desired.
5. The library might not be compatible with things like logging or error handling, and may require extra effort to integrate.


Libraries can be including in a project through building it separately and linking.   They can also be imported as source.
For exmaple, Catch2 is distributed as a single include file that is easy to add to a project.

For some cases, I would rather write ncode into the project directly.  This makes it easier to integrate and use a precise subset.

What I want then is detailed instructions on how to write the code.  Examples of implementation, warnings of tricky parts, discussions on how to test it, etc.

Of course, this has some downsides

1. Violates Don't Repeat Yourself (DRY) principle.   Using DRY is not free, and requires coordination, integration, and linkage between the parts to be not replicated.
2. Now similar, but not identical, source is scattered over different projects.  How to easily get bug fixes or update functionality?

Some of the ideas in the rest of the document may help with this.  Programming by transformation has two potential applications - one it makes the code easier to understand.  
Secondly, the idea of applying a source transformation might help with the second downside, but making it easier to apply a bug fix.

There is always a tradeoff between rewrite and reuse.  This might shift the balance towards rewrite by making it easier to implement and maintain.

### Example applications

One area is the use of timers to profile a code.  It is very useful to have some sort of timing framework in a code.  
Often the timers are created a higher level than a function granularity, and give more information about how the programmers structure the code.
These also make convenient hooks for other things, like interfacing with vendor profilers.

Because this code is usually pretty simple, it makes integration into the project easier to write it fresh, rather than using a library.


Another area is abstraction or interface layers to parallelism and GPUs.  There's a number of technologies to provide this (Kokkos, Alpaka, Raja, HIP, OpenMP, Sycl etc.)
When architectecting an application, it's often a good idea to create an interface layer to isolate the program from things that might change.
A project either needs to commit fully to one of these technologies (which brings along all the issues of dependencies, etc.) or isolate it to give the project
more flexibility.   So the project winds up making an interface layer on top of an interface layer.    
If the project needs are simple, this is pretty straightforward.

It would be useful to have some guidance on how to write a subset of some of these technologies.

