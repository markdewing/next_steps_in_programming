
The initial goal is to create a DSL (using Sympy) to express scientific algorithms.
Some steps.

1. Use a dataflow-based executor or scheduler to tie the execution of functions and expressions together.
2. To make the language useful, it will need to have procedures and some control flow.

This should form a reasonable specification for the algorithm.  We then want to use this to analyze and compile the algorithm.
As an example analysis, create an execution path that analyzes floating point precision and could flag areas where precision loss might be a problem.

For performance, use LLVM and/or GCCJIT to compile to native code
(Some work on JIT'ing scalar sympy expressions is here: https://github.com/markdewing/sympy/tree/llvmlite ) (Despite the branch name, there is also code for GCC jit in there)
Now this will necessarily require deciding on memory layouts for the data structures, and how the abstract indexing should map to the data structure.   It would be nice if this were flexible to allow selecting different memory layouts to find the best performance.

Now we will work through the desired DSL features to see how they might work.
* List of simple expressions.
  Here is an IPython notebook that creates and evaluates a simple set of expressions: [Simple Expression Evaluation](https://github.com/markdewing/next_steps_in_programming/blob/master/eval/simple_expression_eval.ipynb)
* Functions
* Indexed values
* Vectors/Matrices
* Loops
  * Foreach
  * Convergence
  * Fixed number of steps (like time steps)
* Procedures
