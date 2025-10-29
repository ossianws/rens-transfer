
from flask import render_template, Blueprint, url_for, redirect, flash, current_app
from app.visuals import generate_graph, get_graph_ids
from app.forms import UploadForm, TestForm
from werkzeug.utils import secure_filename
import os


main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
def dashboard():
    id_list = get_graph_ids()

    return render_template('dashboard.html',frames=id_list)


#individual graph endpoint
@main_bp.route('/dashboard/<graph_id>')
def graph_endpoint(graph_id):
    print(f"Generating graph for ID: {graph_id} with type {type(graph_id)}")
    fig = generate_graph(graph_id)

    graph_json= fig.to_dict()
    return render_template('graph.html',graph_json=graph_json, graph_id=graph_id)


@main_bp.route('/upload', methods=['GET','POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():

        f = form.file_field.data
        filename = secure_filename(f.filename)
        destination_dataset = form.destination.data
        current_app.logger.info(f"Form validated successfully with {filename} and {destination_dataset}")
        
        if not current_app.testing:
            f.save(os.path.join(os.path.join(os.getcwd(), 'app/uploads', filename)))
            flash(f'Your file {filename} was uploaded')
        flash(f'File {filename} would be saved to {destination_dataset} in a non-testing environment.')
        return redirect(url_for('main.index'))
    
    current_app.logger.info(f"choice field {form.destination.data}")
    return render_template('upload.html', form=form)






@main_bp.route('/')
def index():
    return render_template('index.html')


