library(tmap)
library(dplyr)
library(rgdal)
setwd("C:/Users/Samuel/Documents/GEOG_592/Lab8/Data")

feature <- readOGR(".", "STATES")
textfile <- read.csv("./gas.csv")
feature@data <- left_join(feature@data, textfile, by=c("STATE_NAME" = "State"))
qtm(feature, fill="Regular", fill.style="quantile", 
    fill.n=5,
    fill.palette="Greens",
    legend.text.size = 0.5,
    layout.legend.position = c("right", "top"))
