library(tmap)
library(dplyr)
library(rgdal)
library(rgeos)
library(raster)
setwd("C:/Users/Samuel/Documents/GEOG_592/Lab8/Data")


Aug_UTM <- spTransform(Aug_ll, CRS("+init=epsg:26919"))
Aug_UTM <- spTransform(Aug_ll, CRS("+proj=utm +zone=19 +datum=NAD83 +units=m +no_defs +ellps=GRS80 +towgs84=0,0,0"))
dis50 <- buffer(Aug_UTM, width=50000, quadsegs=10)
dis100 <- buffer(Aug_UTM, width=100000, quadsegs=10)
dis150 <- buffer(Aug_UTM, width=150000, quadsegs=10)
dis200 <- buffer(Aug_UTM, width=200000, quadsegs=10)
dis300 <- buffer(Aug_UTM, width=300000, quadsegs=10)

me <- readOGR(".", "Income")
tm_shape(dis300) +tm_borders() +tm_shape(dis200) +tm_borders() +tm_shape(dis150) +tm_borders() +tm_shape(dis100) +tm_borders() + tm_shape(dis50) +tm_borders() +tm_shape(me) +tm_borders()
dAll <- union(dis50, dis100)
dAll <- union(dis150, dAll)
dAll <- union(dis200, dAll)
dAll <- union(dis300, dAll)
dAll$ID <- 1:length(dAll)
dAllme <- crop(dAll, me)

dAllme$Area_band <- gArea(dAllme, byid=TRUE) / 1000000
qtm(dAllme, fill="Area_band")
clp1 <- intersect(me, dAllme)
tm_shape(clp1) + tm_fill(col="Income") + tm_borders()

clp1$Area_sub <- gArea(clp1, byid=TRUE) / 1000000

# Compute the polygon's fraction vis-a_vis the distance band's area
clp1$frac_area <- clp1$Area_sub / clp1$Area_band

# Mutiply income by area fraction--this is the weighted income within each distance band
clp1$wgt_inc <- clp1$Income * clp1$frac_area

dist_inc <- aggregate(clp1, by="ID",sums= list(list(sum, "wgt_inc")))
qtm(dist_inc, fill="wgt_inc") 
