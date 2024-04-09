import pandas as pd
import numpy as np
from scipy.stats import zscore
import matplotlib.pyplot as plt
import seaborn as sns
import random
import folium
import os, shutil, getpass
if 'results' in os.listdir(): shutil.rmtree('results')
os.mkdir('results')
data_dir = os.path.join('/home', getpass.getuser(), 'data')

'''
Source: https://www.kaggle.com/competitions/store-sales-time-series-forecasting
Dataset: train.csv
store_nbr: the store at which the products are sold.
family: the type of product sold.
sales: the total sales for a product family at a particular store at a given date. 
Fractional values are possible since products can be sold in fractional units 
(1.5 kg of cheese, for instance, as opposed to 1 bag of chips).
onpromotion: the total number of items in a product family that were being promoted at a store at a given date.
'''
print('Pandas dataframe: Sales data')
sales = pd.read_csv(os.path.join(data_dir, 'sales.csv.zip'))
sales = sales.rename(columns={'family':'product_type', 'store_nbr': 'store_id'})
# Remove product categories
categories = ['GROCERY I', 'GROCERY II', 'HOME AND KITCHEN I', 'HOME AND KITCHEN II']
sales = sales[~sales['product_type'].isin(categories)]
print(sales.head())
print('Sales values')
print(sales['sales'].value_counts())
print('Sales grouped by family')
sales_sum = sales.groupby('product_type')['sales'].sum()
sales_sum = pd.DataFrame(list(zip(sales_sum.index, sales_sum.values)), columns = ['product', 'items'])
sales_sum['z_score'] = sales_sum[['items']].transform(zscore)
#print(sales_sum)
print('mean zscore=', np.mean(np.abs((sales_sum['z_score']))))
bar_plot_data = sales_sum[sales_sum['product'].isin(['EGGS', 'DAIRY', 'MEATS', 'POULTRY', 'SEAFOOD', 'BREAD/BAKERY'])]

# Add locations
loc = (51.5072, 0.1276)  # London 51.5072° N, 0.1276° W
locations = [(loc[0]+i, loc[1]+i) for i in np.arange(0.1,0.7, 0.1)]
sales_sum['location'] = random.choices(locations, k=len(sales_sum))

print(bar_plot_data)
print('Prepare and save bar plots')
bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
food, sum = list(bar_plot_data['product']), list(bar_plot_data['items'])
plt.bar(food, sum, color=bar_colors)
plt.savefig('results/matplotlib_fig.png')
sns.barplot(x='product', y='items', data=bar_plot_data)
plt.savefig('results/seaborn_fig.png')

# Bokeh test
from bokeh.models import ColumnDataSource
from bokeh.palettes import Bright6
from bokeh.plotting import figure, save, output_file, show
from bokeh.transform import factor_cmap

source = ColumnDataSource(data=dict(food=food, sum=sum))
TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,\
box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,examine,help"
p = figure(x_range=food, height=350, tools=TOOLS, title="Fruit sum")
p.vbar(x='food', top='sum', width=0.9, source=source, legend_field="food",
       line_color='white', fill_color=factor_cmap('food', palette=Bright6, factors=food))
p.xgrid.grid_line_color = None
# p.y_range.start = 0
# p.y_range.end = 9
p.legend.orientation = "horizontal"
p.legend.location = "top_center"
output_file("results/sales.html")
save(p)

m = folium.Map(location=loc, zoom_start=4)
tooltip = "Click me!"
for location in locations:
    folium.Marker(location, popup="<i>Mt. Hood Meadows</i>", tooltip=tooltip).add_to(m)
m.save("results/london_locs.html")