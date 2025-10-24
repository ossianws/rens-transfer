
from app import app
from flask import render_template
from app.visuals import generate_graph

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


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


