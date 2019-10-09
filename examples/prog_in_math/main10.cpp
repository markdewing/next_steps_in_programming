
#include <stdio.h>
#include <math.h>
#include <stdlib.h>



#include "test10.cpp"

int main()
{
  double in,var,err;
  StandardError_and_Integral_and_Variance(err,in,var);
  printf("integral = %g Variance = %g Error = %g\n",in,var,err);
  return 0;
}
