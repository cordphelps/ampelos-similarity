
plotBugPercentages <- function(list, spidersOnly) {
  # from bug-library.R
  #
  # dfAraneae <- dplyr::union(dfCrab, dfOther)  
  # one row for each spider; columns are percent for each week
  dfAraneae <- list[[1]]
  #
  #    otherPct spiderPct sumPct week  family
  #1     19.19      2.37  21.56   23 Araneae
  #2     27.71      0.11  27.82   24 Araneae
  #3     14.70      0.68  15.38   25 Araneae
  #4      9.92      4.37  14.29   26 Araneae
  #5      8.66      4.33  12.99   27 Araneae
  #6     13.10      3.02  16.12   28 Araneae
  #7     10.07      9.37  19.44   29 Araneae
  #8     11.41      5.37  16.78   30 Araneae
  #9      9.12      7.43  16.55   31 Araneae
  #10     8.61      8.20  16.81   32 Araneae
  #11     1.78      3.91   5.69   34 Araneae
  
  
  dfDiptera <- list[[2]]
  dfHymenoptera <- list[[3]]
  dfHemiptera <- list[[4]]
  dfLepidoptera <- list[[5]]
  dfOther <- list[[6]]
  
  if (spidersOnly==TRUE) {
    
    gg <- ggplot() + 
      
      geom_jitter(data=dfAraneae, aes(x=week, y=both, fill = "both"), shape=21, size=3, show.legend=TRUE) +
      geom_jitter(data=dfDiptera, aes(x=week, y=dipteraPct, fill = 'dipteraPct'), shape=21, size=3, show.legend=TRUE) +
      
      scale_fill_manual(name = "", values = c("both" = "green", "dipteraPct" = "royalblue")) +
      
      ylim(c(0, 30)) + 
      expand_limits(y=c(0,40)) + 
      
      scale_y_continuous(breaks = seq(min(0), max(40), by = 5)) +
      scale_x_continuous(breaks=seq(22,40,2)) + 
      
      labs(y="sampled population (percent)", 
           x="week",
           caption = paste("Araneae (green), Diptera (blue)", sep="") ) +
      
      theme_bw() +
      
      theme(legend.title = element_blank(),
            legend.spacing.y = unit(0, "mm"), 
            legend.position="none",
            legend.justification=c(1,0),
            panel.border = element_rect(colour = "black", fill=NA),
            aspect.ratio = 1, axis.text = element_text(colour = 1, size = 12),
            legend.background = element_blank(),
            legend.box.background = element_rect(colour = "black")) 
    
    setwd("/Users/rcphelps/code/groq/")
    saveGGpng(filename="f.pop.araneae.png", subdir="png.output", gg=gg)
    
  } else {
    
    
    gg <- ggplot() + 
      
      geom_jitter(data=dfOther, aes(x=week, y=sumPct, fill = family), shape=21, size=3, show.legend=TRUE) +
      geom_jitter(data=dfAraneae, aes(x=week, y=sumPct, fill = family), 
                  shape=21, size=3, show.legend=TRUE) +
      geom_jitter(data=dfDiptera, aes(x=week, y=sumPct, fill = family), 
                  shape=21, size=3, show.legend=TRUE) +
      geom_jitter(data=dfHymenoptera, aes(x=week, y=sumPct, fill = family), 
                  shape=21, size=3, show.legend=TRUE) +
      geom_jitter(data=dfHemiptera, aes(x=week, y=sumPct, fill = family), 
                  shape=21, size=3, show.legend=TRUE) +
      geom_jitter(data=dfLepidoptera, aes(x=week, y=sumPct, fill = family), 
                  shape=21, size=3, show.legend=TRUE) +
      
      scale_fill_manual(name = 'insect family', 
                        values = c('white','green', 'royalblue', 'darkorange', 'lightgrey', 'lightgrey'), 
                        breaks = c("Other", 'Araneae', 'Diptera', 'Hymenoptera', 'Hemiptera', 'Lepidoptera'),
                        labels = c("other", "Araneae", 'Diptera', 'Hymenoptera', 'Hemiptera', 'Lepidoptera')) +
      
      ylim(c(0, 100)) + 
      expand_limits(y=c(0,100)) + 
      
      scale_y_continuous(trans='log10') +
      annotation_logticks(sides='l') +
      
      scale_x_continuous(breaks=seq(22,40,2)) + 
      
      labs(y="sampled population (percent)", 
           x="week",
            caption = paste("Araneae (green), Diptera (blue), Hymenoptera (orange)\n", 
                           "Hemiptera and Lepidoptera (grey), 'other' (white)", sep="") ) +
      
      theme_bw() +
      
      theme(legend.title = element_blank(),
            legend.spacing.y = unit(0, "mm"), 
            legend.position="none",
            legend.justification=c(1,0),
            panel.border = element_rect(colour = "black", fill=NA),
            aspect.ratio = 1, axis.text = element_text(colour = 1, size = 12),
            legend.background = element_blank(),
            legend.box.background = element_rect(colour = "black")) 
    
    setwd("/Users/rcphelps/code/groq/")
    saveGGpng(filename="f.pop.abundance.png", subdir="png.output", gg=gg)
    
  }
  
  return(gg)
  
}


