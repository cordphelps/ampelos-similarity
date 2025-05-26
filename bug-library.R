
suppressPackageStartupMessages(library(dplyr))

library(ggplot2)
library(ggridges)
library(gridExtra)

library(dplyr)
library(rlang) # see sym()
#Attaching package: ‘dplyr’
#The following objects are masked from ‘package:stats’:
#    filter, lag
#The following objects are masked from ‘package:base’:
#    intersect, setdiff, setequal, union
# protect dplyr function select()
# https://stackoverflow.com/questions/35839408/r-dplyr-drop-multiple-columns
#detach( "package:MASS", unload = TRUE )
#detach( "package:skimr", unload = TRUE )
# get loaded packages with sessionInfo()
# get versions: packageVersion("dplyr")
library(tidyverse)
library(knitr)
library(kableExtra)

savePDF <- function(image, filenameNoExt) {
   
  filename <- paste("./output/", filenameNoExt, ".pdf", sep="")
  
  # 6 inches = 15.24 cm
  ggsave(filename, plot = image,
         width = 15.24, height = 10.16, units = "cm")
  
}


saveGGpng <- function(filename, subdir, gg) {
  
  wd <- getwd() 
  
  # Check if the subdirectory exists
  if (dir.exists(file.path(subdir))) {
    
    dirPath <- paste(wd, "/", subdir, sep="")
    fullPath <- paste(dirPath, "/", filename, sep="")
    
    if (file.exists(fullPath)) { file.remove(fullPath) }
    
    suppressMessages(ggsave(filename, plot = gg, device = NULL, path = dirPath,
                            scale = 1, width = 3.5, height = 3.5, dpi = 300, limitsize = TRUE,
                            units = "in") )
    
    print(paste( "saved ", fullPath, sep=" "))
    
  } else {
    
    print(paste("subdirectory ", subdir, " does not exist", sep=""))
    
  }
  
  return()
  
}

# ==================================================================================

saveDFpng <- function(filename, subdir, df) {
  
  library(gridExtra)
  library(grid)
  
  wd <- getwd() 
  
  # Check if the subdirectory exists
  if (dir.exists(file.path(subdir))) {
    
    dirPath <- paste(wd, "/", subdir, sep="")
    fullPath <- paste(dirPath, "/", filename, sep="")
    
    if (file.exists(fullPath)) { file.remove(fullPath) }
    
    library(gridExtra)
    library(png)
    # Save the table as a PNG
    png(fullPath, units = "in", width = 8, height = 4, res = 72, pointsize = 10)
    grid.table(df, rows = NULL)
    dev.off()
    
    if (FALSE) {
      library(magick)
      # Read the PDF (first page by default)
      img <- image_read_pdf("input.pdf", density = 300)  # Higher density = better quality
      # Save as PNG
      image_write(img, path = "output.png", format = "png")
    }
    
    if (FALSE) {
      #suppressMessages(ggsave(filename, plot = gg, device = NULL, path = dirPath,
      # scale = 1, width = 8, height = NA, dpi = 300, limitsize = TRUE,
      # units = "in") )
      # Open a PDF device
      pdf(fullPath, width = 8, height = 4)  # adjust size as needed
      #
      # Create a table grob with smaller font size
      g <- tableGrob(head(df), 
                     theme = ttheme_default(core = list(fg_params = list(fontsize = 10)),
                                            colhead = list(fg_params = list(fontsize = 10)),
                                            rowhead = list(fg_params = list(fontsize = 10))))
      # Draw the table
      #grid.table(df)
      grid::grid.draw(g)
      # Close the PDF device
      dev.off()
      print(paste( "saved ", fullPath, sep=" "))
    }
    
  } else {
    
    print(paste("subdirectory ", subdir, " does not exist", sep=""))
    
  }
  
  return()
  
}




plotRidgesV2 <- function(data, combined, bugs, speciesText, when, wk, caption) {

  # https://en.wikipedia.org/wiki/Kernel_density_estimation
  #
  # https://stackoverflow.com/questions/7310186/function-in-r-passing-a-dataframe-and-a-column-name

  if (FALSE) {   # available for debug
    # https://stackoverflow.com/questions/9726705/assign-multiple-objects-to-globalenv-from-within-a-function
    assign("data", data, envir=.GlobalEnv)
    assign("bugs", bugs, envir=.GlobalEnv)

    assign("when", when, envir=.GlobalEnv)
    assign("wk", wk, envir=.GlobalEnv)
    assign("caption", caption, envir=.GlobalEnv)
  }
  
  # https://cran.r-project.org/web/packages/ggridges/vignettes/introduction.html
  
  if (wk < 23 | wk > 52) {  # we definitely don't have a valid week
    # this case indicates 'use data from all weeks'
    cumulative <- "(cumulative)"
    
    if (when != "am" & when != "pm") {    # use all the data (am and pm) for each day
      #filteredBugs.df <- filter(data, transect == where)
    } else {                              # use partial data (am or pm) for each day
      filteredBugs.df <- filter(data, time == when)
    }
    
  } else {  #  we might have a 'valid' week (data for the specified week could be
    #  missing....)
    cumulative <- as.character(wk)
    
    if (when != "am" & when != "pm") {   # use all the data (am and pm) for each day
      filteredBugs.df <- filter(data, week == wk)
    } else {                             # use partial data (am or pm) for each day
      filteredBugs.df <- filter(data, time == when & week == wk)
    }
    
    
  }
  
  
  # simplify to include the trap position and the bug in the list
  newBugs.df <- subset(filteredBugs.df, select= c("positionX", "transect", bugs))

  # exclude counts == 0
  newBugs.df <- newBugs.df %>% dplyr::filter(newColumn > 0)
  
  ################################################################################################
  # get some stats to add to the plot

  # note: nuance of using the > operator and sum()
  # As a result you can SUM over this to find the number of values which are TRUE (>2000), 
  # ie Count. While you may have been expecting this input to SUM the actual values themselves
  # https://stackoverflow.com/questions/22690255/count-observations-greater-than-a-particular-value

  spider_rows <- nrow(newBugs.df)
  trapsWithSpiders <- nrow(newBugs.df[newBugs.df[,bugs] > 0, ])
  # trapsWithSpiders <- sum(newBugs.df[,bugs])
  percentOcurrence <- (trapsWithSpiders / spider_rows) * 100
  # https://stackoverflow.com/questions/3443687/formatting-decimal-places-in-r
  percentOcurrence <- format(round(percentOcurrence, 2), nsmall = 2)

  ################################################################################################
  
  # get factors for geom_density_ridges
  # (grouping by "count")
  factor.list <- newBugs.df[,bugs]   #     
  newBugs.df$geomFactors <- NULL                        
  newBugs.df$geomFactors <- as.factor(factor.list)
  
  # assign("newBugs.df", newBugs.df, envir=.GlobalEnv)
  
  #Density plots can be thought of as plots of smoothed histograms.
  #The smoothness is controlled by a bandwidth parameter that is analogous 
  #to the histogram binwidth.
  #Most density plots use a kernel density estimate, but there are other 
  #possible strategies; qualitatively the particular strategy rarely matters.
  # https://homepage.divms.uiowa.edu/~luke/classes/STAT4580/histdens.html
  
  if (combined == FALSE) {
    # the x axis data is multi-level
  gg2 <- ggplot(newBugs.df, aes_string(x="positionX", y="geomFactors", fill="geomFactors")) +
    geom_density_ridges(
      #aes(point_color = spider, point_fill=spider, point_shape=spider),
      # https://stackoverflow.com/questions/22309285/how-to-use-a-variable-to-specify-column-name-in-ggplot
      aes_string(point_color = "geomFactors", point_fill="geomFactors", point_shape="geomFactors"),
      alpha = .2, jittered_points = TRUE, show.legend=F, scale = 0.9) +

      scale_point_color_hue(l = 40)  +
      scale_discrete_manual(aesthetics = "point_shape", values = c(21, 22, 23, 24, 25) ) +
    
      xlim(1,10) +
      # http://ggplot2.tidyverse.org/reference/sec_axis.html
      scale_x_continuous(position='top',
        breaks=seq(4,200,16), 
        sec.axis = sec_axis(~.*.3048,
        breaks= seq(0, 70, 10),
        name= "trap distance from row start (m)"))  +

      guides(fill = guide_legend(override.aes = list(size = 5, alpha = 1))) + 

      labs(x="trap distance from row start (ft)",
         y= paste(speciesText, "\nobservations with spiders", sep=""),
 
         caption=paste(speciesText, " probability density\n", 
                      "transect: ", where, "collection time: ", when, 
                      "\ntotal ", speciesText,  " observations: ", spider_rows, 
                      "\ntraps with ", speciesText, "s: ", percentOcurrence, " %",
                      sep="")) +

      scale_fill_manual(values = c("1" = "red", "2" = "green", "3" = "blue"), 
                        breaks = c("oakMargin", "control"),
                        labels = c("SNH", "control")) +

      scale_shape_manual(values = 21) +

      theme(panel.grid.minor=element_blank()) +  # hide the minor gridlines
      theme(axis.title.y = element_text(angle = 90, vjust=.5)) +
      theme_bw()

  } else {   # the x axis data combined for values > 0 ; adjust labels with scale_y_discrete()

    gg2 <- ggplot(newBugs.df, aes(x=positionX, y=transect, fill=transect)) +

      geom_density_ridges(aes(point_color = transect, point_fill = transect, point_shape = transect),
                          alpha = .2, jittered_points = TRUE) +

      scale_point_color_hue(l = 40)  +
      scale_discrete_manual(aesthetics = "point_shape", values = c(21, 22, 23)) +

      xlim(1,10) +

      # http://www.sthda.com/english/wiki/ggplot2-axis-ticks-a-guide-to-customize-tick-marks-and-labels#change-tick-mark-labels
      #scale_y_discrete(labels=c("0" = "none", "1" = "one or more")) +
      scale_x_continuous(
        position='top',
        breaks=seq(4,200,16), 
        sec.axis = sec_axis(~.*.3048,
        breaks= seq(0, 70, 10),
        name= "trap distance from row start (m)"))  +

      labs(x="trap distance from row start (ft)",
         y= paste("observations with spiders", sep=""),
         caption=paste(speciesText, " probability density\ncollection time: ", when, sep="")) +

      theme(panel.grid.minor=element_blank()) +  # hide the minor gridlines
      theme(axis.title.y = element_text(angle = 90, vjust=.5)) +
      theme_bw()

  }
  
  return(gg2)
}



