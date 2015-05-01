#!/usr/bin/env Rscript

similarityValues <- read.table('sim1Plot.txt', header=T)

# Create the data.
a <- similarityValues$Sim1

# Set colors for the CDF.
aCDFcolor <- rgb(1,0,0)

plot(a, type = 'l', ylim = c(0, 1), xlab = 'Dates', ylab = 'Similarity', main = '\nChart 3: Jaccard Distance Relative to first Memento for
	tinyurl.com from \nMon, 13 Oct 2008 to Wed, 29 Apr 2015\n', col=aCDFcolor)


#For each of the 3 cases (i.e., 1-, 2-, 3-grams) build a Cumulative Distribution Function that shows the % change on the x-axis & the % of the population on the x-axis 
