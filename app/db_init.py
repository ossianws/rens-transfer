#from app import db
from app.models import Graph
from flask_sqlalchemy import SQLAlchemy
from app.visuals import facebook

#this will fill the database with graphs (only if it's already empty)
#It must be called inside a WITH statement of flask app context
def populate_db(generator_path_dict:dict,db:SQLAlchemy):
    """
    generator_path_dict should take the form {name: (generator-function,path)}
    """
    
    existing_graphs = Graph.query.all()

    if len(existing_graphs)!=0:
        db.session.rollback()
        raise Exception("Database is not empty. Use empty_db() before population.")
    
    
    for name,(function,path) in generator_path_dict.items():
        
        graph_dict = str(function(path))
        g = Graph(name=name,data=graph_dict)
        print(f'Adding {g} to the db session')
        db.session.add(g)

    db.session.commit()
    print('DB committed')


#nuclear - clear graphs from db. 
#Like populate_db, requires application context.
def empty_db(db):

    graphs = Graph.query.all()
    for g in graphs:
        db.session.delete(g)
    db.session.commit()
    

generators = {'facebook-followers':(facebook,'app/datasets/Facebook.csv')}