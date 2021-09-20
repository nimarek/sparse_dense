library(afex)
library(dplyr)
library(lsmeans)
library(lmerTest)
library(ggplot2)

# set paths, load data
myPath <- 'C:/Users/Exp_psy/Desktop/sparse_dense/sequence_data/'
setwd(myPath)

temp = list.files(pattern='.txt')
myfiles = lapply(temp, read.delim)
spadens_df <- do.call(rbind, myfiles)

# start to correct the data structure
spadens_df$sNumber <- as.factor(spadens_df$sNumber)
spadens_df$RT <- as.numeric(spadens_df$RT)

# check number of observations for MRI analysis
n_dense <- nrow(spadens_df[spadens_df$dispDens == 'dense',])
n_sparse <- nrow(spadens_df[spadens_df$dispDens == 'sparse',])

n_Mixed <- nrow(spadens_df[spadens_df$disType == 'Mixed',])
n_Fixed <- nrow(spadens_df[spadens_df$disType == 'Fixed',])

n_dD <- nrow(spadens_df[spadens_df$seqType == 'dD',])
n_sD <- nrow(spadens_df[spadens_df$seqType == 'sD',])
n_sF <- nrow(spadens_df[spadens_df$seqType == 'sF',])

# remove all rows containing 'n/a' and errors
spadens_df <- spadens_df[!grepl('n/a', spadens_df$seqType),]
spadens_df <- spadens_df[!grepl('1', spadens_df$error),]
spadens_df <- na.omit(spadens_df)

# slice df into two separate dfs containing only fixed and mixed runs
spadens_df_mixed <- spadens_df[!grepl('Fixed', spadens_df$disType),]
spadens_df_fixed <- spadens_df[!grepl('Mixed', spadens_df$disType),]

                
fit_freq <- lmer(RT ~ dispDens*seqType*blockNo + (1|sNumber), data=spadens_df)
summary(fit_freq)

fit_bayes <- stan_glm(RT ~ dispDens*seqType*blockNo, data=spadens_df, chains=4, iter=10000, warmup=2500)
posteriors <- insight::get_parameters(fit_bayes)
head(posteriors)

ggplot(posteriors, aes(x = RT)) +
  geom_density(fill = "orange")