plotRidgesV2tableOnly <- function(data, combined, bugs, speciesText, when, wk, caption) {

  # https://en.wikipedia.org/wiki/Kernel_density_estimation
  #
  # https://stackoverflow.com/questions/7310186/function-in-r-passing-a-dataframe-and-a-column-name

  if (FALSE) {   # available for debug
    # https://stackoverflow.com/questions/9726705/assign-multiple-objects-to-globalenv-from-within-a-function
    assign("data", data, envir=.GlobalEnv)
    assign("bugs", bugs, envir=.GlobalEnv)

    assign("when", when, envir=.GlobalEnv)
    assign("wk", wk, envir=.GlobalEnv)
    assign("caption", caption, envir=.GlobalEnv)
  }
  
  # https://cran.r-project.org/web/packages/ggridges/vignettes/introduction.html
  
  if (wk < 23 | wk > 52) {  # we definitely don't have a valid week
    # this case indicates 'use data from all weeks'
    cumulative <- "(cumulative)"
    
    if (when != "am" & when != "pm") {    # use all the data (am and pm) for each day
      #filteredBugs.df <- filter(data, transect == where)
    } else {                              # use partial data (am or pm) for each day
      filteredBugs.df <- filter(data, time == when)
    }
    
  } else {  #  we might have a 'valid' week (data for the specified week could be
    #  missing....)
    cumulative <- as.character(wk)
    
    if (when != "am" & when != "pm") {   # use all the data (am and pm) for each day
      filteredBugs.df <- filter(data, week == wk)
    } else {                             # use partial data (am or pm) for each day
      filteredBugs.df <- filter(data, time == when & week == wk)
    }
    
    
  }
  
  
  # simplify to include the trap position and the bug in the list
  newBugs.df <- subset(filteredBugs.df, select= c("positionX", "transect", bugs))

  # exclude counts == 0
  newBugs.df <- newBugs.df %>% dplyr::filter(newColumn > 0)
  
  ################################################################################################
  # get some stats to add to the plot

  # note: nuance of using the > operator and sum()
  # As a result you can SUM over this to find the number of values which are TRUE (>2000), 
  # ie Count. While you may have been expecting this input to SUM the actual values themselves
  # https://stackoverflow.com/questions/22690255/count-observations-greater-than-a-particular-value

  spider_rows <- nrow(newBugs.df)
  trapsWithSpiders <- nrow(newBugs.df[newBugs.df[,bugs] > 0, ])
  # trapsWithSpiders <- sum(newBugs.df[,bugs])
  percentOcurrence <- (trapsWithSpiders / spider_rows) * 100
  # https://stackoverflow.com/questions/3443687/formatting-decimal-places-in-r
  percentOcurrence <- format(round(percentOcurrence, 2), nsmall = 2)

  ################################################################################################
  
  # get factors for geom_density_ridges
  # (grouping by "count")
  factor.list <- newBugs.df[,bugs]   #     
  newBugs.df$geomFactors <- NULL                        
  newBugs.df$geomFactors <- as.factor(factor.list)

  return(newBugs.df)
  
  }



