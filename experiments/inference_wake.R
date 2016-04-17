#!/usr/bin/env Rscript
library(MCMCpack) 
args = commandArgs(trailingOnly=TRUE)
data_file = ""
if (length(args)==0) {
  stop("At least one argument must be supplied.", call.=FALSE)
} else{
	data_file = args[1]
}

data = read.csv(paste("../data/",(data_file),sep=""))
data = data[data$N>100,]

n = length(data$Y)
post <- MCMChierEI(data$Y,(1-data$Y),data$X, (1-data$X), 
                   mcmc=5000, burnin= 2000, thin=5, verbose=1000,seed=list(NA, 1))
predicted_W1_wake  <- colMeans(post)[1:n]
predicted_W2_wake  <- colMeans(post)[(n+1):(2*n)]

write(predicted_W1_wake, paste("../results/predicted_W1_wake",data_file,sep=""), sep = ",")
write(predicted_W2_wake, paste("../results/predicted_W2_wake",data_file,sep=""), sep = ",")