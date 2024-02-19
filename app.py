
import os 
from scipy.stats import norm
import numpy as np 
import pandas as pd
import cssutils
import requests
from dash import Dash, html, dash_table, dcc, Input, Output, no_update, callback
import plotly.express as px
import plotly.graph_objs as go

# os.getcwd()
# os.chdir('C:/Users/thomj/OneDrive - Baylor College of Medicine/Cholankeril/multistate/dash')
# os.getcwd()
#os.listdir('C:/Users/thomj/OneDrive - Baylor College of Medicine/Cholankeril/multistate/dash/data')
#mpreds = pd.read_csv('C:/Users/thomj/OneDrive - Baylor College of Medicine/Cholankeril/multistate/dash/data/stacked_multistate_model_risk_probabilities.csv', low_memory=False)
#mpreds.to_pickle('C:/Users/thomj/OneDrive - Baylor College of Medicine/Cholankeril/multistate/dash/data/stacked_multistate_model_risk_probabilities.pkl')
mpreds = pd.read_pickle('./data/stacked_multistate_model_risk_probabilities.pkl')

df = mpreds.loc[:,['transition', 'etiology', 'age_at_state_start', 'month', 'prob', 'll', 'ul', 'estimate']].copy()
df['year'] = np.round(df['month']/12, 1)

#plotly express convenience for faceting requires standard error +/-; a lot more complex in plotly go, so tricking visual with recovering SEs
##add in recovered SEs for ribbons 
#norm.ppf(.975)
def se_recovery(LL, UL, CI=.95, MIN_SE = .000001):
    '''
    LL:  vector of lower limit confidence intervals,
    UL:  vector of upper limit confidence intervals,
    CI:  Confidence Interval (CI) for later use with scipy probability point function, normal quantiles
    '''
    nqval = norm.ppf(1.00 - ((1.00-CI)/2))
    #print(nqval)
    pointvec = (UL-LL)/2.00
    se = pointvec/nqval
    se = pd.Series(np.where(se<MIN_SE, MIN_SE, se))
    #print(se)
    return se

df['se'] = se_recovery(df['ll'], df['ul'])
df['se_plus_ppf'] = df['se']*np.repeat(norm.ppf(.975), len(df))
##check approx recovery of LL/UL estimates, albeit with floating point error
#df['LL'] = df['prob'] - df['se']*1.96  
#df['UL'] = df['prob'] + df['se']*1.96 

# Initialize the app
app = Dash(__name__)

app.layout = html.Div([
    html.H3("Cirrhosis Progression\nMultistate Model Risk Estimates"),
    html.P("Note: below the figure, options to print 95% Confidence Intervals and resize the figure are available to modify the figure."),

    html.Label("Select Liver Disease Progression Transition (may choose multiple):", style={'fontSize':18, 'textAlign':'left'}),
    dcc.Dropdown(
        id='tran',
        options=[{'label': s, 'value': s} for s in list(sorted(df.transition.unique()))],
        value=['CC --> Ascites'],
        placeholder='Select a Transition',
        clearable=False, 
        multi=True),

    html.Label("Cirrhosis Etiology (may choose multiple):", style={'fontSize':18, 'textAlign':'left'}),
    dcc.Dropdown(
        id='etiol', 
        options=[{'label': s, 'value': s} for s in list(sorted(df.etiology.unique()))],
        value=['Unadjusted'],
        placeholder='Selected Etiology of Cirrhosis',
        clearable=False, 
        multi=True),  
    
    html.Label("Age (may choose multiple):", style={'fontSize':18, 'textAlign':'left'}),
    dcc.Dropdown(
        id='ages',
        options=[{'label': s, 'value': s} for s in list(sorted(df.age_at_state_start.unique()))],
        value=['Unadjusted'],
        placeholder='Select an Age',
        clearable=False, 
        multi=True),
    
    dcc.Graph(id='figure', figure={}),

    html.Label("Show 95% Confidence Intervals:", style={'fontSize':18, 'textAlign':'left'}),
    dcc.RadioItems(
        id='print_ci',
        options=['Yes', 'No'],
        value='No'),
    
    html.Label("Figure Width:", style={'fontSize':18, 'textAlign':'left'}),
    dcc.Slider(id='fig_width_slider', 
               min=25, 
               max=2000, 
               step=25, 
               value=750,
               marks={x: str(x) for x in [100, 250, 500, 750, 1000, 1250, 1500, 1750, 2000]}),

    html.Label("Figure Height:", style={'fontSize':18, 'textAlign':'left'}),
    dcc.Slider(id='fig_height_slider', 
               min=25, 
               max=2000, 
               step=25, 
               value=500,
               marks={x: str(x) for x in [100, 250, 500, 750, 1000, 1250, 1500, 1750, 2000]})

    ])

#initialize starting state for whether 95% CIs should be visualized or not
plot_ci_var = 'No'

#reactive callbacks list
@callback(
        Output('figure', 'figure'),
        Input('ages', 'value'),
        Input('etiol', 'value'),
        Input('tran', 'value'),
        Input('print_ci', 'value'),
        Input('fig_width_slider', 'value'),
        Input('fig_height_slider', 'value'))
def update_graph(selected_age, selected_etiol, selected_tran, selected_ci, selected_width, selected_height):
    
    #if nothing selected, create a blank figure, since no reference points
    if (selected_age is None or len(selected_age) == 0) or (selected_etiol is None or len(selected_etiol) == 0) or (selected_tran is None or len(selected_tran) == 0):
        return {}
    else: 
        #print(f"Selected value = {selected_ci}")

        sdf = df[(df.transition.isin(selected_tran)) & 
                    (df.etiology.isin(selected_etiol)) & 
                    (df.age_at_state_start.isin(selected_age))]
        #print(sdf.head(1))
        #print(sdf.tail(1))

        if selected_ci=='Yes':
            plot_ci_var = 'se_plus_ppf'
        else:
            plot_ci_var = None
        fig = px.line(sdf, 
                        x='month', 
                        y='prob', 
                        error_y=plot_ci_var, 
                        color='age_at_state_start', 
                        facet_row='etiology', 
                        facet_col='transition',
                    # hover_name='estimate',
                        hover_data={'prob': False, 
                                    'se_plus_ppf': False,
                                    'etiology': True,
                                    'age_at_state_start': True,
                                    'transition': True,
                                    'month': False,
                                    'estimate': True},
                        labels={'month': 'Month',
                                'age_at_state_start': 'Age at State Entry', 
                                'etiology': 'Etiology', 
                                'transition': 'Transition',
                                'prob': 'Risk Probability',
                                'estimate': 'Risk Estimate'})

        #change the thickness of CI values for all facets        
        for i in range(len(fig.data)):
            #print(fig.data[i])
            fig.data[i].error_y.thickness = .5
        
        #markers and lines, not just lines
        fig.update_traces(mode="markers+lines")

        #make height and width adjustable based on user input (reactive), create relevant tick marks, and whiten background
        fig.update_layout(autosize=True,
                          width=int(selected_width),
                          height=int(selected_height), 
                          hovermode="x unified", 
                          template='plotly_white',
                          xaxis=dict(tickvals=[1, 6, 12, 18, 24, 30, 36]))
        
        fig.update_xaxes(gridcolor='lightgrey')
        
        fig.update_yaxes(gridcolor='lightgrey')

        fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))

        fig.for_each_xaxis(lambda xaxis: xaxis.update(showticklabels=True))
  
    return fig

#launch app
if __name__ == '__main__':
    app.run(debug=False) #, port=8050)
