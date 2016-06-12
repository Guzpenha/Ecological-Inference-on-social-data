library(ggplot2)
library(reshape2)
library(plyr)

setwd("/home/Guz/Dropbox/UFMG/8º Período/POC_2/Ecological-Inference-on-social-data/evaluation") 
nsize_groups = read.csv("sensitivy_to_nsize_group.txt")
timebox_groups = read.csv("sensitivity_to_timebox_group.txt")
ggplot(timebox_groups, aes(names, mean)) +   
  geom_bar(aes(fill = Grupo), position = "dodge", stat="identity")+
  geom_errorbar(aes(fill = Grupo,ymin= bt, ymax= up), width=.1,position=position_dodge(.9))+facet_grid(~Dataset)+
  # labs(title ="Sensitivade aos grupos de N") + xlab("Método") + ylab("MAE")+facet_grid(~Dataset)
  labs(title ="Sensitivade aos grupos por janela de tempo") + xlab("Método") + ylab("MAE")+facet_grid(~Dataset)

