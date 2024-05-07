import matplotlib.pyplot as plt
import networkx as nx
import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig as mc
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence
from ndlib.viz.bokeh.MultiPlot import MultiPlot
from bokeh.io import output_notebook, show, export_png

#SIR
g = nx.erdos_renyi_graph(1000, 0.1)
sir_model = ep.SIRModel(g)
cfg = mc.Configuration()
cfg.add_model_parameter('beta', 0.001) # infection rate
cfg.add_model_parameter('gamma', 0.01) # recovery rate
cfg.add_model_parameter("percentage_infected", 0.01)
sir_model.set_initial_status(cfg)
sir_iterations = sir_model.iteration_bunch(200)
sir_trends = sir_model.build_trends(sir_iterations)


#SI
si_model = ep.SIModel(g)
config = mc.Configuration()
config.add_model_parameter('beta', 0.001)
config.add_model_parameter("fraction_infected", 0.05)
si_model.set_initial_status(config)
si_iterations = si_model.iteration_bunch(200)
si_trends = si_model.build_trends(si_iterations)

sir_dt = DiffusionTrend(sir_model, sir_trends)
sir_plot = sir_dt.plot()
si_dt = DiffusionTrend(si_model, si_trends)
si_plot = si_dt.plot()

trend_plot = MultiPlot()
trend_plot.add_plot(sir_plot)
trend_plot.add_plot(si_plot)
mp = trend_plot.plot()
show(mp)