plotSpeciesTrendV3 <- function(data, species, speciesText, period, trend,
                               lowerWeekLimit, upperWeekLimit, caption) {
  

  ########### stand-alone dplyr test code ##########
  if (FALSE) {   # this is essentially a multi-line comment
    temp.df <- bugs.df %>%
      filter( time == "pm",  transect == "oakMargin") %>%
      group_by( week ) %>%
      summarise( sp_by_week = sum( Thomisidae..crab.spider. , na.rm = TRUE ) , n=n()) %>%
      mutate(ave_per_week = sp_by_week / (n / 30))
    
    sp_percent <- sum(temp.df$sp_by_week) / sum(temp.df$n)
    
    new.df <- bugs.df %>% mutate(newColumn = ifelse(Thomisidae..crab.spider. > 0, 1, 0))
    
  }
  ########### end stand-alone dplyr test code ##########
  
  
  temp.df <- data %>%
    #filter( time == "pm",  transect == "oakMargin") %>%
    filter(transect == "oakMargin") %>%
    group_by( week ) %>%
    summarise( sp_by_week = sum( !!species , na.rm = TRUE ) , n=n()) %>%
    mutate(ave_per_week = sp_by_week / (n / 30))
  
  # get statistics
  sp_percentOak <- sum(temp.df$sp_by_week) / sum(temp.df$n) * 100
  sp_percentOak <- format(round(sp_percentOak, 2), nsmall = 2)
  
  temp.df <- data %>%
    filter( time == "pm",  transect == "control") %>%
    group_by( week ) %>%
    summarise( sp_by_week = sum( !!species , na.rm = TRUE ) , n=n()) %>%
    mutate(ave_per_week = sp_by_week / (n / 30))
  
  # get statistics
  sp_percentControl <- sum(temp.df$sp_by_week) / sum(temp.df$n) * 100
  sp_percentControl <- format(round(sp_percentControl, 2), nsmall = 2)
  
  # partition the dataframes into 3 cluster components, plot each
  #
  # clusters are "
  #
  # oakMargin: cluster 1 = trap position 1 - 4
  #            cluster 2 = trap position 5 - 7
  #            cluster 3 = trap position 8 - 10
  #
  # control:   cluster 1 = trap position 1 - 3
  #            cluster 2 = trap position 4 - 7
  #            cluster 3 = trap position 8 - 10
  # 
  
  
  oakPM.df <- data %>%
    filter( time == "pm",  transect == "oakMargin") %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  
  oakPMcluster1.df <- data %>%
    filter( time == "pm",  transect == "oakMargin") %>%
    filter( position >= 1 & position <= 4) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  oakPMcluster2.df <- data %>%
    filter( time == "pm",  transect == "oakMargin") %>%
    filter( position >= 5 & position <= 7) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  oakPMcluster3.df <- data %>%
    filter( time == "pm",  transect == "oakMargin") %>%
    filter( position >= 8 & position <= 10) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  
  oakPMcluster.list <- list()
  oakPMcluster.list[[1]] <- oakPMcluster1.df
  oakPMcluster.list[[2]] <- oakPMcluster2.df
  oakPMcluster.list[[3]] <- oakPMcluster3.df
  
  
  controlPM.df <- data %>%
    filter( time == "pm",  transect == "control") %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  
  controlPMcluster1.df <- data %>%
    filter( time == "pm",  transect == "control") %>%
    filter( position >= 1 & position <= 3) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) )  
  controlPMcluster2.df <- data %>%
    filter( time == "pm",  transect == "control") %>%
    filter( position >= 4 & position <= 7) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  controlPMcluster3.df <- data %>%
    filter( time == "pm",  transect == "control") %>%
    filter( position >= 8 & position <= 10) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  
  controlPMcluster.list <- list()
  controlPMcluster.list[[1]] <- controlPMcluster1.df
  controlPMcluster.list[[2]] <- controlPMcluster2.df
  controlPMcluster.list[[3]] <- controlPMcluster3.df


  
  oakAM.df <- data %>%
    filter( time == "am",  transect == "oakMargin") %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) )

  oakAMcluster1.df <- data %>%
    filter( time == "am",  transect == "oakMargin") %>%
    filter( position >= 1 & position <= 4) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  oakAMcluster2.df <- data %>%
    filter( time == "am",  transect == "oakMargin") %>%
    filter( position >= 5 & position <= 7) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  oakAMcluster3.df <- data %>%
    filter( time == "am",  transect == "oakMargin") %>%
    filter( position >= 8 & position <= 10) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  
  oakAMcluster.list <- list()
  oakAMcluster.list[[1]] <- oakAMcluster1.df
  oakAMcluster.list[[2]] <- oakAMcluster2.df
  oakAMcluster.list[[3]] <- oakAMcluster3.df



  
  controlAM.df <- data %>%
    filter( time == "am",  transect == "control") %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) )

  controlAMcluster1.df <- data %>%
    filter( time == "am",  transect == "control") %>%
    filter( position >= 1 & position <= 3) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) )  
  controlAMcluster2.df <- data %>%
    filter( time == "am",  transect == "control") %>%
    filter( position >= 4 & position <= 7) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  controlAMcluster3.df <- data %>%
    filter( time == "am",  transect == "control") %>%
    filter( position >= 8 & position <= 10) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  
  controlAMcluster.list <- list()
  controlAMcluster.list[[1]] <- controlAMcluster1.df
  controlAMcluster.list[[2]] <- controlAMcluster2.df
  controlAMcluster.list[[3]] <- controlAMcluster3.df

  

  
  oakAllDay.df <- data %>%
    filter( transect == "oakMargin") %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 

  oakAllDaycluster1.df <- data %>%
    filter(transect == "oakMargin") %>%
    filter( position >= 1 & position <= 4) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  oakAllDaycluster2.df <- data %>%
    filter(transect == "oakMargin") %>%
    filter( position >= 5 & position <= 7) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  oakAllDaycluster3.df <- data %>%
    filter(transect == "oakMargin") %>%
    filter( position >= 8 & position <= 10) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  
  oakAllDayCluster.list <- list()
  oakAllDayCluster.list[[1]] <- oakAllDaycluster1.df
  oakAllDayCluster.list[[2]] <- oakAllDaycluster2.df
  oakAllDayCluster.list[[3]] <- oakAllDaycluster3.df




  
  controlAllDay.df <- data %>%
    dplyr::filter( transect == "control") %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 


  controlAllDayCluster1.df <- data %>%
    filter(transect == "control") %>%
    filter( position >= 1 & position <= 3) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) )  
  controlAllDayCluster2.df <- data %>%
    filter(transect == "control") %>%
    filter( position >= 4 & position <= 7) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  controlAllDayCluster3.df <- data %>%
    filter(transect == "control") %>%
    filter( position >= 8 & position <= 10) %>%
    group_by( week ) %>%
    summarise( bugs = sum( !!species , na.rm = TRUE ) ) 
  
  controlAllDayCluster.list <- list()
  controlAllDayCluster.list[[1]] <- controlAllDayCluster1.df
  controlAllDayCluster.list[[2]] <- controlAllDayCluster2.df
  controlAllDayCluster.list[[3]] <- controlAllDayCluster3.df

  
  
  #lowerWeekLimit <- 23
  #upperWeekLimit <- 34
  #trend<-FALSE
  # species<-quo(Thomisidae..crab.spider.)

  g.list <- list()

  
  if (period=="pm") {

    
    g1 <- ggTrendOrCumulative(df1=oakPM.df, df2=controlPM.df, 
                              lowerWeekLimit1=lowerWeekLimit, upperWeekLimit1=upperWeekLimit,
                              lowerWeekLimit2=lowerWeekLimit, upperWeekLimit2=upperWeekLimit,
                              t1="SNH", t2="control",
                              tr=trend,  st="crab spider", 
                              spct=sp_percentOak, 
                              subtitle="afternoon collection", caption=" ")
    
    g.list[[1]] <- g1
    
    # don't run this twice
    if (trend==FALSE) {

      # write the PM counts data by cluster by week
      DFtoDiscCL(df1=oakPMcluster1.df, df2=oakPMcluster2.df, df3=oakPMcluster3.df, name="spiderCountsOAKclustersPM")
      DFtoDiscCL(df1=controlPMcluster1.df, df2=controlPMcluster2.df, df3=controlPMcluster3.df, name="spiderCountsCONTROLclustersPM")


      clusterGraph.list <- ggTrendClusters(df1=oakPMcluster.list, df2=controlPMcluster.list, 
                              lowerWeekLimit1=lowerWeekLimit, upperWeekLimit1=upperWeekLimit,
                              lowerWeekLimit2=lowerWeekLimit, upperWeekLimit2=upperWeekLimit,
                              st="crab spider", 
                              spct=sp_percentOak, 
                              subtitle="afternoon collection", caption=" ")
    
      g.list[[2]] <- clusterGraph.list[[1]]  # SNH
      g.list[[3]] <- clusterGraph.list[[2]]  # control

    }
    
  } else if (period=="am") {
  
    g2 <- ggTrendOrCumulative(df1=oakAM.df, df2=controlAM.df, 
                            lowerWeekLimit1=lowerWeekLimit, upperWeekLimit1=upperWeekLimit,
                            lowerWeekLimit2=lowerWeekLimit, upperWeekLimit2=upperWeekLimit,
                            t1="SNH", t2="control",
                            tr=trend,  st="crab spider", 
                            spct=sp_percentOak, 
                            subtitle="morning collection", caption=" ")
    
    g.list[[1]] <- g2

    # don't run this twice
    if (trend==FALSE) {

      clusterGraph.list <- ggTrendClusters(df1=oakAMcluster.list, df2=controlAMcluster.list, 
                              lowerWeekLimit1=lowerWeekLimit, upperWeekLimit1=upperWeekLimit,
                              lowerWeekLimit2=lowerWeekLimit, upperWeekLimit2=upperWeekLimit,
                              st="crab spider", 
                              spct=sp_percentOak, 
                              subtitle="morning collection", caption=" ")
    
      g.list[[2]] <- clusterGraph.list[[1]]  # SNH
      g.list[[3]] <- clusterGraph.list[[2]]  # control

    }

    
  } else {
 
    g3 <- ggTrendOrCumulative(df1=oakAllDay.df, df2=controlAllDay.df, 
                              lowerWeekLimit1=lowerWeekLimit, upperWeekLimit1=upperWeekLimit,
                              lowerWeekLimit2=lowerWeekLimit, upperWeekLimit2=upperWeekLimit,
                              t1="SNH", t2="control",
                              tr=trend,  st="crab spider", 
                              spct=sp_percentOak, 
                              subtitle="24 hour collection", caption=" ") 
    
    g.list[[1]] <- g3

    # don't run this twice
    if (trend==FALSE) {

      clusterGraph.list <- ggTrendClusters(df1=oakAllDayCluster.list, df2=controlAllDayCluster.list, 
                              lowerWeekLimit1=lowerWeekLimit, upperWeekLimit1=upperWeekLimit,
                              lowerWeekLimit2=lowerWeekLimit, upperWeekLimit2=upperWeekLimit,
                              st="crab spider", 
                              spct=sp_percentOak, 
                              subtitle="24 hour collection", caption=" ")
    
      g.list[[2]] <- clusterGraph.list[[1]]   # SNH
      g.list[[3]] <- clusterGraph.list[[2]]   # control

    }


    
  }
  
  
  return(g.list)
  
}


