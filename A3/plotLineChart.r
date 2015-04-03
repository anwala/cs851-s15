#!/usr/bin/env Rscript


TermTermFrequencyP <- read.table('plaintextTop50Terms.txt', header=T)

TermTermFrequencyH <- read.table('rawHTMLTop50Terms.txt', header=T)

plot(TermTermFrequencyP$Frequency, type='o', col='blue', xlab='Word Rank', ylab='Word Frequency', main='Distribution of terms in HTML files pre boilerplate \nremoval (red) and post boilerplate removal (blue)')

#plot(TermTermFrequencyH$Frequency, type='o', col='blue', xlab='Word Rank', ylab='Word Frequency', main='Distribution of terms in HTML files')
lines(TermTermFrequencyH$Frequency, type='o', col='red')