createFamilyPercentages <- function(list) {
  # from bug-library.R
  # given the dataframe and a list of columns returned by scanBugPercentages, organize percentages 
  # by individual families, return dataframes for each family of insects showing pct by week 
  
  #        list[[1]]   # dataframe with all the data : count and percent by week (columns) for each bug (rows)
  #        list[[2]]   # list of columns that contain the weekly percentages
  #        list[[3]]   # vector of week numbers
  
  dfBase <- list[[1]] %>% dplyr::select(bugNames)  # one column of bugNames
  
  for (i in 1:length(list[[2]])) {    # get the percentage columns
    
    temp.df <- list[[1]] %>% dplyr::select(list[[2]][[i]])
    
    dfBase <- dplyr::bind_cols(dfBase, temp.df)
    
  }
  
  # dfBase is now columns of weekly insect pct and rows for each insect
  # we are transforming the data into dataframes for 'families' of specific insects
  # 
  # each will be the sum of the percentages for each species in the family
  #
  # dfAraneae :      columns:   otherPct   spiderPct   avePct    week
  #
  
  dfCrab <- dfBase %>% dplyr::filter(bugNames == 'Thomisidae..crab.spider.')  # remove all insects except spiders
  dfOther <- dfBase %>% dplyr::filter(bugNames == 'spider.other') 
  dfAraneae <- dplyr::union(dfCrab, dfOther)  # one row for each spider; columns are percent for each week
  dfAraneae <- squashFlip(df=dfAraneae, weekList=list[[3]], columnList=c('otherPct', 'spiderPct', 'week'))
  dfAraneae$family <- 'Araneae'
  dfAraneae$both <- dfAraneae$otherPct + dfAraneae$spiderPct
  
  dfDiptera <- dfBase %>% dplyr::filter(bugNames == 'Diptera..Agromyzidae..leafminer..') 
  dfDiptera <- squashFlip(df=dfDiptera, weekList=list[[3]], columnList=c('dipteraPct', 'week'))
  dfDiptera$family <- 'Diptera'
  
  dfH1 <- dfBase %>% dplyr::filter(bugNames == 'Braconid.wasp')
  dfH2 <- dfBase %>% dplyr::filter(bugNames == 'Halictus.sp....3.part..native.bee.')
  dfH3 <- dfBase %>% dplyr::filter(bugNames == 'Agapostemon.sp....green..native.bee.')
  dfH4 <- dfBase %>% dplyr::filter(bugNames == 'Osmia.sp...native.bee.')
  dfH5 <- dfBase %>% dplyr::filter(bugNames == 'Honey.Bee')
  dfH6 <- dfBase %>% dplyr::filter(bugNames == 'Bombus.californicus..bumble.')
  dfHymenoptera <- dplyr::union(dfH1, dfH2)
  dfHymenoptera <- dplyr::union(dfHymenoptera, dfH3)
  dfHymenoptera <- dplyr::union(dfHymenoptera, dfH4)
  dfHymenoptera <- dplyr::union(dfHymenoptera, dfH5)
  dfHymenoptera <- dplyr::union(dfHymenoptera, dfH6)
  dfHymenoptera <- squashFlip(df=dfHymenoptera, weekList=list[[3]], columnList=c('a', 'b', 'c', 'd', 'e', 'f', 'week'))
  dfHymenoptera$family <- 'Hymenoptera'
  
  dfHe1 <- dfBase %>% dplyr::filter(bugNames == 'Lygus.hesperus..western.tarnished.plant.bug.')
  dfHe2 <- dfBase %>% dplyr::filter(bugNames == 'pentamonidae...stinkBug.')
  dfHemiptera <- dplyr::union(dfHe1, dfHe2)
  dfHemiptera <- squashFlip(df=dfHemiptera, weekList=list[[3]], columnList=c('a', 'b', 'week'))
  dfHemiptera$family <- 'Hemiptera'
  
  dfLep1 <- dfBase %>% dplyr::filter(bugNames == 'checkerspot.butterfly')
  dfLep2 <- dfBase %>% dplyr::filter(bugNames == 'Pyralidae..Snout.Moth.') 
  dfLepidoptera <- dplyr::union(dfLep1, dfLep2)
  dfLepidoptera <- squashFlip(df=dfLepidoptera, weekList=list[[3]], columnList=c('a', 'b', 'week'))
  dfLepidoptera$family <- 'Lepidoptera'
  
  dfOther1 <- dfBase %>% dplyr::filter(bugNames == 'Orius..pirate.bug.')
  dfOther2 <- dfBase %>% dplyr::filter(bugNames == 'Diabrotica.undecimpunctata..Cucumber.Beetle.')
  dfOther3 <- dfBase %>% dplyr::filter(bugNames == 'other')
  dfOther4 <- dfBase %>% dplyr::filter(bugNames == 'ladyBug')
  dfOther5 <- dfBase %>% dplyr::filter(bugNames == 'pencilBug')
  dfOther <- dplyr::union(dfOther1, dfOther2)
  dfOther <- dplyr::union(dfOther, dfOther3)
  dfOther <- dplyr::union(dfOther, dfOther4)
  dfOther <- dplyr::union(dfOther, dfOther5)
  dfOther <- squashFlip(df=dfOther, weekList=list[[3]], columnList=c('a', 'b', 'c', 'd', 'e', 'week'))
  dfOther$family <- 'Other'
  
  
  if (FALSE) {  # a manual verification that the percentages sum to 1
    
    dfAraneae.temp <- dfAraneae %>% dplyr::select(sumPct)       # that's a dataframe every column except week
    dfDiptera.temp <- dfDiptera %>% dplyr::select(sumPct)
    dfHymenoptera.temp <- dfHymenoptera %>% dplyr::select(sumPct) 
    dfHemiptera.temp <- dfHemiptera %>% dplyr::select(sumPct) 
    dfLepidoptera.temp <- dfLepidoptera %>% dplyr::select(sumPct) 
    dfOther.temp <- dfOther %>% dplyr::select(sumPct) 
    
    dfTotal <- dplyr::bind_cols(dfDiptera.temp, dfHymenoptera.temp)
    dfTotal <- dplyr::bind_cols(dfTotal, dfHemiptera.temp)
    dfTotal <- dplyr::bind_cols(dfTotal, dfLepidoptera.temp)
    dfTotal <- dplyr::bind_cols(dfTotal, dfOther.temp)
    dfTotal <- dplyr::bind_cols(dfTotal, dfAraneae.temp)
    
    
    dfTotal <- transform(dfTotal, sum = rowSums(dfTotal, na.rm = TRUE))
    
    
  }
  
  returnList <- list()
  returnList[[1]] <- dfAraneae
  returnList[[2]] <- dfDiptera
  returnList[[3]] <- dfHymenoptera
  returnList[[4]] <- dfHemiptera
  returnList[[5]] <- dfLepidoptera
  returnList[[6]] <- dfOther
  
  return(returnList)
  
}


