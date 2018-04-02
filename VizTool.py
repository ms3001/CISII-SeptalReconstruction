'''
Manyu Sharma 
Rohit Joshi
CIS 2
3D Data visualization
'''

from plotly.offline import iplot
import plotly.graph_objs as go
import plotly

plotly.offline.init_notebook_mode()


def visualize(dataSources, start, end):

	data = []
	

	for d in dataSources:
		x = [d[i][0,0] for i in range(start, end)]
		y = [d[i][0,1] for i in range(start, end)]
		z = [d[i][0,2] for i in range(start, end)]

		trace = go.Scatter3d(
			x=x,
			y=y,
			z=z,
			mode='line',
			marker=dict(
				size=1,
				line=dict(
					color='rgba(217, 217, 217, 0.14)',
					width=2
				),
					opacity=0.8
			)
		)

		data.append(trace)

	layout = go.Layout(
		margin=dict(
			l=0,
			r=0,
			b=0,
			t=0
		)
	)

	fig = go.Figure(data=data, layout=layout)
	iplot(fig, validate=False)
