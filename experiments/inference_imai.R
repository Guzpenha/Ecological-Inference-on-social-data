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
	# s0 = args[5]
	# mustart = args[6]
	# sigmastart = args[7]
}

data = read.csv(paste("../data/",(data_file),sep=""))
data = data[data$N>100,]

res.ML <-  eco(X ~ Y, N = N, data = data, context = FALSE, parameter=TRUE,n.draws = 50000, burnin = 20000, thin = 9, verbose = FALSE)
out1 <-predict(res.ML,verbose=TRUE)
summary(out1)
last_pos = length(res.ML$W[,1,1])
predicted_W1_strauss= res.ML$W[last_pos,1,]
predicted_W2_strauss= res.ML$W[last_pos,2,]
write(predicted_W1_strauss, paste("../results/predicted_W1_imai",data_file,sep=""), sep = ",")
write(predicted_W2_strauss, paste("../results/predicted_W2_imai",data_file,sep=""), sep = ",")