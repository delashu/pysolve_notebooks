import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
#set wide format
st.set_page_config(layout="wide")
#read in table 12
rec_year =  pd.read_excel("https://ncses.nsf.gov/pubs/nsf19301/assets/data/tables/sed17-sr-tab012.xlsx", 
                   skiprows = range(0,4),
                   names =["field","number_1987", "percent_1987", "number_1992", "percent_1992",
                           "number_1997", "percent_1997",
                          "number_2002", "percent_2002","number_2007", "percent_2007",
                          "number_2012", "percent_2012","number_2017", "percent_2017"])
rec_year_1 = rec_year[["field","number_1987", "number_1992", "number_1997",
                          "number_2002", "number_2007","number_2012","number_2017"]]
#rename columns
rec_year_1 = rec_year_1.rename(columns = {"number_1987": "1987", "number_1992":"1992", "number_1997":"1997",
                          "number_2002":"2002", "number_2007":"2007","number_2012":"2012","number_2017":"2017"})
st.title(":mortar_board:  **The PhD Dashboard**  :book: ")
st.markdown(str("**Visualize and analyze PhD numbers and post-graduation plans**"))
st.markdown(str("Select a Specific Area of study to analyze using the first click-down menu on the left. Longitudinal plots, tables, and summaries of number of doctorates awarded from 1987 - 2017 are shown. Blue points and lines on the longitudinal plot are the true number of doctorates awarded from 1987 to 2017. The red line is the OLS best fit line."))

#data for general area of study: table 55
posg =  pd.read_excel("https://ncses.nsf.gov/pubs/nsf19301/assets/data/tables/sed17-sr-tab055.xlsx", 
                     skiprows = range(0,3), 
                     names = ['Characteristic', 'All fields', 'Life sciences',
       'Physical sciences and earth sciences',
       'Mathematics and computer sciences', 'Psychology and social sciences',
       'Engineering', 'Education', 'Humanities and arts', 'Other'])
#post grad data prep
pos_stat = posg.loc[2:5, :]
pos_stat = pos_stat.assign(Characteristic = ["PostGrad Study","Employment","Seeking","Other"])
#location data prep
usd = posg.loc[31:39, :]
#activity data prep
pact  = posg.loc[16:20, :]

#interactive elements: 
major_study = st.sidebar.selectbox("Specific Area of Study", rec_year_1['field'].tolist())
general_study = st.sidebar.selectbox("General Area of Study", pos_stat.columns[1:].tolist())

#prepare the data for line graphs
rec_year_2 = rec_year_1.melt(id_vars = ['field'], 
        value_vars = ["1987", "1992", "1997","2002", "2007","2012","2017"],
         value_name='Doctorates Awarded', var_name = 'Year')
rec_year_2["Year"] = pd.to_numeric(rec_year_2["Year"])
lineplot_df = rec_year_2.loc[rec_year_2['field'] == major_study].drop(['field'], axis=1).reset_index(drop = True)

fig_line = px.line(lineplot_df, x='Year', y='Doctorates Awarded', 
                title= str("Longitudinal Look at Doctorates Awarded: ")+str(major_study), markers = True)

fig_line.update_xaxes(
    tickvals=["1987", "1992", "1997","2002", "2007","2012","2017"],
)
# fit the regression
regr = sm.OLS(lineplot_df['Doctorates Awarded'],sm.add_constant(lineplot_df['Year']))

# regression extract
lineplot_df['bestfit'] = regr.fit().fittedvalues
# plotly figure setup
fig_line.add_trace(go.Scatter(name='Regression Line', 
                              x=lineplot_df['Year'], 
                              y=lineplot_df['bestfit'], 
                              mode='lines',
                             opacity = 0.4))
suma_dat = pd.DataFrame({'Mean' : [lineplot_df['Doctorates Awarded'].mean().round(2)], 
             'Median': [lineplot_df['Doctorates Awarded'].median()],
             'Max': [lineplot_df['Doctorates Awarded'].max()],
             'Min': [lineplot_df['Doctorates Awarded'].min()],
             'Range' : [lineplot_df['Doctorates Awarded'].max() - lineplot_df['Doctorates Awarded'].min()], 
             'Regression Intercept': regr.fit().params[0],
             'Regression Slope': regr.fit().params[1]})

#output into column features in streamlit
col1, col2 = st.columns((2, 1))
col1.plotly_chart(fig_line)
col2.subheader("Raw Data")
col2.dataframe(lineplot_df.assign(hack='').set_index('hack'))
st.markdown(str("Summary Statistics: ")+str(major_study))
st.dataframe(suma_dat.assign(hack='').set_index('hack'))
#create px bar figure
barfig = px.bar(pos_stat, x = "Characteristic", y = general_study, text = general_study,
        labels={
                "Characteristic": "Post Graduation Plans"
                        },
    title=str("Post Grad Plans: ")+str(general_study)+ str(" by Number"))
barfig.update_layout(xaxis_tickangle=-45)

barfigloc = px.bar(usd, x="Characteristic", y=general_study,  
        text=general_study,
        labels={
                "Characteristic": "USA Location"
                        },
    title=str("Post Grad Locations: ")+str(general_study) + str(" by Percentage"))
barfigloc.update_layout(xaxis_tickangle=-45)
#add space inbetween portions of dashboard
st.markdown(str("  ")) #add blank space
st.markdown(str("  ")) #add blank space
st.markdown(str("  ")) #add blank space
#create subheader
st.subheader(str("** :dollar: Post Graduate Plans & Landing Locations :runner: 2017 Data**"))
#create description
st.markdown(str("Select a General Area of study to analyze using the second click-down menu on the left. Two barplots are rendered based on your input that shows post-graduate plans and landing locations for the year of 2017."))
col3, col4 = st.columns((1, 1))
col3.plotly_chart(barfig)
col4.plotly_chart(barfigloc)
#include descriptions
col3.caption(str("The left barplot quantifies the number of each field's graduate plans as 'PostGrad Study', 'Employment', 'Seeking', or  'Other'.")) #add blank space
col4.caption(str("The right barplot quantifies the landing locations of PhD graduates who will remain in the US as a percentage."))
st.markdown(str("**Among those graduates who chose employment, the below table shows the percentage breakdown of Primary Activity of Employment.**"))
pact  = posg.loc[16:20, :]
pact = pact[['Characteristic',general_study]]
newpact = pact.T
new_header = newpact.iloc[0] #grab the first row for the header
dfpac = newpact[1:] #take the data less the header row
dfpac.columns = new_header #set the header row as the df header
st.dataframe(dfpac.assign(hack='').set_index('hack'))
