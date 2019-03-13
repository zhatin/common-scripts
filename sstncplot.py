#-*- coding: utf-8 -*-

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.font_manager import *
import xarray as xr

import metpy.calc as mpcalc
from metpy.units import units

import numpy as np

ptime = '2019-02-01'

fontprop = FontProperties(fname='/usr/share/fonts/windows/msyh.ttf')

data = xr.open_dataset('sst.mon.mean.nc')

data_var = data.metpy.parse_cf('sst')
lon = data.metpy.parse_cf('lon')
lat = data.metpy.parse_cf('lat')

data_crs = data_var.metpy.cartopy_crs

fig = plt.figure(figsize=(14, 7))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree(central_longitude=180))

ax.set_xlabel('经度', fontproperties=fontprop)
ax.set_xticklabels([0,60,120,180,120,60,0])
ax.set_xticks([-180,-120,-60,0,60,120,180], False)

ax.set_ylabel('纬度', fontproperties=fontprop)
ax.set_yticklabels([90,80,60,40,20,0,20,40,60,80,90])
ax.set_yticks([90,80,60,40,20,0,20,40,60,80,90],True)

ax.coastlines()
# ax.stock_img()

ax.add_feature(cfeature.BORDERS, linewidth=0.3)
ax.add_feature(cfeature.RIVERS, linewidth=0.3)
ax.add_feature(cfeature.LAKES, linewidth=0.2)

ax.gridlines()

ax.set_title('海表温度（每月）', loc='left', fontproperties=fontprop)
ax.set_title('全球海表温度图示', loc='center', fontproperties=fontprop)
ax.set_title('时间: {}'.format(ptime), loc='right', fontproperties=fontprop)

cs = ax.contour(lon, lat, data_var.metpy.loc[{'time': ptime}], levels=range(0, 35, 5), transform=ccrs.PlateCarree(),
                colors='k', linewidths=1.0, linestyles='solid')
ax.clabel(cs, fontsize=10, inline=1, inline_spacing=7,
          fmt='%i', rightside_up=True, use_clabeltext=True)

cf = ax.contourf(lon, lat, data_var.metpy.loc[{'time': ptime}], levels=range(-5, 40, 1), cmap=plt.cm.coolwarm,
                 transform=ccrs.PlateCarree())

cb = fig.colorbar(cf, orientation='horizontal', extend='max', aspect=65, shrink=0.5,
                  extendrect='True')
cb.set_label('图例（degC）', size='x-large', fontproperties=fontprop)

fig.suptitle('SST netCDF测试出图', fontsize=14, fontproperties=fontprop)

# plt.show()

plt.savefig('sst-' + ptime + '.jpg', dpi=300)