DFtoDiscCL <- function(df1, df2, df3, name) {

  # write the data as a text file

  path<- "./code/output/"

  fileName <- paste(path, name, ".txt", sep="")

  library(dplyr)

  df1$cluster <- "cl-one"
  df2$cluster <- "cl-two"
  df3$cluster <- "cl-three"

  combo.df <- full_join(df1, df2, by = "week")
  combo.df <- full_join(combo.df, df3, by = "week")

  write.table(combo.df, fileName, append=FALSE, sep="\t", eol="\r")

}

singleDFtoDiscCL <- function(df, transect, name) {

  # write cluster data by week

  path<- "./code/output/"

  fileName <- paste(path, name, ".txt", sep="")

  write.table(df, fileName, append=FALSE, sep="\t", eol="\r")


}

ggSpeciesJulianTrend <- function(df, j, PM, AM, st, t, spct, caption) {

  # https://stackoverflow.com/questions/19826352/pass-character-strings-to-ggplot2-within-a-function

  # note: these two functions can't be combined with logic to manipluate the labels
  # because labels can't be changed  ... https://ggplot2.tidyverse.org/reference/gg-add.html

  gg <- ggplot(df, aes_string(x=j, y=PM)) +
      geom_point(shape=21) +
      geom_line(aes_string(x=j, y=PM), colour="red") +
      geom_point(aes_string(x=j, y=AM), shape=22) +
      geom_line(aes_string(x=j, y=AM), colour="blue") +   
      ylim(0,100) +
      labs(title= paste(st, " Population Counts",
                        "\ntransect: ", t, sep=""), 
           subtitle = paste("\ntraps with ", st, "s: ", spct, " %", 
                           sep=""),
         x="julian day",
         y= "daily total",
         caption=paste(caption, "\n(NO CAPTION)", sep="")) +
    # https://stackoverflow.com/questions/24496984/how-to-add-legend-to-ggplot-manually-r
    scale_colour_manual(values=c(afternoon="red", morning="blue")) + 
    # https://stackoverflow.com/questions/47584766/draw-a-box-around-a-legend-ggplot2
    theme(legend.title=element_blank(), 
          legend.box.background = element_rect(colour = "black"),
          panel.border = element_rect(colour = "black", fill=NA)) + 
    # Put bottom-right corner of legend box in bottom-right corner of graph
    theme(legend.justification=c(1,0), legend.position=c(.9,.7)) +
    theme(panel.grid.minor=element_blank()) +  # hide the minor gridlines
    theme(axis.title.y = element_text(angle = 90, vjust=.5)) +
    theme_bw() 

    return(gg)

}

ggSpeciesWeekTrend <- function(df, j, PM, AM, st, t, spct, caption) {

  # https://stackoverflow.com/questions/19826352/pass-character-strings-to-ggplot2-within-a-function

  # note: these two functions can't be combined with logic to manipluate the labels
  # because labels can't be changed  ... https://ggplot2.tidyverse.org/reference/gg-add.html
  gg <- ggplot(df, aes_string(x=j, y=PM)) +
      geom_point(shape=21) +
      geom_line(aes_string(x=j, y=PM), colour="red") +
      geom_point(aes_string(x=j, y=AM), shape=22) +
      geom_line(aes_string(x=j, y=AM), colour="blue") + 

      ylim(0,100) +

      #xlim(c(22, 40)) + 
      #expand_limits(x=c(22,40)) +
      #scale_x_continuous(breaks = seq(min(22), max(40), by = 5)) +
      scale_x_continuous(breaks = seq(min(20), max(40), by = 2), labels = fmt_dcimals(0)) +

      labs(title= paste(st, " Population Counts",
                        "\ntransect: ", t, sep=""), 
           subtitle = paste("\ntraps with ", st, "s: ", spct, " %", 
                           sep=""),
         x="week",
         y= "daily total",
         caption=paste(caption, "\n(NO CAPTION)", sep="")) +
    # https://stackoverflow.com/questions/24496984/how-to-add-legend-to-ggplot-manually-r
    scale_colour_manual(values=c(afternoon="red", morning="blue")) + 
    # https://stackoverflow.com/questions/47584766/draw-a-box-around-a-legend-ggplot2
    theme(legend.title=element_blank(), 
          legend.box.background = element_rect(colour = "black"),
          panel.border = element_rect(colour = "black", fill=NA)) + 
    # Put bottom-right corner of legend box in bottom-right corner of graph
    theme(legend.justification=c(1,0), legend.position=c(.9,.7)) +
    theme(panel.grid.minor=element_blank()) +  # hide the minor gridlines
    theme(axis.title.y = element_text(angle = 90, vjust=.5)) +
    theme_bw() 

    return(gg)

}