scanBugPercentages <- function(df) {
  # from bug-library.R
  # calculate count and percent by week (columns) for each bug (rows)
  
  if (FALSE) {
    
    df <- bugs.df
    
  }
  
  weeks.vector <- getWeeks(df)
  bugList <- colnames(df[,5:22])
  
  bugPct <- as.data.frame(df %>% select(5:22) %>% names())   # bug names as first column
  # disapointing : https://stackoverflow.com/questions/42769650/how-to-dplyr-rename-a-column-by-column-index
  # bugPct <- bugPct %>% rename_at( 1, ~"column1" ) %>% tibble::column_to_rownames('column1')
  bugPct <- bugPct %>% rename_at( 1, ~"bugNames" )  # 
  
  pctColNames <- list()
  
  for (i in 1:length(weeks.vector)) {
    
    trim.tbl <- as.data.frame(df %>% filter(week == weeks.vector[[i]]) %>% select(5:22) %>% colSums()) # append column representing totals 
    # of each insect for week i
    trim.tbl <- cbind(trim.tbl,round(prop.table(trim.tbl)*100,2))  # append column representing the percent of each insect for week i
    
    colnames(trim.tbl) <- c(paste('week', weeks.vector[[i]], 'count', sep=""), paste('week', weeks.vector[[i]], 'pct', sep=""))
    rownames(trim.tbl) <- NULL
    
    pctColNames[[i]] <- paste('week', weeks.vector[[i]], 'pct', sep="")  # save the column names
    
    bugPct <- dplyr::bind_cols(bugPct, trim.tbl)
    
  }
  
  returnList <- list()
  returnList[[1]] <- bugPct        # count and percent by week (columns) for each bug (rows)
  returnList[[2]] <- pctColNames   # week23pct, week24pct, ....
  returnList[[3]] <- weeks.vector  # 23, 24, .....
  
  return(returnList)
  
}


