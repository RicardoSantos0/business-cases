import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

###################################################### Data ##############################################################

df = pd.read_csv('Databases/final_df.csv',dtype={'ProductFamily_ID': np.int16,
                                         'ProductCategory_ID  ': np.int16,
                                         'ProductBrand_ID': np.int16,
                                         'ProductName_ID': np.int16,
                                         'ProductPackSKU_ID': np.int16,
                                         'Point-of-Sale_ID': np.int16,
                                         'Value_units': np.float32,
                                         'Value_price': np.float32,
                                         'Unit_Price': np.float32,
                                         'Retail_price': np.float32,
                                         'Is_Promo': np.int16,
                                        })
df.drop(columns='Unnamed: 0', inplace=True)

complementary = pd.read_csv('Databases/complementary_df.csv')
substitutes = pd.read_csv('Databases/substitutes_df.csv')

######################################################Interactive Inputs Components############################################

store_input = dcc.Input(
    id='store_input',
    placeholder='Enter a Store ID',
    type='number',
    min=1,
    max=410,
    value=292,
    style = {'text-align': 'center'},
)

number_categories_input = dcc.Input(
    id='number_categories_input',
    placeholder='Enter the number of categories',
    type='number',
    min=1,
    max=100,
    value=3,
    style = {'text-align': 'center'},

)

number_products_input = dcc.Input(
    id='number_products_input',
    placeholder='Enter the number of products',
    type='number',
    min=1,
    max=100,
    value=3,
    style = {'text-align': 'center'},
)

number_stores_input = dcc.Input(
    id='number_stores_input',
    placeholder='Enter the number of stores',
    type='number',
    min=1,
    max=100,
    value=5,
    style = {'text-align': 'center'},

)

type_analysis_input = dcc.RadioItems(
    id='type_analysis_input',
    options=[
        {'label': 'Value', 'value': 'value'},
        {'label': 'Units', 'value': 'units'},
    ],
    value='units',
    style = {'text-align': 'center', 'color': 'white'}
)  

type_association_input = dcc.RadioItems(
    id='type_association_input',
    options=[
        {'label': 'Complementary', 'value': 'Complementary'},
        {'label': 'Substitutes', 'value': 'Substitutes'},
    ],
    value='Substitutes',
    style = {'text-align': 'center', 'color': 'white'},

)  

aggregated_quarter_input = dcc.Slider(
    id='aggregated_quarter_input',
    marks={str(i): '{}'.format(str(i)) for i in
            [1, 2, 3, 4]},
    min=1,
    max=4,
    value=1,
    step=1,
    )

quarter_input = dcc.Dropdown(
    id='quarter_input',
    options=[
        {'label': 'Total', 'value': 'total'},
        {'label': '2016Q1', 'value': '2016Q1'},
        {'label': '2016Q2', 'value': '2016Q2'},
        {'label': '2016Q3', 'value': '2016Q3'},
        {'label': '2016Q4', 'value': '2016Q4'},
        {'label': '2017Q1', 'value': '2017Q1'},
        {'label': '2017Q2', 'value': '2017Q2'},
        {'label': '2017Q3', 'value': '2017Q3'},
        {'label': '2017Q4', 'value': '2017Q4'},
        {'label': '2018Q1', 'value': '2018Q1'},
        {'label': '2018Q2', 'value': '2018Q2'},
        {'label': '2018Q3', 'value': '2018Q3'},
        {'label': '2018Q4', 'value': '2018Q4'},
        {'label': '2019Q1', 'value': '2019Q1'},
        {'label': '2019Q2', 'value': '2019Q2'},
        {'label': '2019Q3', 'value': '2019Q3'},
        {'label': '2019Q4', 'value': '2019Q4'},
    ],
    value='total',
)  

cluster_input = dcc.Dropdown(
    id='cluster_input',
    options=[
        {'label': 'Cluster 0', 'value': 0},
        {'label': 'Cluster 1', 'value': 1},
        {'label': 'Cluster 2', 'value': 2},
        {'label': 'Cluster 3', 'value': 3},
        {'label': 'Cluster 4', 'value': 4},
    ],
    value=1,
)  