ggTrendOrCumulative <- function(df1, df2,
                                lowerWeekLimit1, upperWeekLimit1,
                                lowerWeekLimit2, upperWeekLimit2,
                                t1, t2,
                                tr, st, spct, subtitle, caption) {
  
  df1 <- df1 %>%
    filter(week >= lowerWeekLimit1 & week <= upperWeekLimit1) %>%
    mutate(cumulativeBugs= cumsum(bugs))
  
  assign("df1", df1, envir=.GlobalEnv)

  df2 <- df2 %>%
    filter(week >= lowerWeekLimit2 & week <= upperWeekLimit2) %>%
    mutate(cumulativeBugs= cumsum(bugs))
  
  color <- c( "c1" = "red", "c2" = "blue" )
  shape <- c("s1" = 21, "s2" = 22) 
  
  if (tr==TRUE) {
    
    gg <- ggplot() +
      geom_point(data=df1, aes(x=week, y=bugs, shape="s1")) +
      geom_line(data=df1, aes(x=week, y=bugs, color="c1")) +
      geom_point(data=df2, aes(x=week, y=bugs, shape="s2")) +
      geom_line(data=df2, aes(x=week, y=bugs, color="c2")) +
      
      ylim(0,150) +
    
      labs(x="week", y= "daily total",
         caption=paste(st, " weekly population counts, ", subtitle,  sep=""))
    
  } else {
    
    gg <- ggplot() +
      geom_point(data=df1, aes(x=week, y=cumulativeBugs, shape="s1")) +
      geom_line(data=df1, aes(x=week, y=cumulativeBugs, color="c1")) +
      geom_point(data=df2, aes(x=week, y=cumulativeBugs, shape="s2")) +
      geom_line(data=df2, aes(x=week, y=cumulativeBugs, color="c2")) +
      
      ylim(0,450) +
    
      labs(x="week", y= "cumulative count",
           caption=paste(st, " cumulative population counts\n", subtitle,  sep="")) 
  }
    
  gg <- gg + 
    
    expand_limits(x=c(23,34)) +
    scale_x_continuous(breaks = seq(24, 34, 2)) +
    
    # https://stackoverflow.com/questions/24496984/how-to-add-legend-to-ggplot-manually-r
    # https://stackoverflow.com/questions/17713919/two-geom-points-add-a-legend
    scale_shape_manual(name = "transect", 
                       breaks = c("s1", "s2"),
                       values = shape,
                       labels = c("SNH", "control")) + 
    scale_color_manual(name = "transect", 
                       breaks = c("c1", "c2"), 
                       values = color,
                       labels = c("SNH", "control")) +
    
    theme_bw() + 
    theme(axis.title.y = element_text(angle = 90, vjust=.5)) +
    
    theme(legend.title = element_blank(),
          legend.spacing.y = unit(0, "mm"), 
          #legend.position=c(.9,.7),
          legend.justification=c(1,0),
          panel.border = element_rect(colour = "black", fill=NA),
          aspect.ratio = 1, axis.text = element_text(colour = 1, size = 12),
          legend.background = element_blank(),
          legend.box.background = element_rect(colour = "black")) 
  
  return(gg)
  
}


ggTrendClusters <- function(df1, df2,
                            lowerWeekLimit1, upperWeekLimit1,
                            lowerWeekLimit2, upperWeekLimit2,
                            st, spct, subtitle, caption) {
  
  assign("df1", df1, envir=.GlobalEnv)
  
  color <- c( "c1" = "red", "c2" = "green", "c3" = "blue" )
  shape <- c("s1" = 21, "s2" = 22, "s3" = 23) 
  
    
    ggOak <- ggplot() +
      
      geom_point(data=df1[[1]], aes(x=week, y=bugs, shape="s1")) +
      geom_line(data=df1[[1]], aes(x=week, y=bugs, color="c1")) +
      geom_point(data=df1[[2]], aes(x=week, y=bugs, shape="s2")) +
      geom_line(data=df1[[2]], aes(x=week, y=bugs, color="c2")) +
      geom_point(data=df1[[3]], aes(x=week, y=bugs, shape="s3")) +
      geom_line(data=df1[[3]], aes(x=week, y=bugs, color="c3")) +
      
      ylim(0,60) +
      expand_limits(y=c(0,60)) +

      labs(x="week", y= "daily total",
           caption=paste("weekly population counts by cluster\n", "SNH transect, ", subtitle, sep="")) +
      
      expand_limits(x=c(23,34)) +
      scale_x_continuous(breaks = seq(24, 34, 2)) +
      
      # https://stackoverflow.com/questions/24496984/how-to-add-legend-to-ggplot-manually-r
      # https://stackoverflow.com/questions/17713919/two-geom-points-add-a-legend
      scale_shape_manual(name = "transect", 
                         breaks = c("s1", "s2", "s3"),
                         values = shape,
                         labels = c("cluster 1", "cluster 2", "cluster 3")) + 
      scale_color_manual(name = "transect",   # <-- bug: should be scale_shape_manual() to match aes()
                         breaks = c("c1", "c2", "c3"), 
                         values = color,
                         labels = c("cluster 1", "cluster 2", "cluster 3")) +
      
      theme_bw() + 
      theme(axis.title.y = element_text(angle = 90, vjust=.5)) +
      
      theme(legend.title = element_blank(),
            legend.spacing.y = unit(0, "mm"), 
            #legend.position=c(.9,.7),
            legend.justification=c(1,0),
            panel.border = element_rect(colour = "black", fill=NA),
            aspect.ratio = 1, axis.text = element_text(colour = 1, size = 12),
            legend.background = element_blank(),
            legend.box.background = element_rect(colour = "black")) 
    
      
    
    ggControl <- ggplot() +
      
      geom_point(data=df2[[1]], aes(x=week, y=bugs, shape="s1")) +
      geom_line(data=df2[[1]], aes(x=week, y=bugs, color="c1")) +
      geom_point(data=df2[[2]], aes(x=week, y=bugs, shape="s2")) +
      geom_line(data=df2[[2]], aes(x=week, y=bugs, color="c2")) +
      geom_point(data=df2[[3]], aes(x=week, y=bugs, shape="s3")) +
      geom_line(data=df2[[3]], aes(x=week, y=bugs, color="c3")) +
     
      ylim(0,60) +
      expand_limits(y=c(0,60)) +
      
      #labs(title= paste("weekly population counts by cluster", sep=""), 
           #subtitle = paste("control transect, ", subtitle, sep=""),
      labs(x="week", y= "daily total",
           caption=paste("weekly population counts by cluster\n", "control transect, ", subtitle, sep="")) +
      
      expand_limits(x=c(23,34)) +
      scale_x_continuous(breaks = seq(24, 34, 2)) +
    
    # https://stackoverflow.com/questions/24496984/how-to-add-legend-to-ggplot-manually-r
    # https://stackoverflow.com/questions/17713919/two-geom-points-add-a-legend
    scale_shape_manual(name = "transect", 
                       breaks = c("s1", "s2", "s3"),
                       values = shape,
                       labels = c("cluster 1", "cluster 2", "cluster 3")) + 
    scale_color_manual(name = "transect", 
                       breaks = c("c1", "c2", "c3"), 
                       values = color,
                       labels = c("cluster 1", "cluster 2", "cluster 3")) +
    
    theme_bw() + 
    theme(axis.title.y = element_text(angle = 90, vjust=.5)) +
    
    theme(legend.title = element_blank(),
          legend.spacing.y = unit(0, "mm"), 
          #legend.position=c(.9,.7),
          legend.justification=c(1,0),
          panel.border = element_rect(colour = "black", fill=NA),
          aspect.ratio = 1, axis.text = element_text(colour = 1, size = 12),
          legend.background = element_blank(),
          legend.box.background = element_rect(colour = "black")) 
    
    graphs.list <- list()
    graphs.list[[1]] <- ggOak 
    graphs.list[[2]] <- ggControl
    
  return(graphs.list)
  
}