densityNoFacets <- function(tibble, periodString) {
  
  color = c("SNH" = "royalblue2", "control" = "darkorange2")
  
  gg <- ggplot(data = tibble, aes(x = transect, y = Thomisidae..crab.spider.)) +  
    
    geom_jitter(aes(fill=transect), shape = 21, size=3) +
    
    #title = paste("thomisidae observations seasonal ", periodString, sep=""), 
    
    labs(x = periodString, 
         y = "count per trap") +
    
    theme_bw() +
    
    scale_y_continuous(limits= c(0,4), breaks = seq(0, 4, 1)) +
    
    scale_fill_manual(values = color, breaks = c("SNH", "control"), labels = c("SNH", "control")) +
    
    theme(legend.position="none") 
  
  return(gg)
}


densityFacets <- function(tibble, periodString) {
  
  color = c("SNH" = "royalblue2", "control" = "darkorange2")
  
  gg <- ggplot(data = tibble, aes(x = positionX, y = Thomisidae..crab.spider.)) + 
  #gg <- ggplot(data = tibble, aes(x = positionX / 3.281, y = Thomisidae..crab.spider.)) +
    
    geom_jitter(aes(fill=transect), shape = 21, size=3) +
    
    facet_grid(~transect) +
    #scale_x_continuous(breaks = seq(0, 200, 1)) +
    
    labs(title = paste("thomisidae observations seasonal ",
                       periodString, sep=""),
         x = "trap distance from field edge (ft)", 
         y = "count per trap") +
    
    theme_bw() +
    
    scale_y_continuous(breaks = seq(0, 4, 1)) +
    
    scale_fill_manual(values = color, breaks = c("SNH", "control"), labels = c("SNH", "control")) +
    
    theme(legend.position="none") 
  
  return(gg)
  
}