############################################ FIXED CHARTS ########################################################
def cluster_sales_scatter():
    plot_data = []
    
    for cluster in df.clusters.unique():
        df_plot = df[df['clusters']==cluster]
        df_plot = df_plot[['clusters','Quarter','Value_price']]

        temp_df_plot = df_plot.groupby('Quarter')['Value_price'].sum()

        comp_cum = dict(type='scatter',
                            x=temp_df_plot.index,
                            y=temp_df_plot.values,
                            name=f'Cluster {cluster}',
                            #marker = dict(color= 'orange')
                           )

        plot_data.append(comp_cum)

    _fig = go.Figure(data=plot_data)
    _fig.update_xaxes(tickangle = 310,showgrid=False)
    _fig.update_yaxes(gridwidth=1, gridcolor='#aaaaaa')
    _fig.update_layout(
        font= {'color': 'white','size':15},
        plot_bgcolor = '#343434',
        paper_bgcolor = '#343434',
    )
    return _fig

def cluster_bar_prods():
    #colors = ['red','green','yellow','black','blue']
    plot_data = []
    #i=0
    for cluster in df.clusters.unique():
        df_plot = df[df['clusters']==cluster]
        df_plot["ProductName_ID"] = df_plot["ProductName_ID"].astype(str)

        df_plot = df_plot['ProductName_ID'].value_counts().head(10)

        comp_bar = dict(type='bar',
                        x=df_plot.index,
                        y=df_plot.values,
                        name=f'Cluster {cluster}',
                        #marker = dict(color= colors[i]),
                       )

        plot_data.append(comp_bar)
        #i+=1
        

    _fig = go.Figure(data=plot_data)
    _fig.update_xaxes(tickangle = 310)
    _fig.update_layout(
        font= {'color': 'white','size':15},
        plot_bgcolor = '#343434',
        paper_bgcolor = '#343434',
    )
    return _fig
################################################## APP ###################################################################
app = dash.Dash(__name__)
app.title = 'Mind Over Data Dash'

server = app.server

app.layout = html.Div([
    #main title
    html.H1('MIND OVER DATA SALES DASHBOARD', className='box box_title',style={'font-size': '40px',}),

############# SECTION 1 ######################    
    html.Div([
        
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Select the Quarter'),
                    quarter_input,
                ], style={'width': '100%'}, className='box box_graph'),   
            ], className='row'),

            #best_worst_bar_chart
            dcc.Loading(
                id='loading_best_worst_bar_chart',
                children=[dcc.Graph(id='best_worst_bar_chart')],
                type='circle'
            )
        ], style={'width': '50%'}, className='box box_graph'),
        
        
        html.Div([
             html.Div([
                 html.Div([
                    html.H3('Select nº of Stores'),
                    html.Div([number_stores_input],style=dict(display='flex', justifyContent='center')),

                ],style={'width': '33%'}, className='box box_graph'),

                html.Div([
                    html.H3('Select nº of Categories'),
                    html.Div([number_categories_input],style=dict(display='flex', justifyContent='center')),
                ],style={'width': '34%'}, className='box box_graph'),
                
                html.Div([
                    html.H3('Select nº of Products'),
                    html.Div([number_products_input],style=dict(display='flex', justifyContent='center')),

                ],style={'width': '33%'}, className='box box_graph'),
            ], className='row'),

            #sunburst
            dcc.Loading(
                id='loading_sunburst',
                children=[dcc.Graph(id='sunburst')],
                type='circle'
            )
        ], style={'width': '50%'}, className='box box_graph'),
    ], className='row'),

############# SECTION 2 ######################    

    html.H2('Explore Statistics by Store', className='box box_title',style={'font-size': '40px',}),
   
    html.Div([
        html.Div([
            html.Div([
                html.H3(['Select the Store']),
                html.Div([store_input], style={'text-align': 'center'}),
            ]),
            dcc.Loading(
                id='loading_quarter_scatter_bar',
                children=[dcc.Graph(id='quarter_scatter_bar')],
                type='circle'
            ),
        ], style={'width': '50%'}, className='box box_graph'),
        html.Div([
            html.H3(['Select the Type of Data']),
            html.Div([type_analysis_input], style={'text-align': 'center'}),
            dcc.Loading(
                id='loading_market_share_pie',
                children=[dcc.Graph(id='market_share_pie')],
                type='circle'
            ),
        ], style={'width': '50%'}, className='box box_graph'),
    ], className='row'),


    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3(['Select the Type of Association']),
                    type_association_input,
                ], style={'width': '25%'}),
                html.Div([
                    html.H3(['Select the Quarter']),
                    aggregated_quarter_input,
                ], style={'width': '75%'}),
            ], className='row'),
            dcc.Loading(
                id='loading_asssociation_table',
                children=[dcc.Graph(id='asssociation_table')],
                type='circle'
            ),
        ], style={'width': '100%'}, className='box box_graph'),
    ], className='row'),