fmt_dcimals <- function(decimals=0){
  # https://stackoverflow.com/questions/10035786/ggplot2-y-axis-label-decimal-precision
    function(x) format(x,nsmall = decimals,scientific = FALSE)
}



bugCount <- function() {
  
  total <- sum(bugs.df$DBfly, na.rm=TRUE) +
    sum(bugs.df$LBfly, na.rm=TRUE) +
    sum(bugs.df$X3partFly, na.rm=TRUE) +
    sum(bugs.df$houseFly, na.rm=TRUE) +
    sum(bugs.df$greenFly, na.rm=TRUE) +
    sum(bugs.df$wasp, na.rm=TRUE) +
    sum(bugs.df$wildBee, na.rm=TRUE) +
    sum(bugs.df$bumble, na.rm=TRUE) +
    sum(bugs.df$spider, na.rm=TRUE) +
    sum(bugs.df$spiderJumping, na.rm=TRUE) +
    sum(bugs.df$ladyBug, na.rm=TRUE) +
    sum(bugs.df$hopper, na.rm=TRUE) +
    sum(bugs.df$ant, na.rm=TRUE) +
    sum(bugs.df$other, na.rm=TRUE) +
    sum(bugs.df$butterFly, na.rm=TRUE) +
    sum(bugs.df$microMoth, na.rm=TRUE) +
    sum(bugs.df$cucumberBeetle, na.rm=TRUE)
  
  return(total)
  
}

bugNames <- function(df) {
  #column names to be ignored
  ignore <- c("transect", "row", "position",
              "date", "time", "julian", "week",
              "positionX")
  df[ignore] <- NULL
  return(as.list(colnames(df)))
}

bigTable <- function(df) {
  # https://rdrr.io/cran/dplyr/man/summarise_all.html 
  # https://stackoverflow.com/questions/9723208/aggregate-summarize-multiple-variables-per-group-e-g-sum-mean
  
  list <- as.character(bugNames(df))
  charVector <- as.character(c("sum", "max"))
  df2 <- df  %>% summarise_at(list, funs(sum, max))
  
  # https://stackoverflow.com/questions/35839408/r-dplyr-drop-multiple-columns
  #iris %>% select(-one_of(drop.cols))
  
  
  return(df2)
}




