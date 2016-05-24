#!/usr/bin/env Rscript
library(ei) # for king 97
args = commandArgs(trailingOnly=TRUE)
data_file = ""
if (length(args)==0) {
  stop("At least one argument must be supplied.", call.=FALSE)
} else{
	data_file = args[1]
	er = as.numeric(args[2])
	es= as.numeric(args[3])
	eb  = as.numeric(args[4])
}

data = read.csv(paste("../data/",(data_file),sep=""))
data = data[data$N>100,]

dbuf = ei(formula=X ~ Y ,total="N",data=data,truth=cbind(data$W1,data$W2), sample = 5000, burnin = 2000, thin = 5, erho = er, esigma = es, ebeta = eb)
predicted_W1_king  <- eiread(dbuf, "betab")
predicted_W2_king  <- eiread(dbuf, "betaw")
write(predicted_W1_king, paste("../results/predicted_W1_king",data_file,sep=""), sep = ",")
write(predicted_W2_king, paste("../results/predicted_W2_king",data_file,sep=""), sep = ",")