sink("/dev/null")
library(eco) # for Imai 2008
args = commandArgs(trailingOnly=TRUE)
data_file = ""
if (length(args)==0) {
  stop("At least one argument must be supplied.", call.=FALSE)
} else{
	data_file = args[1]
	mu0 = as.numeric(args[2])
	tau0 = as.numeric(args[3])
	nu0 = as.numeric(args[4])
	s0 = args[5]
	mustart = args[6]
	sigmastart = args[7]
}

data = read.csv(paste("../data/",(data_file),sep=""))
data = data[data$N>100,]

res.ML <-  eco(X ~ Y, N = N, data = data, context = TRUE, parameter=TRUE,n.draws = 5000, burnin = 2000, thin = 5, verbose = FALSE
	,mu0=mu0,tau0=tau0,nu0=nu0,S0=s0,mu.start=mustart,Sigma.start=sigmastart)
# out1 <-predict(res.ML,verbose=TRUE)
# last_pos = length(res.ML$W[,1,1])
# predicted_W1_strauss= res.ML$W[last_pos,1,]
# predicted_W2_strauss= res.ML$W[last_pos,2,]
predicted_W1_strauss <- numeric()
for(i in 0:length(data$N)){
  predicted_W1_strauss[i] <- mean(res.ML$W[,1,i])
}
predicted_W2_strauss <- numeric()
for(i in 0:length(data$N)){
  predicted_W2_strauss[i] <- mean(res.ML$W[,2,i])
}

write(predicted_W1_strauss, paste("../results/predicted_W1_imai",data_file,sep=""), sep = ",")
write(predicted_W2_strauss, paste("../results/predicted_W2_imai",data_file,sep=""), sep = ",")