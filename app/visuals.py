
from app.data import graph_list
import plotly.graph_objs as go

def generate_graph(id):
    data_dict = graph_list[id]
    graph_type=data_dict['type']
    data = data_dict['data']
    if graph_type == 'scatter':
        fig = go.Figure(data=go.Scatter(x=data[0].tolist(), y=data[1].tolist(), mode = "markers"))
        fig.update_layout(title=data_dict['title'], xaxis_title='X Axis', yaxis_title='Y Axis')
    elif graph_type == 'bar':
        fig = go.Figure(data=go.Bar(x=data[0].tolist(), y=data[1].tolist()))
        fig.update_layout(title=data_dict['title'], xaxis_title='X Axis', yaxis_title='Y Axis')
    elif graph_type == "pie":
        fig = go.Figure(data=go.Pie(labels=data.tolist()))
        fig.update_layout(title=data_dict['title'])
    
    else:
        raise TypeError("Unrecognised graph type")
    return fig

def get_graph_ids():
    return [(graph_id,graph_list[graph_id]['title']) for graph_id in graph_list]

