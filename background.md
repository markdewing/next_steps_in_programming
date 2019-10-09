## Background

  This is an account of my personal journey through several iterations of these ideas.

  In graduate school, I kept a Latex document with all the equations (and derivations) needed to write my research code.  Scientific papers store the information in a compressed form - it takes some reading and re-reading to unpack them.  This document stored the results of that unpacking (or at least the equations) in an uncompressed form, to make it all more plainly visible.  One problem is that I still had to manually type the expressions into the computer program (Fortran, at the time).   That step was still error-prone - it would be much better to store the equations in a better format (than Latex), and convert them to code automatically.
(The document is here, for Quantum Monte Carlo calculations: [Notes on the Wavefunction and Local Energy](examples/qmc_equations/eloc.pdf) )

  One first attempt used MathML to make the equations look more like math. [Programming in Mathematical Notation](http://www.markdewing.com/prog_in_math/intro.xhtml) 
  
  At this point, it looked like some sort of computer algebra system would be helpful, and I found out about the Sympy project.   I wrote some code generation, but I was not happy with how it scaled.  \<insert rant about how template approaches quickly become messy, and make it hard to reason about the final output\>
  
Languages are becoming more Unicode friendly with respect to their source code.
Greek characters and math symbols can then be used in the source.
(The Fortress language was an early leader in this.)
The source looks more like the mathematical expression it is implementing.
What always bothered me is that it isn't really a mathematical expression.
That is, it can not be transformed or manipulated like one.
So what needs to be present in the ideal system is some way to transform and analyze some expressions as symbolic algebra.


Konrad Hinsen wrote an interesting article titled "Daydreaming about Scientific Programming" ( [Computers in Science and Engineering, Sept/Oct 2013](http://scitation.aip.org/content/aip/journal/cise/15/5/10.1109/MCSE.2013.104)  [PDF](http://www.researchgate.net/profile/Konrad_Hinsen/publication/259621131_Daydreaming_about_Scientific_Programming/links/00b4952cec2738c956000000.pdf) )  It describes the system/workflow for scientfic programming that I really would like to build.

The simplest example I would like to see involves the force calculation for molecular dynamics.  The force is the derivative of the potential (well, and multiplied by -1).  For this sample, the code should compute the derivative symbolically from the expression for the potential.  (Are there any MD codes that do that?)

The next section will be concerned with building a Domain Specific Language (DSL) for representing scientific computing algorithms.
  
  