plotRawWeeklyV2 <- function(day, night, tr) {
  
  
  
  # plot daily spider counts, by week, differentiate by time
  
  # input 2 dataframes :
  #  week, transect, time{am, pm}, totalSpiders
  #
  
  # > head(total.df, 10)
  #   week  transect time totalSpiders
  #1    23 oakMargin   am             2
  #2    23 oakMargin   am             6
  #3    23 oakMargin   am             2
  #4    23 oakMargin   am             4
  #5    23 oakMargin   am             2
  #6    23 oakMargin   am             3
  #7    23 oakMargin   pm             1
  #8    23 oakMargin   pm             7
  #9    23 oakMargin   pm            14
  #10   23 oakMargin   pm             5
  
  color_list <- list("royalblue4", "royalblue3", "royalblue2", "darkorange4", "darkorange3", "darkorange2")
  
  if (tr == "control") {
    time = c("pm" = "darkorange4", "am" = "darkorange2")
  } else {
    time = c("pm" = "royalblue4", "am" = "royalblue2")
  }
  
  gg <- ggplot() + 
    
    geom_jitter(data=day, aes(x=week, y=totalSpiders, fill=time), 
                size=5, shape=21, alpha=.7, show.legend=TRUE, width=.2, height=.2) +
    
    geom_jitter(data=night, aes(x=week, y=totalSpiders, fill=time), 
                size=5, shape=21, alpha=.7, show.legend=TRUE, width=.2, height=.2) +
    
    geom_vline(xintercept=25.5) + # seasonal timeframe seperators
    geom_vline(xintercept=31.5) + #
    
    ylim(c(0, 31)) + 
    expand_limits(y=c(0,31)) + 
    coord_fixed(ratio=1/4) +     # control the aspect ratio of the output; "ratio" refers to the 
    # ratio of the axis limits themselves
    
    scale_y_continuous(breaks = seq(min(0), max(65), by = 5)) +
    scale_x_continuous(breaks=seq(22,40,2)) + 
    
    # labs(title=paste("total spiders trapped by week", sep=""),
    labs(
      y="counts", 
      x="week", 
      caption = paste(where, " transect population activity\nby collection time in three\nobserved seasonal periods", 
                      sep="") ) +
    
    theme_bw() +
    
    #scale_fill_manual(values = colours, 
    #                  breaks = c("am", "pm"),
    #                  labels = c("overnight", "daytime")) +
    
    theme(legend.title = element_blank(),
          legend.spacing.y = unit(0, "mm"), 
          legend.position="none",
          legend.justification=c(1,0),
          panel.border = element_rect(colour = "black", fill=NA),
          aspect.ratio = 1, axis.text = element_text(colour = 1, size = 12),
          legend.background = element_blank(),
          legend.box.background = element_rect(colour = "black")) 
  
  
  
  return(gg)
  
}

plotCountsWeeklyV3 <- function(day, night, tr) {
  
  # derived from plotRawWeeklyV2
  
  # plot daily spider counts, by week, differentiate by time
  
  # input 2 dataframes :
  #  week, transect, time{am, pm}, totalSpiders
  #
  
  # > head(total.df, 10)
  #   week  transect time   crabSpiders
  #1    23 oakMargin   am             2
  #2    23 oakMargin   am             6
  #3    23 oakMargin   am             2
  #4    23 oakMargin   am             4
  #5    23 oakMargin   am             2
  #6    23 oakMargin   am             3
  #7    23 oakMargin   pm             1
  #8    23 oakMargin   pm             7
  #9    23 oakMargin   pm            14
  #10   23 oakMargin   pm             5
  
  color_list <- list("royalblue4", "royalblue3", "royalblue2", "darkorange4", "darkorange3", "darkorange2")
  
  if (tr == "control") {
    time_colors = c("pm" = "darkorange4", "am" = "darkorange2")
  } else {
    time_colors = c("pm" = "royalblue4", "am" = "royalblue2")
  }
  
  gg <- ggplot() + 
    
    geom_jitter(data=day, aes(x=week, y=crabSpiders, fill=time),
                size=5, shape=21, alpha=.7, show.legend=TRUE, width=.2, height=.2) +
    
    geom_jitter(data=night, aes(x=week, y=crabSpiders, fill=time), 
                size=5, shape=21, alpha= 1 , show.legend=TRUE, width=.2, height=.2) +
    
    scale_fill_manual(values = time_colors) +
    
    geom_vline(xintercept=25.5) + # seasonal timeframe seperators
    geom_vline(xintercept=31.5) + #
    
    ylim(c(0, 31)) + 
    expand_limits(y=c(0,31)) + 
    
    scale_y_continuous(breaks = seq(min(0), max(85), by = 10)) +
    
    labs(
      y="counts", 
      x="week", 
      caption = paste(" transect: ",  tr, sep="") ) +
    
    theme_bw() +
    
    theme(legend.title = element_blank(),
          legend.spacing.y = unit(0, "mm"), 
          legend.position="none",
          legend.justification=c(1,0),
          panel.border = element_rect(colour = "black", fill=NA),
          aspect.ratio = 1, axis.text = element_text(colour = 1, size = 12),
          legend.background = element_blank(),
          legend.box.background = element_rect(colour = "black")) 
  
  
  
  return(gg)
  
}