compareTransectG2V1 <- function (data, species, operator, initialPosition, secondaryPosition, positionText) {

  # Programming with dplyr, Different input variable (how and when to quote/unquote)
  # https://cran.r-project.org/web/packages/dplyr/vignettes/programming.html

  # This function provides the flexibility to configure the dplyr::filter() position argument on-the-fly,
  # we need to support the following cases
  #
  # filter(position < initialPosition)
  # filter(position > initialPosition)
  # filter(between(position, initialPosition, secondaryPosition))

  #####################################################
  # https://stackoverflow.com/questions/29554796/meaning-of-band-width-in-ggplot-geom-smooth-lm

  #species <- enquo(species)
  #initialPosition <- enquo(initialPosition)
  #secondaryPosition <- enquo(secondaryPosition)
  
  #######################################
  # rMarkdown
  #
  #positionText <- paste("\ntransect positions ", "1-4", sep="")
  #g3 <- compareTransectG2V1(data=bugs.df, 
                            #species=quo(Thomisidae..crab.spider.), 
                            #operator="LT",
                            #initialPosition=quo(5), 
                            #secondaryPosition=quo(0),
                            #positionText)
  #positionText <- paste("\ntransect positions ", "5-7", sep="")
  #g46 <- compareTransectG2V1(data=bugs.df, 
                             #species=quo(Thomisidae..crab.spider.), 
                             #operator="BETWEEN",
                             #initialPosition=quo(4), 
                             #secondaryPosition=quo(8),
                             #positionText)
  #positionText <- paste("\ntransect positions ", "8-10", sep="")
  #g7 <- compareTransectG2V1(data=bugs.df, 
                            #species=quo(Thomisidae..crab.spider.), 
                            #operator="GT",
                            #initialPosition=quo(7), 
                            #secondaryPosition=quo(0),
                            #positionText)
  #
  #######################################

  if (FALSE) {   # available for debug
    # https://stackoverflow.com/questions/9726705/assign-multiple-objects-to-globalenv-from-within-a-function
    assign("data", data, envir=.GlobalEnv)
    assign("species", species, envir=.GlobalEnv)
    assign("operator", operator, envir=.GlobalEnv)
    assign("initialPosition", initialPosition, envir=.GlobalEnv)
    assign("secondaryPosition", secondaryPosition, envir=.GlobalEnv)
  }

  if (operator == "BETWEEN") {

      oak.df <- data %>% 
      dplyr::filter(between(position, !!initialPosition , !!secondaryPosition), time=="pm", transect=="oakMargin") %>% 
      dplyr::group_by(julian) %>% 
      dplyr::summarise(oakEdgeMean=mean(!!species))

      center.df <- data %>% 
      dplyr::filter(between(position, !!initialPosition , !!secondaryPosition), time=="pm", transect=="control") %>% 
      dplyr::group_by(julian) %>% 
      dplyr::summarise(controlEdgeMean=mean(!!species))
      

  } else {

    if (operator == "LT") {

      oak.df <- data %>% 
      # dplyr::filter(position < !! initialPosition, time=="pm", transect=="oakMargin") %>% 
      dplyr::filter(position < !! initialPosition, transect=="oakMargin") %>% 
      dplyr::group_by(julian) %>% 
      dplyr::summarise(oakEdgeMean=mean(!!species))

      center.df <- data %>% 
      # dplyr::filter(position < !! initialPosition, time=="pm", transect=="control") %>% 
      dplyr::filter(position < !! initialPosition, transect=="control") %>% 
      dplyr::group_by(julian) %>% 
      dplyr::summarise(controlEdgeMean=mean(!!species))

      ip <- initialPosition 
      positionString <- paste("\ntransect positions < ", ip , sep="")

    } else if (operator == "GT") {

      oak.df <- data %>% 
      dplyr::filter(position > !! initialPosition, transect=="oakMargin") %>% 
      dplyr::group_by(julian) %>% 
      dplyr::summarise(oakEdgeMean=mean(!! species))

      center.df <- data %>% 
      dplyr::filter(position > !! initialPosition, transect=="control") %>% 
      dplyr::group_by(julian) %>% 
      dplyr::summarise(controlEdgeMean=mean(!! species))

      ip <- initialPosition
      positionString <- paste("\ntransect positions > ", ip , sep="")

    } else {

      message( paste("compareTransectUsingQuosure(): ", operator, " not supported", sep=""))
      stop()

    }

  }

  combo.df <- merge(oak.df, center.df)

  combo.df <- combo.df %>% 
    dplyr::mutate(deltaMean=as.numeric( oakEdgeMean/controlEdgeMean ) )
  
  combo.df <- combo.df %>% filter(!is.na(deltaMean), !is.infinite(deltaMean))

  
  # assign("combo.df", combo.df, envir=.GlobalEnv)  # for debugging
  # the dataframe contains columns 'julian', 'oakEdgeMean', 'controlEdgeMean', 'deltaMean'

  # arbitraty week groupings (from bayes.R): "weeks 23-25",  "weeks 26-30", "weeks 31-34"
  #
  # "weeks 23-25" : julian range 155 - 175
  # "weeks 26-30" : julian range 176 - 210
  # "weeks 31-34" : julian range 211 - 238

  # add a 'julianGroup' factor for geom_smooth ()
  combo.df <- combo.df %>% dplyr::mutate(julianGroup = 
    case_when( julian >= 155 & julian <= 175  ~ "red", 
               julian >= 176 & julian <= 210  ~ "green",
               julian >= 211 & julian <= 238  ~ "blue" ))

assign("combo.df", combo.df, envir=.GlobalEnv)

# https://stackoverflow.com/questions/29880210/as-numeric-removes-decimal-places-in-r-how-to-change

  ggCompare1 <- ggplot(data=combo.df, shape=21) +
      # ggplot really only likes to draw legends for things that have aesthetic mappings.
      #
      geom_point(data=subset(combo.df, julianGroup=="red"), aes(x=julian, y=deltaMean, color=julianGroup, fill=julianGroup) ) +
      geom_point(data=subset(combo.df, julianGroup=="green"), aes(x=julian, y=deltaMean, color=julianGroup, fill=julianGroup) ) +
      geom_point(data=subset(combo.df, julianGroup=="blue"), aes(x=julian, y=deltaMean, color=julianGroup, fill=julianGroup) ) +
      geom_smooth(method="lm", level=0.89, aes(x=julian, y=deltaMean, color=julianGroup)) +   # aes() sections the data even though 'line' is undefined

      # aes(color=julianGroup, fill=julianGroup),
      #geom_hline(yintercept=0) +
      xlim(154,239) +
      ylim(-.1,1.2) +

      geom_hline(yintercept=1) + 

      labs(title= paste("average spiders per trap ",
                        positionText,
                        "\n(oak average / control average)", sep=""), 
           subtitle = paste("89% confidence interval", sep=""),
         x="julian day",
         y= "oakMargin fraction of control",
         caption=paste("120 observations per day", "\npositions 1 - 10 inclusive", sep="")) +

      theme(legend.title=element_blank(), 
          legend.box.background = element_rect(colour = "black"),
          panel.border = element_rect(colour = "black", fill=NA)) + 
      # Put bottom-right corner of legend box in bottom-right corner of graph
      theme(legend.justification=c(1,0), legend.position=c(.9,.7)) +
      theme(panel.grid.minor=element_blank()) +  # hide the minor gridlines
      theme(axis.title.y = element_text(angle = 90, vjust=.5)) +
      theme_bw() 
    

  return(grid.arrange(ggCompare1, ncol=1, nrow=1))

}


selectDataAcrossTransects <- function(data, week, species) {

        #dplyr::filter(transect == UQ(t), week == UQ(w)) # last comment
        # https://www.reddit.com/r/rstats/comments/6zu5od/when_writing_functions_involving_dplyr_how_do_you/

    test.df <- data %>% 
        dplyr::filter(week == UQ(week))  %>%
        dplyr::select(positionX, row, UQ(species)) %>%
        dplyr::group_by(positionX, row) %>%
        summarize(totalSpiders = sum(UQ(species), na.rm = T))

  return(test.df)

}


plotBugDistribution <- function (data, cap) {


  # http://t-redactyl.io/blog/2016/02/creating-plots-in-r-using-ggplot2-part-6-weighted-scatterplots.html
  gg <- ggplot(data, aes(positionX, row, size=totalSpiders)) +
    geom_point(shape=21, colour = "purple", fill = "plum", alpha=0.6) +           # 
    #scale_size_area(max_size = 20) +
    # geom_count() probably more appropriate http://ggplot2.tidyverse.org/reference/scale_size.html
    scale_size(range = c(1, 10)) +
    scale_fill_continuous(low = "plum1", high = "purple4") +
    scale_y_reverse(breaks = seq(40, 100, 5),
                    sec.axis = sec_axis(~. * 2.4384 - 103.622,         #### 8*.3048=2.4384  40*8*.3084=103.622
                                           breaks= seq(0, 350, 50),
                                           name= "distance (m)")    ) +
    expand_limits(y=c(30,100)) + 
    scale_x_continuous(position='top', breaks=seq(-12,200,16), 
                       sec.axis = sec_axis(~.*.3048,
                                           breaks= seq(0, 80, 10),
                                           name= "trap distance from field margin (m)"))  +
    # ggtitle(title) +

    labs( x = "trap distance from field margin (ft)", 
          y = "row",
          caption = cap) +

    annotate("rect", xmin=4, xmax=210, ymin=42.5,ymax=54.5, alpha=0.2, fill="blue") +
    annotate("rect", xmin=-12, xmax=5, ymin=42.5,ymax=54.5, alpha=0.2, fill="red") +

    annotate("rect", xmin=4, xmax=210, ymin=78,ymax=90, alpha=0.2, fill="blue") +
    annotate("rect", xmin=-12, xmax=5, ymin=78,ymax=90, alpha=0.2, fill="red") +

    annotate("text", x = 95, y = 76, label = "SNH transect", colour="black") +
    annotate("text", x = 95, y = 40, label = "control transect", colour="black") + # fill="white", 
    theme_bw() +
    #theme() + 
    # theme(legend.position = "bottom", legend.direction = "horizontal") +
    theme(legend.position = "none", legend.direction = "horizontal") +
    theme(legend.box = "horizontal", legend.key.size = unit(1, "cm")) +
    # coord_fixed(ratio=4)
    coord_fixed(ratio=2)
  
  return(grid.arrange(gg, ncol=1, nrow=1))
}



