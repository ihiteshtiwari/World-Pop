import streamlit as st
import pandas as pd
import plotly.express as px


def load_custom_css():
    with open("styles.css", "r") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide")
    load_custom_css()

    # Your Streamlit app content with different options
    # ...

if __name__ == "__main__":
    main()


 
# Load the data and perform necessary transformations
data = pd.read_csv(r'world_population.csv')

# Renaming Columns and other data processing...

# Grouping data for visualization
population = data.groupby(['ORIGEN', 'CCA3']).agg({
    '2022': 'sum', '2020': 'sum', '2015': 'sum', '2010': 'sum',
    '2000': 'sum', '1990': 'sum', '1980': 'sum', '1970': 'sum'
}).stack().reset_index()
population.columns = ['ORIGEN', 'CCA3', 'Year', 'Population']

# Define 'con_pop' globally
con_pop = population.groupby(['ORIGEN', 'Year']).Population.sum().reset_index()

# Your Streamlit app structure

option = st.sidebar.selectbox("Select an option", ("Home", "Choropleth Map", "Bar Chart", "Pie Chart", "Top 10 by Area", "Top 10 Growth Rate", "Population Predication", "Top 10 Population & Growth Rate"))



if option == "Home":
    
    
    
    # Read the contents of the HTML file
    try:
        with open('index.html', 'r') as file:
            html_content = file.read()

        # Wrap HTML content in a div with height set to 100%
        html_with_height = f'<div style="height:100%;">{html_content}</div>'

        # Display the content of the HTML file with adjusted height
        st.components.v1.html(html_with_height, width=1450, height=1500)
        st.write("", data)
        st.write("ref:https://www.kaggle.com/datasets/iamsouravbanerjee/world-population-dataset/data")
    except FileNotFoundError:
        st.write("HTML file not found. Check the file path.")
    except Exception as e:
        st.write("An error occurred:", e)
        

elif option == "Choropleth Map":
    # Code for Choropleth Map
    pop_gr = population.sort_values(by='Year', ascending=True)
    fig = px.choropleth(pop_gr, locations="CCA3", color="Population",
                        hover_name='ORIGEN', animation_frame="Year",
                        animation_group="CCA3", color_continuous_scale="Viridis_r")
    st.plotly_chart(fig)
    # Additional details or content related to the Choropleth Map option
    # ...
elif option == "Bar Chart":
    # Code for Bar Chart
    fig = px.bar(con_pop, x="ORIGEN", y="Population", color="ORIGEN",
                 animation_frame="Year", animation_group="ORIGEN",
                 range_y=[0, 2000000000], range_x=[0, 236])
    st.plotly_chart(fig)
    # Additional details or content related to the Bar Chart option
    # ...
elif option == "Pie Chart":
    # Code for Pie Chart
    fig = px.pie(con_pop, names="ORIGEN", values="Population",
                 title="Population Distribution by Country/Territory")
    fig.update_traces(textinfo="none")
    st.plotly_chart(fig)
    # Additional details or content related to the Pie Chart option
    # ...
# Other options and their respective codes...


elif option == "Top 10 by Area":
    data_sorted = data.sort_values(by='Area (km²)', ascending=False)
    top_10 = data_sorted.head(10)
    fig = px.choropleth(top_10, locations='CCA3', color='Area (km²)',
                        hover_name='ORIGEN', title='Top 10 Countries by Area',
                        color_continuous_scale="Viridis_r")
    st.plotly_chart(fig)
    # Additional details or content related to the Top 10 by Area option
    st.write("Top 10 by Area Code Goes Here")
    # ...

elif option == "Top 10 Growth Rate":
    top_10_growth = data.sort_values(by='Growth Rate', ascending=False).head(10)
    fig = px.line(top_10_growth, x='ORIGEN', y='Growth Rate',
                  labels={'ORIGEN': 'Country'},
                  title='Top 10 Countries with the Highest Growth Rate',
                  markers=True)
    fig.update_traces(line=dict(color="blue"))
    st.plotly_chart(fig)
    # Additional details or content related to the Top 10 Growth Rate option
    st.write("Top 10 Growth Rate Code Goes Here")
    # ...

elif option == "Predict Population":
    # Select the features and target variable
    X = data[['1970', '1980', '1990', '2000', '2010', '2015', '2020', '2022']]
    y = data['WP%']

    # Train the regression model
    regression_model = LinearRegression()
    regression_model.fit(X, y)

    # Get the year input from the user
    input_year = st.number_input("Enter a year:", min_value=1970, max_value=2022, step=1)

    # Create a DataFrame with the input year for prediction
    input_data = pd.DataFrame([[input_year, input_year, input_year, input_year, input_year, input_year, input_year, input_year]], columns=X.columns)

    # Predict the population percentage for the input year
    predicted_population_percentage = regression_model.predict(input_data)

    # Display the predicted population percentage for the input year
 

elif option == "Population Predication":
    # Calculate the population growth rate for each year
    data['Population_Growth_Rate'] = (data['2022'] - data['1970']) / data['1970']

    # Calculate the average population growth rate
    average_population_growth_rate = data['Population_Growth_Rate'].mean()

    # Get the future year input from the user
    future = st.number_input("Enter a year:", min_value=1970, max_value=2100, step=1)

    try:
        if future < 2023:
            # Sum the values in the column corresponding to the entered year
            col_sum = data[str(future)].sum() / 1e9  # Convert to billions
            st.write(f"World-wide Population in {future}:", col_sum, "billion")

            # Prepare data for line chart (assuming year columns are from '1970' to '2022')
            years = ['1970', '1980', '1990', '2000', '2010', '2015', '2020', '2022', str(future)]
            population_data = data[years].loc[0] / 1e9  # Selecting the population data from the first row and converting to billions

            # Create a line chart
            st.line_chart(population_data)
        else:
            future_data = future - 2022

            # Calculate the sum of values in the '2022' column
            sum_2022 = data['2022'].sum()

            # Calculate the projected future population
            future_pop = sum_2022 * (1 + (average_population_growth_rate / 100)) ** future_data / 1e9  # Convert to billions
            
            # Display the projected future population
            st.write(f"World-wide Population in {future} will be:", round(future_pop, 2), "billion")

            # Prepare data for line chart (assuming year columns are from '1970' to '2022')
            years = ['1970', '1980', '1990', '2000', '2010', '2015', '2020', '2022', str(round(future_pop))]
            population_data = data[years].loc[0] / 1e9  # Selecting the population data from the first row and converting to billions

            # Create a line chart including future projection
            st.line_chart(population_data)

            # Create data for the future year and add to the line chart
            future_years = ['2022', str(round(future_pop))]
            future_population_data = data[future_years].iloc[0] / 1e9  # Selecting the population data for future years and converting to billions
            st.line_chart(future_population_data)
    except KeyError:
        st.markdown("<p style='color:red;'>Data not found for the entered year. Please enter one of these years: 1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022 OR FUTURE YEAR. </p>", unsafe_allow_html=True)


elif option == "Top 10 Population & Growth Rate":
    st.subheader('Top 10 Countries by Population and Growth Rate')
    top_10_population = data.nlargest(10, 'World Population Percentage')
    top_10_growth_rate = data.nlargest(10, 'Growth Rate')

    st.write("Top 10 Countries by Population:")
    st.table(top_10_population[['ORIGEN', 'World Population Percentage']])

    st.write("Top 10 Countries by Growth Rate:")
    st.table(top_10_growth_rate[['ORIGEN', 'Growth Rate']])