############# SECTION 3 ######################    

    html.H2('Cluster Analysis', className='box box_title',style={'font-size': '40px',}),
    html.Div([
        html.Div([
            html.Div([
                html.H3(['Cluster Sales by Quarter']),
            ]),
            dcc.Loading(
                id='loading_cluster_sales_scatter',
                children=[dcc.Graph(id='cluster_sales_scatter',figure=cluster_sales_scatter())],
                type='circle'
            ),
        ], style={'width': '50%'}, className='box box_graph'),
        html.Div([
            html.Div([
                html.H3(['Top 10 Products by Cluster']),
            ]),
            dcc.Loading(
                id='loading_cluster_bar_prods',
                children=[dcc.Graph(id='cluster_bar_prods',figure=cluster_bar_prods())],
                type='circle'
            ),
        ], style={'width': '50%'}, className='box box_graph'),
    ], className='row'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H2(['Cluster Sales by Quarter']),
                    cluster_input,
                ], style={'text-align': 'center'}),
            ]),
            dcc.Loading(
                id='loading_cluster_treemap',
                children=[dcc.Graph(id='cluster_treemap')],
                type='circle'
            ),
        ], style={'width': '100%'}, className='box box_graph'),
    ],className='row'),

])


##################################################### Callbacks ########################################################

#/W BAR CHART
@app.callback(
    [
        Output("best_worst_bar_chart", "figure"),
    ],
    [
        Input("quarter_input", "value"),
    ]
)

def bw_bar_chart(quarter):
    if quarter == 'total':
        df_plot = df.copy()
    else:
        df_plot = df[df['Quarter']==quarter]
    best_selling_stores = df_plot.groupby(by=["Point-of-Sale_ID"])["Value_price"].sum().sort_values(ascending=False)
    
    best_sellers = best_selling_stores.head(5)
    worst_sellers = best_selling_stores.tail(5)

    b_w_bar = go.Figure()
    b_w_bar.add_trace(go.Bar(
        x=best_sellers.index.map(str),
        y=best_sellers.values,
        name=f'Top 5 best performing stores',
        marker_color='#4EC8CA'
    ))
    b_w_bar.add_trace(go.Bar(
        x=worst_sellers.index,
        y=worst_sellers.values,
        name=f'Top 5 worst performing stores',
        marker_color='#a8a8a8'
    ))

    b_w_bar.update_layout(
        barmode='stack', 
        xaxis_tickangle=-45,
        xaxis={'categoryorder':'total descending'},
        title={'text':f"Best/Worst performing stores in {quarter}",'x':0.5},
        font= {'color': 'white','size':15},
        plot_bgcolor = '#343434',
        paper_bgcolor = '#343434',
    )
    best_worst_bar_chart = b_w_bar
    
    
    return best_worst_bar_chart,\

# SUNBURST
@app.callback(
    [
        Output("sunburst", "figure"),
    ],
    [
        Input("quarter_input", "value"),
        Input("number_stores_input", "value"),
        Input("number_categories_input", "value"),
        Input("number_products_input", "value"),
    ]
)

