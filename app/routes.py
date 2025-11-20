
from flask import render_template, Blueprint, url_for, redirect, flash, current_app, abort
from app.test_visuals import generate_graph, get_graph_ids
from app.forms import LoginForm, UploadForm
from app.models import Graph
from app.data import graph_list
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
from flask_login import login_user, logout_user, current_user, login_required


main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
def dashboard():
    id_list = get_graph_ids()

    return render_template('dashboard.html',frames=id_list)

@main_bp.route('/dashboard/<graph_id>')
def graph_endpoint(graph_id):
    
    g = Graph.query.get_or_404(int(graph_id))
    
    if not current_user.is_authenticated:
        if not g.public:
            abort(403)
    graph_json = g.data
    
    return render_template('graph.html',graph_json=graph_json,graph_id=graph_id)

#individual graph endpoint
@main_bp.route('/dashboard/test/<graph_id>')
def test_graph_endpoint(graph_id):
    try:
        graph_list[str(graph_id)]
    except KeyError as k:
        abort(404)
    if not current_user.is_authenticated:
        if not graph_list[str(graph_id)]['public']:
            abort(403)
        else:
            pass
    print(f"Generating graph for ID: {graph_id} with type {type(graph_id)}")
    fig = generate_graph(graph_id)

    graph_json= fig.to_dict()
    return render_template('graph.html',graph_json=graph_json, graph_id=graph_id)


@main_bp.route('/upload', methods=['GET','POST'])
@login_required
def upload():
    form = UploadForm()

    if form.validate_on_submit():

        f = form.file_field.data
        filename = secure_filename(f.filename)
        destination_dataset = form.destination.data
        current_app.logger.info(f"Form validated successfully with {filename} and {destination_dataset}")
        
        if not current_app.testing:
            f.save(os.path.join(os.path.join(os.getcwd(), 'app/uploads', filename)))
            flash(f'Your file {filename} was uploaded',category='info')
        flash(f'File {filename} would be saved to {destination_dataset} in a non-testing environment.',category='warning')
        return redirect(url_for('main.index'))
    
    current_app.logger.info(f"choice field {form.destination.data}")
    return render_template('upload.html', form=form)



@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!',category='info')
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        form_password = form.password.data

        admin_user = current_app.config['ADMIN_USER']

        admin_hash = admin_user.password_hash
        admin_username = admin_user.username
        if username != admin_username or not check_password_hash(admin_hash,form_password):
            flash('Invalid username or password',category='error')
            return redirect(url_for('main.login'))
        
        login_user(admin_user,remember=form.remember_me.data)
        current_app.logger.info("Logged in admin")
        flash('Logged in successfully.',category='info')
        return redirect(url_for('main.index'))
    
    return render_template('login.html', form=form)


@main_bp.route('/logout')
def logout():
    logout_user()
    flash("Successfully logged out.", category='info')
    current_app.logger.info("Logged out admin")
    return redirect(url_for('main.index'))

@main_bp.route('/internal-error')
def internal_error():
    return render_template('does not exist.html')