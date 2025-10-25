from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.data import gapminder

gapminder_df = gapminder()
continents = gapminder_df["continent"].unique()
years = sorted(gapminder_df["year"].unique())

css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"]
app = Dash(__name__, external_stylesheets=css)
app.title = "Gapminder Dashboard"

def create_bar_chart(df, y_col, title):
    df = df.sort_values(by=y_col, ascending=False).head(15)
    fig = px.bar(df, x="country", y=y_col, color="country", text_auto=True,
                 template="plotly_white", color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(height=500, margin=dict(t=50, l=20, r=20, b=20))
    return fig

def create_population_chart(continent="Asia", year=1952):
    df = gapminder_df[(gapminder_df["continent"]==continent) & (gapminder_df["year"]==year)]
    return create_bar_chart(df, "pop", f"Top 15 Populations in {continent} ({year})")

def create_gdp_chart(continent="Asia", year=1952):
    df = gapminder_df[(gapminder_df["continent"]==continent) & (gapminder_df["year"]==year)]
    return create_bar_chart(df, "gdpPercap", f"Top 15 GDP per Capita in {continent} ({year})")

def create_life_exp_chart(continent="Asia", year=1952):
    df = gapminder_df[(gapminder_df["continent"]==continent) & (gapminder_df["year"]==year)]
    return create_bar_chart(df, "lifeExp", f"Top 15 Life Expectancy in {continent} ({year})")

def create_choropleth_map(variable="lifeExp", year=1952):
    df = gapminder_df[gapminder_df["year"]==year]
    fig = px.choropleth(df, color=variable,
                        locations="iso_alpha", locationmode="ISO-3",
                        color_continuous_scale="RdYlBu",
                        hover_data=["country", variable],
                        title=f"{variable} Map ({year})")
    fig.update_layout(paper_bgcolor="#f8f9fa", height=600, margin={"l":0, "r":0})
    return fig

# ---------------- 控件 ----------------
def continent_dropdown(id_value, default="Asia"):
    return dcc.Dropdown(
        id=id_value,
        options=[{"label": c, "value": c} for c in continents],
        value=default, clearable=False
    )

def year_dropdown(id_value, default=1952):
    return dcc.Dropdown(
        id=id_value,
        options=[{"label": y, "value": y} for y in years],
        value=default, clearable=False
    )

app.layout = html.Div([
    # 标题
    html.Div([
        html.H1("Gapminder Dashboard", className="text-center text-primary fw-bold my-3")
    ], className="container"),

    # Tabs
    dcc.Tabs([
        # Dataset Tab
        dcc.Tab([dcc.Graph(
            id="dataset",
            figure=go.Figure(data=[go.Table(
                header=dict(values=list(gapminder_df.columns), align='left'),
                cells=dict(values=[gapminder_df[col] for col in gapminder_df.columns], align='left')
            )]).update_layout(paper_bgcolor="#f8f9fa", margin=dict(t=0,l=0,r=0,b=0), height=600)
        )], label="Dataset"),

        # Population Tab
        dcc.Tab([
            html.Div([
                html.Div([
                    html.Label("Select Continent:", className="fw-semibold"),
                    continent_dropdown("cont_pop"),
                    html.Label("Select Year:", className="fw-semibold mt-3"),
                    year_dropdown("year_pop")
                ], className="col-md-3"),

                html.Div([
                    html.Div([dcc.Graph(id="population")],
                             className="card p-3 shadow-sm",
                             style={"background-color":"#ffffff","border-radius":"10px"})
                ], className="col-md-9")
            ], className="row g-4 container mt-3")
        ], label="Population"),

        # GDP Tab
        dcc.Tab([
            html.Div([
                html.Div([
                    html.Label("Select Continent:", className="fw-semibold"),
                    continent_dropdown("cont_gdp"),
                    html.Label("Select Year:", className="fw-semibold mt-3"),
                    year_dropdown("year_gdp")
                ], className="col-md-3"),

                html.Div([
                    html.Div([dcc.Graph(id="gdp")],
                             className="card p-3 shadow-sm",
                             style={"background-color":"#ffffff","border-radius":"10px"})
                ], className="col-md-9")
            ], className="row g-4 container mt-3")
        ], label="GDP per Capita"),

        # Life Expectancy Tab
        dcc.Tab([
            html.Div([
                html.Div([
                    html.Label("Select Continent:", className="fw-semibold"),
                    continent_dropdown("cont_life_exp"),
                    html.Label("Select Year:", className="fw-semibold mt-3"),
                    year_dropdown("year_life_exp")
                ], className="col-md-3"),

                html.Div([
                    html.Div([dcc.Graph(id="life_expectancy")],
                             className="card p-3 shadow-sm",
                             style={"background-color":"#ffffff","border-radius":"10px"})
                ], className="col-md-9")
            ], className="row g-4 container mt-3")
        ], label="Life Expectancy"),

        # Choropleth Map Tab
        dcc.Tab([
            html.Div([
                html.Div([
                    html.Label("Select Variable:", className="fw-semibold"),
                    dcc.Dropdown(
                        id="var_map",
                        options=[
                            {"label":"Population","value":"pop"},
                            {"label":"GDP per Capita","value":"gdpPercap"},
                            {"label":"Life Expectancy","value":"lifeExp"}],
                        value="lifeExp", clearable=False
                    ),
                    html.Label("Select Year:", className="fw-semibold mt-3"),
                    year_dropdown("year_map")
                ], className="col-md-3"),

                html.Div([
                    html.Div([dcc.Graph(id="choropleth_map")],
                             className="card p-3 shadow-sm",
                             style={"background-color":"#ffffff","border-radius":"10px"})
                ], className="col-md-9")
            ], className="row g-4 container mt-3")
        ], label="Choropleth Map")
    ])
], style={"background-color":"#f8f9fa", "padding":"20px"})

# ---------------- 回调 ----------------
@callback(Output("population","figure"), [Input("cont_pop","value"), Input("year_pop","value")])
def update_population_chart(continent, year):
    return create_population_chart(continent, year)

@callback(Output("gdp","figure"), [Input("cont_gdp","value"), Input("year_gdp","value")])
def update_gdp_chart(continent, year):
    return create_gdp_chart(continent, year)

@callback(Output("life_expectancy","figure"), [Input("cont_life_exp","value"), Input("year_life_exp","value")])
def update_life_exp_chart(continent, year):
    return create_life_exp_chart(continent, year)

@callback(Output("choropleth_map","figure"), [Input("var_map","value"), Input("year_map","value")])
def update_choropleth_map(variable, year):
    return create_choropleth_map(variable, year)

# ---------------- 启动 ----------------
if __name__ == "__main__":
    app.run(debug=True, port=8051)
