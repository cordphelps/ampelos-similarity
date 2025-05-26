




spiderArea <- function(tibbleData, tLabel, dotFill) {


		gg <- ggplot(data=tibbleData, aes(y=positionX, x=positionY)) +

  			geom_jitter(aes(size=Thomisidae..crab.spider.), shape=21, fill = dotFill ) +

  			theme_bw() +
		  
		    theme(legend.position="none") +

  			scale_y_continuous(limits=c(-10, 220), breaks=c(seq(from=0, to=220, by=16))) +
        	scale_x_continuous(limits=c(0, 8), breaks=c(seq(from=0, to=8, by=1))) +

  			labs(	y = paste( "distance from vineyard edge (feet)", sep=""),
         		 	x = paste( "row position", sep=""),
          		caption = paste(tLabel, "\n(min = 0, max = 4)", sep=""))
  			      
 	#title = paste(tLabel, " spider counts\n","by transect position\n","(min = 0, max = 4)", sep=""))


  	return(gg)

}


abundanceEstimate <- function(tibbleInput, sliceArea) {

	counts.df <- as_data_frame(tibbleInput) %>%
  		rename(groupsize = Thomisidae..crab.spider.) %>%
  		rename(dist = distance) %>%
  		mutate(rowChar = as.character(row)) %>%
  		mutate(posChar = as.character(positionX)) %>%
  		unite("siteID", rowChar:posChar) %>%
  		select(-row, -positionX, -positionY)

	df.df <- as_data_frame(counts.df) 
	site.df <- df.df %>% distinct(siteID) %>% select(siteID)

	detectionFunction <- dfuncEstim(formula = dist ~ 1,
		detectionData = counts.df,
		pointSurvey = TRUE,
		likelihood = "halfnorm")

	# Estimate Abundance 
	fit <- abundEstim(dfunc = detectionFunction,
			detectionData = counts.df,
			siteData = site.df,
			area = sliceArea,
			R = 100,
			ci = 0.95)

	return(list(fit$n.hat, fit$ci))

}


radialSlice <- function(tibbleInput, distanceMin, distanceMax, info) {

	sliced.tbl <- tibbleInput %>%
				filter(distance > distanceMin & distance < distanceMax)


  	# calculate the area of the slice
  	#     - 

  	areaMinCircle = 3.14159 * (distanceMin ** 2)
  	areaMaxCircle = 3.14159 * (distanceMax ** 2)

  	area = (areaMaxCircle - areaMinCircle) / 4

  	# get population density
  	popDetails <- abundanceEstimate(tibbleInput=sliced.tbl, sliceArea=area)


  	gg <- spiderArea(tibbleData=sliced.tbl, tLabel=paste(info, "\ndensity ", round(popDetails[[1]], digits=2), "\n", sep=""), dotFill="blue")


  	return(list(gg, popDetails[[1]], popDetails[[2]]))

}