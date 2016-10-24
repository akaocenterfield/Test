
input = seq(1, 20)
response = 0.3 * input - 5 + (runif(20)-0.5)
plot(input, response)

GetError <- function(input, reponse, A, b) {
  N = length(input) 
  total.error = sum((response - (A * input + b))^2) 
  return(total.error/N)
}

StepGradient <- function(input, response, A0, b0, learning.rate) {
  N = length(input) 
  A1 = A0 - learning.rate * (-2/N) * (response - A0 * input - b0) %*% input
  b1 = b0 - learning.rate * (-2/N) * sum(response - A0 * input - b0) 
  output = c(A1, b1)
  return(output)
}





Error = 100 
E_threshold = 5
max.iter = 1000000
learning.rate = 0.0001
A_new = 1
b_new = 2
ii = 1 
q1 = c()
q2 = c()
for (ii in 1:100000){
  output = StepGradient(input, response, A_new, b_new, learning.rate)
  A_new = output[1]
  b_new = output[2]
  q1 = c(q1, A_new)
  q2 = c(q2, b_new)
  Error = GetError(input, reponse, A_new, b_new)
  # if (Error <= E_threshold) {
  #   cat("A:", A_new, "b:", b_new, "   Error=", Error, "iterations=", ii, "\n")
  #   print(ii)
  #   print(Error)
  #   break
  # }
  if (ii %% 10 == 0) {
    cat("A:", A_new, "b:", b_new, "   Error=", Error, "iterations=", ii, "\n")
    cat(ii, "th iteration with E = ", Error, "\n")

  }
}
