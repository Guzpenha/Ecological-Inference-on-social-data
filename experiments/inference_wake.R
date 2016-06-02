sink("/dev/null")
#!/usr/bin/env Rscript
library(MCMCpack) 
args = commandArgs(trailingOnly=TRUE)
data_file = ""
if (length(args)==0) {
  stop("At least one argument must be supplied.", call.=FALSE)
} else{
	data_file = args[1]
	m0_arg = as.numeric(args[2])
	M0_arg = as.numeric(args[3])
	m1_arg = as.numeric(args[4])
	M1_arg = as.numeric(args[5])
	a0_arg = as.numeric(args[6])
	b0_arg = as.numeric(args[7])
	a1_arg = as.numeric(args[8])
	b1_arg = as.numeric(args[9])
}
data = read.csv(paste("../data/",(data_file),sep=""))
data = data[data$N>100,]

n = length(data$Y)
post <- MCMChierEI(data$Y,(1-data$Y),data$X, (1-data$X), mcmc=5000, burnin= 2000, thin=5, verbose=1000,seed=list(NA, 1), m0= m0_arg, M0= M0_arg,m1= m1_arg, M1 = M1_arg, a0=a0_arg, b0=b0_arg,a1=a1_arg,b1=b1_arg)
predicted_W1_wake  <- colMeans(post)[1:n]
predicted_W2_wake  <- colMeans(post)[(n+1):(2*n)]

write(predicted_W1_wake, paste("../results/predicted_W1_wake",data_file,sep=""), sep = ",")
write(predicted_W2_wake, paste("../results/predicted_W2_wake",data_file,sep=""), sep = ",")