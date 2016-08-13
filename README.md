# Ecological inference, a comparison of methods on social data


## Abstract 

*Online Social Networks have recently become extremely popular and generates a huge volume of spontaneous data, making it possible to obtain fast feedback over different topics, such as a brand or a political candidate. Understanding demographics of these users can provide useful information (e.g. marketing campaign segmentation) and as a consequence approaches to infer such characteristics have already been proposed in literature. Unlike most of them that model this problem as a supervised learning classifier which infers users characteristics individually, we propose the use of Ecological Inference for understanding demographics of groups of users.  We consider the problem of inferring user demographics (gender and age) of users who supported Brazilian president Dilma Rousseff in Twitter during an interval of political disturbance in the country by comparing three methods of Ecological Inference over a thorough experimental evaluation.  Our results show that the solution with the best predictions in the context of our social data is (KING, 1997), tying statistically  with (IMAI,2008) only in a few configurations of the dataset. Furthermore, we show that geographic units with higher user samples yields lower errors than cities with smaller samples and even though the support for Dilma decreased over the time interval of the crawling, the errors difference between Ecological Inference methods of aggregated data and time sliced data are not statistically significant. Finally we present a comparison of the Ecological Inference methods between a standard electoral benchmark and our social generated dataset.*


## Data

Age and social 2x2 tables for support for Dilma from Twitter collected between dates 25/11/2015 and 25/03/2016. Ecological Inference variables Y	X	W1 W2	N for both variables.

### Gender
* Y = % of male citizens in city\n
* X = % of users who publish positive posts about Dilma
* W1 = % of male who publish positive posts about Dilma
* W2 = % of female who publish positive posts about Dilma
* N = Number of users sampled
    
### Age
* Y = % of people with less than 40 years in city
* X = % of users who publish positive posts about Dilma
* W1 = % of people with less than 40 years who publish positive posts about Dilma
* W2 = % of people with less than 40 years who publish positive posts about Dilma
* N = Number of users sampled

## Experiments

Python and R scripts for comparing models and hypothesis testing.
