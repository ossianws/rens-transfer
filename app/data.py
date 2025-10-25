import plotly.express as px

graph_list = {
    "1":{
        'data':(px.data.iris()['petal_length'],px.data.iris()['petal_width']),
        'type':'scatter',
        'title':'Petal Length by Petal Width'
    },
    "2":{
       'data':(px.data.iris()['sepal_width'],px.data.iris()['sepal_length']),
       'type':'bar',
        'title':'Sepal Width by Sepal Length'
       },
    '3':{
        'data':px.data.iris()['species'],
        'type':'pie',
        'title':'Species of Irises'
        }
}