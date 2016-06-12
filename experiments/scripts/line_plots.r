library(ggplot2)
library(reshape2)
library(plyr)

setwd("/home/Guz/Dropbox/UFMG/8º Período/POC_2/Ecological-Inference-on-social-data/evaluation") 
data = read.csv("removing_topn.csv")
# data = data[data$method == 'king',]
# data = data[data$k < 75,]
ggplot()
ggplot(data, aes(x=k, y= mae,colour=method,group=method))+
  labs(title="Sensitividade ao remover as k top-N cidades. ")+
  ylab("MAE")+
  geom_line(size=1)+
  geom_point(aes(colour=method),size=3) +
  scale_x_continuous(breaks=c(0,25,50,75))
