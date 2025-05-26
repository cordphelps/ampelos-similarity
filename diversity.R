
countRowSpecies <- function(data, row) {
  j <- 0
  for (i in 1:ncol(data)) {
          #if (unlist(as.data.frame(t(data))[,row][i]) > 0 ) {
      if (as.integer(unlist(data[row,][i])) > 0 ) {
              j <- j +1
           }
  }
  return(j)
}

bugsOnlyByWeek <- function(data, iB, tR, w) {

  
  #
  # this function is intended to be called from ampelos.Rmd
  #

  #data <- bugs.df
  #ignoreBees <- FALSE
  #t <- "control"
  #w <- 26


  weeks.vector <- getWeeks(data)                    # determine weeks in the dataset
  weeks.df <- dplyr::bind_cols(week = weeks.vector) # place weeks in a column

  data <- data %>%  dplyr::rename(
                        Lygus.hesperus = Lygus.hesperus..western.tarnished.plant.bug., 
                        cucumber.beetle = Diabrotica.undecimpunctata..Cucumber.Beetle.) 

  if (iB == TRUE) { 
    data <- data %>% dplyr::select( 
      -Agapostemon.sp....green..native.bee.,
      -Bombus.californicus..bumble.,
      -Halictus.sp....3.part..native.bee.,
      -Honey.Bee,
      -Osmia.sp...native.bee.)
  }

  data <- data %>% 
    
    dplyr::filter(transect == tR) %>% 
    dplyr::select(-row, -position, -positionX, -transect, -julian, -time, -date)  %>%
    dplyr::group_by(week)  %>%
    dplyr::summarise_all(sum)
     
  
  return(as.data.frame(data))
}



countRowIndividuals <- function(data,row) {
  
  return(sum(unlist(as.data.frame(t(data))[,row])[1:ncol(data)]))
}




divV2 <- function(data, species, ignoreBees) {
  
  #data <- test.df
  #ignoreBees <- TRUE
  #data <- bugs.df
  
    dataOak <- bugsOnlyByWeek(data, iB=ignoreBees, tR="oakMargin")
    dataControl <- bugsOnlyByWeek(data, iB=ignoreBees, tR="control")

  
    weeks.df <- dataOak %>%     # just weeks
      dplyr::select(week) 
  
    dataOak <- dataOak %>%        # bugs only
      dplyr::select(-week)
  
    rowSum <- NULL
    rowCounts <- NULL
    for (row in 1:nrow(dataOak)) {
      rowSum[row] <- countRowIndividuals(dataOak, row)
      rowCounts[row] <- countRowSpecies(dataOak, row) 
    }
  
    inputOak.df <- cbind(dataOak, 
                    data.frame(rowSum), 
                    data.frame(rowCounts),
                    weeks.df)

    weeks.df <- dataControl %>%     # just weeks
      dplyr::select(week) 
  
    dataControl <- dataControl %>%        # bugs only
      dplyr::select(-week)
  
    rowSum <- NULL
    rowCounts <- NULL
    for (row in 1:nrow(dataControl)) {
      rowSum[row] <- countRowIndividuals(dataControl, row)
      rowCounts[row] <- countRowSpecies(dataControl, row) 
    }
  
    inputControl.df <- cbind(dataControl, 
                    data.frame(rowSum), 
                    data.frame(rowCounts),
                    weeks.df)

    # inputControl.df and inputOak.df are columns of counts for each species plus
    # a column 'rowSum' and a column 'rowCounts' indicating individual species presence
    # rows represent weeks
  
    if (species == FALSE) {

      gg <- plotDivIndividualsV2(dfOak=inputOak.df, dfControl=inputControl.df,
                captionText=paste("transect species abundance\nignoreBees: ", ignoreBees, sep=""))
    } else {

      gg <- plotDivSpeciesV2(dfOak=inputOak.df, dfControl=inputControl.df,
                captionText=paste("transect species diversity\nignoreBees : ", ignoreBees, sep=""))

    }

    return(gg)

}


  divV3 <- function(data, species, ignoreBees) {

    # this is divV2 modified to return only the dataframes (not graphs) for table generation 
  
  #data <- test.df
  #ignoreBees <- TRUE
  #data <- bugs.df
  
  dataOak <- bugsOnlyByWeek(data, iB=ignoreBees, tR="oakMargin")
  dataControl <- bugsOnlyByWeek(data, iB=ignoreBees, tR="control")

  
  weeks.df <- dataOak %>%     # just weeks
    dplyr::select(week) 
  
  dataOak <- dataOak %>%        # bugs only
    dplyr::select(-week)
  
  rowSum <- NULL
  rowCounts <- NULL
  for (row in 1:nrow(dataOak)) {
    rowSum[row] <- countRowIndividuals(dataOak, row)
    rowCounts[row] <- countRowSpecies(dataOak, row) 
  }
  
  inputOak.df <- cbind(dataOak, 
                    data.frame(rowSum), 
                    data.frame(rowCounts),
                    weeks.df)

  weeks.df <- dataControl %>%     # just weeks
    dplyr::select(week) 
  
  dataControl <- dataControl %>%        # bugs only
    dplyr::select(-week)
  
  rowSum <- NULL
  rowCounts <- NULL
  for (row in 1:nrow(dataControl)) {
    rowSum[row] <- countRowIndividuals(dataControl, row)
    rowCounts[row] <- countRowSpecies(dataControl, row) 
  }
  
  inputControl.df <- cbind(dataControl, 
                    data.frame(rowSum), 
                    data.frame(rowCounts),
                    weeks.df)

  # inputControl.df and inputOak.df are columns of counts for each species plus
  # a column 'rowSum' and a column 'rowCounts' indicating individual species presence
  # rows represent weeks
  
  df.list <- list()
  df.list[[1]] <- inputOak.df
  df.list[[2]] <- inputControl.df

  return(df.list)

}


