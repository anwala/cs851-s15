#!/usr/bin/env Rscript

rawInputStatusCodes <- read.table('STATUS_CODE_FREQUENCY.txt', header=T)
rawInputRedirectionCounts <- read.table('REDIRECTION_COUNT_FREQUENCY.txt', header=T)
rawInputAge <- read.table('DELTA_DAYS.txt', header=T)

binsStatusCodes <- 
c(
200,
204, 
301,
302,
307,
406,
405,
404,
403,
400,
504,
503,
500 
)

binsRedirectionCounts <-
c(
0,
1,
2,
3,
4,
6,
1443
)

barplot( rawInputStatusCodes$STATUS_CODE_FREQUENCY, las=2, names=binsStatusCodes, xlab="Status Codes", ylab="Frequency", main="Chart 1: Distribution of HTTP status codes", col="lightblue")
barplot( rawInputRedirectionCounts$REDIRECTION_COUNT_FREQUENCY, las=2, names=binsRedirectionCounts, xlab="Redirection Counts", ylab="Frequency", main="Chart 2: Distribution of Redirection Counts", col="lightblue")
hist( rawInputAge$AGE_DIFFS_DAYS, xlab="Age Values (days)", ylab="Frequency", main="Chart 3: Distribution of Age (TweetDateTime - Est. DateTime)", col="lightblue")

mean( rawInputAge$AGE_DIFFS_DAYS )
median( rawInputAge$AGE_DIFFS_DAYS )
sd( rawInputAge$AGE_DIFFS_DAYS )
std <- function(x) sd(x)/sqrt(length(x))
std(rawInputAge$AGE_DIFFS_DAYS)