scanBugPercentages <- function(df) {

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

createFamilyPercentages <- function(list) {

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


plotBugPercentages <- function(list, spidersOnly) {

  dfAraneae <- list[[1]]
  dfDiptera <- list[[2]]
  dfHymenoptera <- list[[3]]
  dfHemiptera <- list[[4]]
  dfLepidoptera <- list[[5]]
  dfOther <- list[[6]]

  if (spidersOnly==TRUE) {

    gg <- ggplot(dfAraneae) + 
    
      geom_point(aes(x=week, y=spiderPct, fill = "spiderPct"), shape=21, size=5, show.legend=TRUE) +
      geom_point(aes(x=week, y=otherPct, fill = 'otherPct'), shape=21, size=5, show.legend=TRUE) +

      scale_fill_manual(name = "", values = c("spiderPct" = "purple", "otherPct" = "violet"), labels = c("crab spider", "spider (other)")) +

      ylim(c(0, 30)) + 
      expand_limits(y=c(0,30)) + 
      #coord_fixed(ratio=1/4) +     # control the aspect ratio of the output; "ratio" refers to the 
      # ratio of the axis limits themselves
    
      scale_y_continuous(breaks = seq(min(0), max(30), by = 5)) +
      scale_x_continuous(breaks=seq(22,40,2)) + 
    
    
      #labs(title=paste("spider abundance", sep=""),
      #subtitle=paste("percent of total insects by week", sep=""), 
      labs(y="percent", x="week" ) +
    
      theme_bw() +
    
      theme(legend.title = element_blank(),
          legend.spacing.y = unit(0, "mm"), 
          #legend.position=c(.9,.7),
          legend.justification=c(1,0),
          panel.border = element_rect(colour = "black", fill=NA),
          aspect.ratio = 1, axis.text = element_text(colour = 1, size = 12),
          legend.background = element_blank(),
          legend.box.background = element_rect(colour = "black")) 

    } else {

      colours = c("oakMargin" = "#405E00", "control" = "#9BCC94")

      gg <- ggplot() + 
    
        geom_jitter(data=dfOther, aes(x=week, y=sumPct, fill = family), shape=21, size=3, show.legend=TRUE) +
        geom_jitter(data=dfAraneae, aes(x=week, y=sumPct, fill = family), shape=21, size=3, show.legend=TRUE) +
        geom_jitter(data=dfDiptera, aes(x=week, y=sumPct, fill = family), shape=21, size=3, show.legend=TRUE) +
        geom_jitter(data=dfHymenoptera, aes(x=week, y=sumPct, fill = family), shape=21, size=3, show.legend=TRUE) +
        geom_jitter(data=dfHemiptera, aes(x=week, y=sumPct, fill = family), shape=21, size=3, show.legend=TRUE) +
        geom_jitter(data=dfLepidoptera, aes(x=week, y=sumPct, fill = family), shape=21, size=3, show.legend=TRUE) +

        scale_fill_manual(name = 'insect family', 
          values = c('black','green', 'blue', 'violet', 'purple', 'red'), 
          breaks = c("Other", 'Araneae', 'Diptera', 'Hymenoptera', 'Hemiptera', 'Lepidoptera'),
          labels = c("other", "Araneae", 'Diptera', 'Hymenoptera', 'Hemiptera', 'Lepidoptera')) +

        #guides(shape = guide_legend("insect family"))  +

        ylim(c(0, 100)) + 
        expand_limits(y=c(0,100)) + 
        #coord_fixed(ratio=1/4) +     # control the aspect ratio of the output; "ratio" refers to the 
        # ratio of the axis limits themselves
    
        #scale_y_continuous(trans='log10', breaks = seq(min(0), max(100), by = 20)) +
        scale_y_continuous(trans='log10') +
        annotation_logticks(sides='l') +

        scale_x_continuous(breaks=seq(22,40,2)) + 
    
    
        #labs(title=paste("insect abundance by taxonometric Order", sep=""),
        # subtitle=paste("percent of total population by week", sep=""),
        labs(y="percent", x="week" ) +
    
        theme_bw() +
    
        theme(legend.title = element_blank(),
          legend.spacing.y = unit(0, "mm"), 
          #legend.position=c(.9,.7),
          legend.justification=c(1,0),
          panel.border = element_rect(colour = "black", fill=NA),
          aspect.ratio = 1, axis.text = element_text(colour = 1, size = 12),
          legend.background = element_blank(),
          legend.box.background = element_rect(colour = "black")) 

      }
    
  return(gg)

}

getWeeks <- function(data) {
  
  # return a list of the weeks occurring in the dataset
  # https://stackoverflow.com/questions/29832411/use-dplyr-to-get-values-of-a-column
  
  library(dplyr)
  
  weeks <- data %>%
    select(week) %>%
    unique() %>% 
    .$week
  
  return(weeks)
  
}


squashFlip <- function(df, weekList, columnList) {

  # convert row wise percent occurrance of bugs across weeks to 
  # an average of these associated insects by week

  # 
  # inbound dataframe
  #
  #        bugNames   week1Pct   week2Pct  week3Pct  ...... 
  # bugA
  # bugB   
  #
  # weeklist   : a vector of week numbers occurring in the df
  # columnList : a vector of row names ultimately to be applied as column names


  if (FALSE) {
    df <- dfShort
    weekList <- list[[3]]
    columnList <- c('otherPct', 'spiderPct', 'week')
  }

  df <- df %>% dplyr::select(-bugNames)  # remove the bugNames column
  df <- df %>% rbind(as.character(weekList)) # add a row of week numbers
  colnames(df) <- NULL
  df <- as.data.frame(t(df)) # flip  = transpose https://stackoverflow.com/questions/6778908/transpose-a-data-frame
  colnames(df) <- columnList
  options(digits=4)  # https://stackoverflow.com/questions/26734913/r-converting-from-string-to-double
  for (i in 1:length(columnList)) {
    df[,columnList[[i]]] <- as.numeric(as.character((df[,columnList[[i]]]))) # https://stackoverflow.com/questions/3796266/change-the-class-from-factor-to-numeric-of-many-columns-in-a-data-frame
  }

  # now, just create an average of insects for this particular family dataframe. columnList represents the
  # column names including 'week'. We could truncate the list to remove 'week', 
  #          like so : columnList <- columnList [ - length(columnList) ] # ignore the week column (the last column in the list)
  # and then use the modified columnList to define the columns that need to be used for the average
  #           somewhat like : df <- df %>% rowwise() %>% dplyr::mutate(meanPct=mean(columnList))
  # but mutate() is choking on that list, I think it is due to the old bogey of dyplr not accepting clean variables.
  #            the solution may be here : https://datascience.blog.wzb.eu/2016/09/27/dynamic-columnvariable-names-with-dplyr-using-standard-evaluation-functions/
  # the other approach is to remove the 'week' column, creat the average, then re-add the week column.
  #
  
  temp.df <- df
  temp.df <- temp.df %>% dplyr::select(week)                # that's a dataframe containing only week
  df <- df %>% dplyr::select(-week)                         # that's a dataframe every column except week
  df <- transform(df, sumPct = rowSums(df, na.rm = TRUE))  # finally, escaping the nightmare of dplyr https://stackoverflow.com/questions/12486264/average-across-columns-in-r-excluding-nas
  df <- dplyr::bind_cols(df, temp.df)

  # returning dataframe
  #                                     /----------- use this average for graphing purposes
  # species1.Pct .... speciesX.Pct   avePct   week
  #
  #

  return(df)

}


