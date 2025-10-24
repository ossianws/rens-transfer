
from app.data import graph_list
import plotly.graph_objs as go

def generate_graph(id):
    data_tuple = graph_list[id]
    if data_tuple[2] == 'scatter':
        fig = go.Figure(data=go.Scatter(x=data_tuple[0].tolist(), y=data_tuple[1].tolist(), mode = "markers"))
        fig.update_layout(title=f'Scatter Plot for Graph {id}', xaxis_title='X Axis', yaxis_title='Y Axis')
    elif data_tuple[2] == 'bar':
        fig = go.Figure(data=go.Bar(x=data_tuple[0].tolist(), y=data_tuple[1].tolist()))
        fig.update_layout(title=f'Bar Chart for Graph {id}', xaxis_title='X Axis', yaxis_title='Y Axis')
    
    return fig