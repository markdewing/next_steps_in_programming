## Background

  This is an account of my personal journey through several iterations of these ideas.

  In graduate school, I kept a Latex document with all the equations (and derivations) needed to write my research code.  Scientific papers store the information in a compressed form, and I wanted all the equations in an uncompressed form, to make it all plainly visible.  One problem is that I still had to manually type the expressions into the computer program (Fortran, at the time).   That step was still error-prone - it would be much better to store the equations in a better format (than Latex), and convert them to code automatically.
(The document is here: [Notes on the Wavefunction and Local Energy](http://www.markdewing.com/qmc/eloc/eloc.pdf)

  One first attempt used MathML to make the equations look more like math. [Programming in Mathematical Notation](http://www.markdewing.com/prog_in_math/intro.xhtml) 
  
  At this point, it looked like some sort of computer algebra system would be helpful, and I found out about the Sympy project.   I wrote some code generation, but I was not happy with how it scaled.  \<insert rant about how template approaches quickly become messy, and make it hard to reason about the final output\>
  
  
  
