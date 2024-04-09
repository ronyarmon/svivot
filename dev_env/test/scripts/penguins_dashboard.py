#!/usr/bin/env python
# coding: utf-8

# # Palmer Archipelago (Antarctica) penguin data
# source: https://towardsdatascience.com/using-panel-to-build-data-dashboards-in-python-e87a04c9034d  
# dataset: https://www.kaggle.com/datasets/parulpandey/palmer-archipelago-antarctica-penguin-data

import os, getpass
import pandas as pd
import holoviews as hv
import hvplot.pandas
import panel as pn
from pylab import *
hv.extension('bokeh')
pn.extension()
print('script', os.path.basename(__file__) )

# Data
data_dir = os.path.join('/home', getpass.getuser(), 'data')
dfPenguins = pd.read_csv(os.path.join(data_dir, 'penguins_lter.csv'))
columns = list(dfPenguins.columns)
x = pn.widgets.Select(value='Culmen Length (mm)', options=columns, name='x')
y = pn.widgets.Select(value='Flipper Length (mm)', options=columns, name='y')
dashboard = pn.Row(pn.Column('## Penguins', x, y),
       pn.bind(dfPenguins.hvplot.scatter, x, y, by='Species'))
from bokeh.resources import INLINE
dashboard.save('results/penguins_dashboard.html', resources=INLINE)
dashboard.servable()
