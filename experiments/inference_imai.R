library(eco) # for Imai 2008
args = commandArgs(trailingOnly=TRUE)
data_file = ""
if (length(args)==0) {
  stop("At least one argument must be supplied.", call.=FALSE)
} else{
	data_file = args[1]
}

data = read.csv(paste("../data/",(data_file),sep=""))
data = data[data$N>100,]


res.ML <-  eco(X ~ Y, N = N, data = data, context = TRUE, parameter=TRUE,
	n.draws = 5000, burnin = 2000, thin = 5, verbose = TRUE)
last_pos = length(res.ML$W[,1,1])
predicted_W1_strauss= res.ML$W[last_pos,1,]
predicted_W2_strauss= res.ML$W[last_pos,2,]
write(predicted_W1_strauss, paste("../results/predicted_W1_imai",data_file,sep=""), sep = ",")
write(predicted_W2_strauss, paste("../results/predicted_W2_imai",data_file,sep=""), sep = ",")