plotDivSpeciesV2 <- function(dfOak, dfControl, captionText) {


  gg <- ggplot() + 

      # geom_jitter(aes(x=rowCounts, y=rowSum, col=week), width = 0.1, height = 0.1, show.legend = TRUE, shape = 21, size=5, colour = "mediumvioletred", fill = "plum1") + 
      
      geom_jitter(aes(x=week, y=rowCounts, colour = "mediumvioletred", fill = "plum1"), data=dfOak, width = 0.1, height = 0.1, show.legend = TRUE, 
        shape = 21, size=5) + 
      geom_jitter(aes(x=week, y=rowCounts, colour = "mediumvioletred", fill = "purple1"), data=dfControl, width = 0.1, height = 0.1, show.legend = TRUE, 
        shape = 21, size=5) + 

      scale_fill_identity(name = 'transect', guide = 'legend', 
                          breaks = c('plum1'='plum1','purple1'='purple1'), 
                          labels = c('SNH','control')) +

      guides(colour=FALSE) +
      theme(legend.position = "right", legend.direction = "vertical") +
      
      expand_limits(y=c(0,30)) +
      scale_y_continuous(breaks = seq(min(0), max(30), by = 5)) +
    
      expand_limits(x=c(22,34)) +
      scale_x_continuous(breaks = seq(min(22), max(34), by = 2)) +
    
      labs(y="total species", 
          #x="total number of 'vane trap apparent' species in sample", 
          x="week",
          caption = paste(captionText, sep="") ) +

      theme_bw() 

      return(gg)

  }

  plotDivIndividualsV2 <- function(dfOak, dfControl, captionText) {


  gg <- ggplot() + 

      # geom_jitter(aes(x=rowCounts, y=rowSum, col=week), width = 0.1, height = 0.1, show.legend = TRUE, shape = 21, size=5, colour = "mediumvioletred", fill = "plum1") + 
      
      geom_jitter(aes(x=week, y=rowSum, colour = "mediumvioletred", fill = "plum1"), data=dfOak, width = 0.1, height = 0.1, show.legend = TRUE, 
        shape = 21, size=5) + 
      geom_jitter(aes(x=week, y=rowSum, colour = "mediumvioletred", fill = "purple1"), data=dfControl, width = 0.1, height = 0.1, show.legend = TRUE, 
        shape = 21, size=5) + 

      scale_fill_identity(name = 'transect', guide = 'legend',
                          breaks = c('plum1'='plum1','purple1'='purple1'), 
                          labels = c('SNH','control')) +

      guides(colour=FALSE) +
      theme(legend.position = "right", legend.direction = "vertical") +

      expand_limits(y=c(0,500)) +
      scale_y_continuous(breaks = seq(min(0), max(500), by = 50)) +
    
      #xlim(c(22, 40)) +              # data zoom feature
      expand_limits(x=c(22,34)) +
      scale_x_continuous(breaks = seq(min(22), max(34), by = 2)) +
     
      labs(y="total individuals", 

          x="week",
          caption = paste(captionText, sep="") ) +

      theme_bw() 
      

  return(gg)

  }
