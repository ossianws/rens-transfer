from flask import Flask, render_template
#from dash import Dash, html, dcc
import plotly.graph_objs as go
import plotly
from data import graph_list
import json


app = Flask(__name__)


def generate_graph(id):
    data_tuple = graph_list[id]
    if data_tuple[2] == 'scatter':
        fig = go.Figure(data=go.Scatter(x=data_tuple[0].tolist(), y=data_tuple[1].tolist(), mode = "markers"))
        fig.update_layout(title=f'Scatter Plot for Graph {id}', xaxis_title='X Axis', yaxis_title='Y Axis')
    if data_tuple[2] == 'bar':
        fig = go.Figure(data=go.Bar(x=data_tuple[0].tolist(), y=data_tuple[1].tolist()))
        fig.update_layout(title=f'Bar Chart for Graph {id}', xaxis_title='X Axis', yaxis_title='Y Axis')
    
    return fig


@app.route('/dashboard')
def dashboard_home():
    return


#individual graph endpoint
@app.route('/dashboard/<graph_id>')
def graph_endpoint(graph_id):
    print(f"Generating graph for ID: {graph_id} with type {type(graph_id)}")
    fig = generate_graph(graph_id)

    graph_json= fig.to_dict()
    return render_template('graph.html',graph_json=graph_json, graph_id=graph_id)




#non-dash endpoint
@app.route('/')
def index():
    return render_template('index.html')






#run locally
if __name__ == '__main__':
    app.run(debug=True)
