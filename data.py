import plotly.express as px

graph_list = {
    "A":(px.data.iris()['petal_length'],px.data.iris()['petal_width'],"scatter"),
    "B":(px.data.iris()['sepal_width'],px.data.iris()['sepal_length'], "bar")
}