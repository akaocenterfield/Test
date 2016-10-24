# Newton'ss method to find root for polynomials

Fun <- function(x) {
  y = x^2 + 2*x -24
  return(y)
}

Fun_prime <- function(x) {
  y = 2*x + 2 
  return(y)
}

NewtonMethod <- function(x0) {
  x1 = (Fun_prime(x0)*x0 - Fun(x0))/Fun_prime(x0)
  return(x1)
}

N = 50 # number of iterations
x0 = -1.5 # starting point

sp = x0
for (ii in 1:N) {
  x0 = NewtonMethod(x0)
}
cat("Starting point =", sp, "   Found root =", x0, "after", N, "iterations.") # print result

