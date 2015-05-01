#!/usr/bin/env Rscript

similarityValues <- read.table('nGramSimilarity.txt', header=T)

# Create the data.
a <- similarityValues$oneGramSim
b <- similarityValues$twoGramSim
c <- similarityValues$threeGramSim

# Set colors for the CDF.
aCDFcolor <- rgb(1,0,0)
bCDFcolor <- rgb(0,1,0)
cCDFcolor <- rgb(0,0,1)

# Create a single chart with all 3 CDF plots.
#plot(ecdf(a), col=aCDFcolor, main=NA)
#plot(ecdf(b), col=bCDFcolor, add=T)
#plot(ecdf(c), col=cCDFcolor, add=T)
n = sum(!is.na(similarityValues$oneGramSim))

oneGramSim = sort(similarityValues$oneGramSim)
twoGramSim = sort(similarityValues$twoGramSim)
threeGramSim = sort(similarityValues$threeGramSim)

plot((1:n)/n, oneGramSim, type = 'b', ylim = c(0, 1), xlab = 'Percent Population', ylab = 'Percent Similarity', main = 'Chart 1: Empirical Cummulative Distribution\n1-, 2-, 3- grams similarity between page pairs at time points: \nMarch 29, 2015 and April 10, 2015', col=aCDFcolor)
par(new=TRUE)
plot((1:n)/n, twoGramSim, type = 'l', ylim = c(0, 1), xlab = '', ylab = '', main = '', col=bCDFcolor)
par(new=TRUE)
plot((1:n)/n, threeGramSim, type = 'l', ylim = c(0, 1), xlab = '', ylab = '', main = '', col=cCDFcolor)

text(0.23, 1.02, '>= 22% have undergone 0% change (100% similar)', pos=4, col='black')
text(0.23, 1, 'x', pos=4, col='black')

text(0.16, 0.65, '>= 18% have undergone 37% (63% similar)', pos=4, col='black')
text(0.14, 0.65, 'x', pos=4, col='black')

text(0.12, 0.5, '>= 15% have 50% change (50% similar)', pos=4, col='black')
text(0.1, 0.5, 'x', pos=4, col='black')

legend('right', c('1-gram similarity', '2-gram similarity', '3-gram similarity'), fill=c(aCDFcolor, bCDFcolor, cCDFcolor), border=NA)

#For each of the 3 cases (i.e., 1-, 2-, 3-grams) build a Cumulative Distribution Function that shows the % change on the x-axis & the % of the population on the x-axis 
