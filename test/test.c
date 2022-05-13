void sumProd(int n){
  float sum = 0.0; // C1
  float prod = 1.0;
  float *b = &prod;
  int i = 0;
  while (i <= n)
  {sum = sum + i;
    prod = prod * i;
    foo(sum, prod);
    foo(prod, sum);
    i++;}}

float foo(float a1, float a2) {
    return a1+a2;
}