# -*-*- coding: utf-8 -*
import arcpy, os
from arcpy import env
from arcpy.sa import *

work_path = r"D:\任务\饮用水"
env.workspace = work_path
arcpy.CheckOutExtension("Spatial")

# 填洼
dem_tif = r"吉安县金山水厂（禾水）集中式饮用水源地保护区及基础资料\基础数据\dem30m.tif"
outFill = Fill(dem_tif)
# outFill.save(r"D:\任务\饮用水\代码数据/填洼.tif")

# 计算流向
outFlowDirection = FlowDirection(outFill)
# outFlowDirection.save(r"D:\任务\饮用水\代码数据\流向.tif")

# 计算流量
outFlowAccumulation = FlowAccumulation(outFlowDirection)
#outFlowAccumulation.save(r"D:\任务\饮用水\代码数据\流量.tif")

# 栅格河网
outCon = Con(outFlowAccumulation, 1, "", "VALUE >= 1500")
# outCon.save(r"D:\任务\饮用水\代码数据\栅格河网.tif")

#河流连接
outStreamLink = StreamLink(outCon, outFlowDirection)
# outStreamLink.save(r"D:\任务\饮用水\代码数据\河流连接.tif")

#河网分级
orderMethod = "STRAHLER"
outStreamOrder = StreamOrder(outStreamLink, outFlowDirection, orderMethod)
# outStreamOrder.save(r"D:\任务\饮用水\代码数据\河网分级.tif")

# 河网分级转成矢量
outStreamFeats = r"D:\任务\饮用水\代码数据\河网分级矢量"
# StreamToFeature(outStreamOrder, outFlowDirection, outStreamFeats, "NO_SIMPLIFY")

# 捕捉倾泻点
"""
自行导入倾泻点.shp
"""
inPourPoint = r"D:\任务\饮用水\代码数据\倾泻点.shp"
inFlowAccum = outFlowDirection
tolerance = 0
pourField = "OBJECTID"
outSnapPour = SnapPourPoint(inPourPoint, inFlowAccum, tolerance, pourField)
# outSnapPour.save("D:\任务\饮用水\代码数据\捕捉结果.tif")

# 集水区(分水岭)
inFlowDirection = outFlowDirection
inPourPointData = outSnapPour
inPourPointField = "VALUE"
outWatershed = Watershed(inFlowDirection, inPourPointData, inPourPointField)
# outWatershed.save(r"D:\任务\饮用水\代码数据\分水岭.tif")

# 分水岭转矢量
inRaster = outWatershed
outPolygons = r"D:\任务\饮用水\代码数据\分水岭矢量.shp"
field = "VALUE"
# Execute RasterToPolygon
arcpy.RasterToPolygon_conversion(inRaster, outPolygons, "NO_SIMPLIFY", field)

"""
# Set local variables
inRaster = "zone"
outPolygons = "c:/output/zones.shp"
field = "VALUE"
# Execute RasterToPolygon
arcpy.RasterToPolygon_conversion(inRaster, outPolygons, "NO_SIMPLIFY", field)

"""












