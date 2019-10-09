double A = 0.0;

double B = 1.0;

int N = 100;

double f(double x){
    return pow(x,3);
}

double x(int i){
    return A + (B - A) * drand48();
}



void StandardError_and_Integral_and_Variance(double &StandardError,double &Integral,double &Variance){
    double sum = 0.0;
    double sum2 = 0.0;
    int i;
    for (i = 1;i <= N;i++) {
        double tmp = f(x(i));
        sum += tmp;
        sum2 += tmp * tmp;
    }
    double tmp2 = (1.0 / N) * sum;
    Variance = (1.0 / N) * sum2 - tmp2 * tmp2;
    StandardError = sqrt(Variance / (N - 1.0));
    Integral = (1.0 / N) * sum;
}