def sunburst(quarter,store_number,category_number,products_number):
    #sunburst
    if quarter == 'total':
        df_plot_temp = df.copy()
    else:
        df_plot_temp = df[df['Quarter']==quarter]
    best_selling_stores = df_plot_temp.groupby(by=["Point-of-Sale_ID"])["Value_price"].sum().sort_values(ascending=False).head(store_number)
    df_plot = df_plot_temp[df_plot_temp['Point-of-Sale_ID'].isin(best_selling_stores.index)]
    df_plot = df_plot[['Point-of-Sale_ID','ProductCategory_ID','ProductName_ID','Value_price']]

    plot_final_df = pd.DataFrame(columns=['Point-of-Sale_ID','ProductCategory_ID','ProductName_ID','Value_price'])
    for store in best_selling_stores.index:
        temp = df_plot[df_plot['Point-of-Sale_ID']==store]
        temp_best_categ = temp.groupby(by=["ProductCategory_ID"])["Value_price"].sum().sort_values(ascending=False).head(category_number)

        temp = temp[temp['ProductCategory_ID'].isin(temp_best_categ.index)]
        for categ in temp_best_categ.index:
            temp_categ = temp[temp['ProductCategory_ID']==categ]
            temp_categ_product = temp_categ.groupby(by=["ProductName_ID"])["Value_price"].sum().sort_values(ascending=False).head(products_number)
            temp_categ = temp_categ[temp_categ['ProductName_ID'].isin(temp_categ_product.index)]
            frames = [plot_final_df,temp_categ]
            plot_final_df = pd.concat(frames)

    sunburst = px.sunburst(plot_final_df,
                            path=['Point-of-Sale_ID', 'ProductCategory_ID','ProductName_ID'],
                            values='Value_price',
                            title = f'Top {products_number} products, of the Top {category_number} categories, of the Top {store_number} stores'
    )
    sunburst.update_layout(
        font= {'color': 'white','size':15},
        plot_bgcolor = '#343434',
        paper_bgcolor = '#343434',
    )
    return sunburst,\

# Quarter Scatter Bar
@app.callback(
    [
        Output("quarter_scatter_bar", "figure"),
    ],
    [
        Input("store_input", "value"),
    ]
)

def quarter_scatter_bar(store):

    df_plot = df[df['Point-of-Sale_ID']==store]
    df_plot_value = df_plot.groupby('Quarter')['Value_price'].sum()
    df_plot_units = df_plot.groupby('Quarter')['Value_units'].sum()
    
    plot_data = []
    
    comp_bar = dict(type='bar',
                    x=df_plot_units.index,
                    y=df_plot_units.values,
                    yaxis='y1',
                    name='Units sold',
                    marker = dict(color= '#4EC8CA'),
                   )

    comp_cum = dict(type='scatter',
                        x=df_plot_value.index,
                        y=df_plot_value.values,
                        yaxis='y2',
                        name='Value',
                        marker = dict(color= '#F0842D')
                       )
    
    plot_data.append(comp_bar)
    plot_data.append(comp_cum)

    _layout =dict(title=dict(text=f'Quarterly sales of Store nº {store} '),
                  yaxis=dict(color='#4EC8CA'),
                  yaxis2=dict(overlaying='y', side='right',color='#F0842D'))

    scatter_bar = go.Figure(data=plot_data, layout=_layout)
    scatter_bar.update_xaxes(tickangle = 310)
    scatter_bar.update_layout(
        font= {'color': 'white','size':15},
        plot_bgcolor = '#343434',
        paper_bgcolor = '#343434',
    )
    return scatter_bar, \

# Market share pie
@app.callback(
    [
        Output("market_share_pie", "figure"),
    ],
    [
        Input("quarter_input", "value"),
        Input("store_input", "value"),
        Input("type_analysis_input", "value"),

    ]
)
def market_share_pie(quarter, store,msh_type):
    if quarter =='total':
        df_plot = df[df['Point-of-Sale_ID']==store]    
    else:
        df_plot = df[df['Point-of-Sale_ID']==store]
        df_plot = df_plot[df_plot['Quarter']==quarter]


    if msh_type == 'units':
        df_plot_fam_mktsh = (df_plot.groupby(by=["ProductFamily_ID"])['Value_units'].sum()/df_plot['Value_units'].sum()*100).sort_values(ascending=False)
        df_plot_categ_mktsh = (df_plot.groupby(by=["ProductCategory_ID"])['Value_units'].sum()/df_plot['Value_units'].sum()*100).sort_values(ascending=False)
    else:
        df_plot_fam_mktsh = (df_plot.groupby(by=["ProductFamily_ID"])['Value_price'].sum()/df_plot['Value_price'].sum()*100).sort_values(ascending=False)
        df_plot_categ_mktsh = (df_plot.groupby(by=["ProductCategory_ID"])['Value_price'].sum()/df_plot['Value_price'].sum()*100).sort_values(ascending=False)

    # Create subplots: use 'domain' type for Pie subplot
    market_share_pie = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

    market_share_pie.add_trace(go.Pie(labels=df_plot_fam_mktsh.index, values=df_plot_fam_mktsh.values, name="Family"),
                  1, 1)
    market_share_pie.add_trace(go.Pie(labels=df_plot_categ_mktsh.index, values=df_plot_categ_mktsh.values, name="Category"),
                  1, 2)

    # Use `hole` to create a donut-like pie chart
    market_share_pie.update_traces(hole=.4,textposition='inside', textinfo='percent+label')

    market_share_pie.update_layout(
        title_text=f"Market Share by {msh_type}",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='Family', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='Category', x=0.82, y=0.5, font_size=20, showarrow=False)],
        showlegend=False,
        font= {'color': 'white','size':15},
        plot_bgcolor = '#343434',
        paper_bgcolor = '#343434',
    )
    return market_share_pie, \

