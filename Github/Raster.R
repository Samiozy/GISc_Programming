library(raster)
dem <- raster("./DEM.img")
tm_shape(dem) + tm_raster(palette = "Greys", n=8) +
  tm_legend(outside = TRUE, text.size = .8)
slope  <- terrain(dem, opt='slope')
aspect <- terrain(dem, opt='aspect')
hill   <- hillShade(slope, aspect, 40, 270)
tm_shape(hill) + tm_raster(palette = "Greys", style="cont", contrast = c(0,.8)) +
  tm_legend(show=TRUE)

library(rgdal)
me <- readOGR(".", "Income")

hill_me <- mask(hill, me)
tm_shape(hill_me) + tm_raster(palette = "Greys", style="cont", contrast = c(0,.8)) +
  tm_legend(show=FALSE)
me$Cutoff <- ifelse( me$Income > 23000, 1, 0)
qtm(me, fill="Cutoff", fill.style="cat")