double A = 0;

double B = 1;

int N = 100;

double f(double x){
    return pow(x,3);
}
double h = (B - A) / N;

double a(int i){
    return A + i * h;
}
double Integral(){
    double sum = 0.0;
    int i;
    for (i = 1;i <= N - 1;i++) {
        sum += f(a(i));
    }
    return (h / 2) * (f(a(0)) + f(a(N))) + h * sum;
}