# Association rules table
@app.callback(
    [
        Output("asssociation_table", "figure"),
    ],
    [
        Input("type_association_input", "value"),
        Input("aggregated_quarter_input", "value"),
    ]
)
def association_table(association_type, quarter):
    if association_type == 'Complementary':
        complementary_quarter= complementary[complementary['quarter']==quarter]
        df_plot = complementary_quarter[['antecedents','consequents','antecedent support','consequent support','support','confidence','lift']]
    else:
        substitutes_quarter= substitutes[substitutes['quarter']==quarter]
        
        df_plot = substitutes_quarter[['antecedents','consequents','antecedent support','consequent support','support','confidence','lift']]
        
    association_table = go.Figure(data=[go.Table(
        header=dict(values=list(df_plot.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df_plot.antecedents, 
                           df_plot.consequents, 
                           df_plot['antecedent support'].round(4), 
                           df_plot['consequent support'].round(4),
                           df_plot.support.round(4),
                           df_plot.confidence.round(4),
                           df_plot.lift.round(4)],
                   fill=dict(color=['rgb(204,235,197)', 'rgb(179,226,205)','white']),
                   align='left'))
    ])
    association_table.update_layout(
        title = {'text':f"{association_type} products table, for Q{quarter}",'x':0.5,'font':{'color':'white'}},
        plot_bgcolor = '#343434',
        paper_bgcolor = '#343434',
    )
    return association_table, \

@app.callback(
    [
        Output("cluster_treemap", "figure"),
    ],
    [
        Input("cluster_input", "value"),
    ]
)
def cluster_treemap(cluster):    
    df_plot = df[df['clusters']==cluster]
    df_plot = df_plot[['ProductFamily_ID','ProductBrand_ID','ProductName_ID','Value_units']]
    
    plot_final_df = pd.DataFrame(columns=['ProductFamily_ID','ProductBrand_ID','ProductName_ID','Value_units'])
    for family in df_plot.ProductFamily_ID.unique():
        temp_df_fam = df_plot[df_plot['ProductFamily_ID']==family]
        temp_best_brands = temp_df_fam.groupby(by=["ProductBrand_ID"])["Value_units"].sum().sort_values(ascending=False).head(3)
        temp = df_plot[df_plot['ProductBrand_ID'].isin(temp_best_brands.index)]
        
        for brand in temp_best_brands.index:
            temp_brand = temp[temp['ProductBrand_ID']==brand]
            temp_name_product = temp_brand.groupby(by=["ProductName_ID"])["Value_units"].sum().sort_values(ascending=False).head(5)
            temp_brand = temp_brand[temp_brand['ProductName_ID'].isin(temp_name_product.index)]
            frames = [plot_final_df,temp_brand]
            plot_final_df = pd.concat(frames)

    
    plot_final_df["family"] = "family" # in order to have a single root node
    cluster_treemap = px.treemap(plot_final_df, path=['family','ProductFamily_ID', 'ProductBrand_ID', 'ProductName_ID'], values='Value_units',title=f'Family treemap of Cluster {cluster}')
    cluster_treemap.data[0].textinfo = 'label+text+value+percent parent'
    cluster_treemap.update_layout(
        font= {'color': 'white','size':15},
        plot_bgcolor = '#343434',
        paper_bgcolor = '#343434',
    )
    return cluster_treemap, \

################################################## END APP ###################################################################

if __name__ == '__main__':
    app.run_server(port='8050',debug=True, use_reloader=False)
