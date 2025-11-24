from app.graphs import bp
from app.models import Graph
from flask import abort,render_template, redirect, url_for, current_app
from flask_login import current_user
from jinja2.exceptions import TemplateNotFound


@bp.route('/graph/<graph_id>')
def graph_endpoint(graph_id):
    if not graph_id:
        return redirect(url_for('main.dashboard'))
    try:
        id = int(graph_id)
        g = Graph.query.get(id)
        if g is None:
            return render_template('errors/basic404.html'), 404
    except ValueError as e:
        return render_template('errors/basic404.html'), 404
    
    if not current_user.is_authenticated:
        if not g.public:
            abort(403)
    #graph_json = json.dumps(g.data)
    
    name = g.name
    try:
        return render_template(f'graphs/{name}.html')
    except TemplateNotFound:
        print(f"Couldn't find graphs/{name}.html")
        abort(404)
