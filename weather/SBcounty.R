
# county map

# get the coordinates of a place
# https://support.google.com/maps/answer/18539?co=GENIE.Platform%3DDesktop&hl=en


# http://eriqande.github.io/rep-res-web/lectures/making-maps-with-R.html
# install.packages(c("ggplot2", "devtools", "dplyr", "stringr"))
# install.packages(c("maps", "mapdata"))
# devtools::install_github("dkahle/ggmap")

library(ggplot2)
library(ggmap)
library(maps)
library(mapdata)

states <- map_data("state")
west_coast <- subset(states, region %in% c("california", "oregon", "washington"))

#> west_coast
#long      lat group order     region
#667   -120.0060 42.00927     4   667 california
#668   -120.0060 41.20139     4   668 california
#669   -120.0060 39.70024     4   669 california

ggplot(data = west_coast) + 
  geom_polygon(aes(x = long, y = lat, group = group), fill = "palegreen", color = "black") + 
  coord_fixed(1.3)

ca_df <- subset(states, region == "california")
counties <- map_data("county")
ca_county <- subset(counties, region == "california")
sbCounty <- subset(counties, subregion == "santa barbara")

ggplot(data = ca_df, mapping = aes(x = long, y = lat, group = group)) + 
  coord_fixed(1.3) + 
  geom_polygon(color = "black", fill = "gray") + 
  theme_nothing() +
  geom_polygon(data = ca_county, fill = NA, color = "white") +
  geom_polygon(color = "black", fill = NA) +  # get the state border back on top
  geom_polygon(data = sbCounty, aes(x = long, y = lat, group = group), fill = "palegreen", color = "black") 


ggplot(data = sbCounty) + 
   geom_polygon(aes(x = long, y = lat, group = group), fill = "palegreen", color = "black") + 
   coord_fixed(1.3)

sbbox <- make_bbox(lon = sbCounty$long, lat = sbCounty$lat, f = .1)
sq_map <- get_map(location = sbbox, maptype = "satellite", source = "google")

# CIMIS #231 google map-able coordinates : 34.672222, -120.51306
# Ampelos 34.625133, -120.280478
points.df <-dplyr::tribble(~name, ~lon, ~lat, "CIMIS-231", -120.51306, 34.672222, 
                           "Ampelos", -120.280478, 34.625133)

center <- sapply(points.df[2:3], mean)

sbbox <- make_bbox(lon = points.df$lon, lat = points.df$lat, f = .1)
# maptype =  "terrain"
sq_map <- get_map(location = center, maptype = "satellite", source = "google", zoom=10)
ggmap(sq_map) + 
  geom_point(data = points.df, mapping = aes(x = lon, y = lat), 
             color = "green", shape=13, size = 8, stroke=2) +
  geom_label(data = points.df, aes(label = paste(as.character(name), sep="")), 
            angle = 0, hjust = 0, nudge_x = 0.02)




