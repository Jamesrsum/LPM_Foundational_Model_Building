import requests
import pandas as pd

api_key = '634b38671f85616051e350e177ae83c4e5ac7ff6'
base_url = 'https://api.census.gov/data/2022/acs/acs5'

variables = {
    'B01003_001E': 'Total Population',
    'B01002_002E': 'Median Age by Sex (Male)',
    'B01002_003E': 'Median Age by Sex (Female)',
    'B02001_002E': 'White',
    'B02001_003E': 'Black or African American',
    'B02001_004E': 'American Indian and Alaska Native',
    'B02001_005E': 'Asian',
    'B02001_006E': 'Native Hawaiian and Other Pacific Islander',
    'B02001_007E': 'Some Other Race',
    'B02001_008E': 'Two or More Races',
    'B03001_003E': 'Hispanic or Latino',
    'B11001_001E': 'Total Households',
    'B11001_002E': 'Family Households',
    'B11001_003E': 'Married-couple Households',
    'B15003_001E': 'Educational Attainment for Population 25 and Over',
    'B15003_017E': 'High School Graduate',
    'B15003_022E': 'Bachelor\'s Degree',
    'B15003_025E': 'Graduate or Professional Degree',
    'B17001_002E': 'Population Below Poverty Level',
    'B19013_001E': 'Median Household Income',
    'B19001_001E': 'Household Income in the Past 12 Months',
    'B19301_001E': 'Per Capita Income',
    'B23025_003E': 'Labor Force Participation Rate',
    'B23025_004E': 'Employed Individuals in Labor Force',
    'B23025_005E': 'Unemployed Individuals in Labor Force',
    'B25001_001E': 'Total Housing Units',
    'B25002_002E': 'Occupied Housing Units', 
    'B25002_003E': 'Vacant Housing Units',
    'B25003_001E': 'Tenured Housing Units',
    'B25003_002E': 'Owner Occupied',
    'B25003_003E': 'Renter Occupied',
    'B25064_001E': 'Median Gross Rent (Dollars)',
    'B25077_001E': 'Median Value of Owner-Occupied Housing Units', # Check this
    # Additional variables from here
    'B23025_004E': 'Employed Individuals in Civilian Labor Force',
    'B23025_005E': 'Unemployed Individuals in Civilian Labor Force',
    'B23025_006E': 'Individuals in Armed Forces',
    'B23025_007E': 'Not in Labor Force',
    'C24010_001E': 'Civilian Employed Population', # how is this different from Civilian Labor Force Population
    'C24060_002E': 'Civilians working in management, business, science, and arts occupations',
    'C24060_003E': 'Civilians working in service occupations',
    'C24060_004E': 'Civilians working in sales and office occupations',
    'C24060_005E': 'Civilians working in natural resources, construction, and maintenance occupations',
    'C24060_006E': 'Civilians working in production, transportation, and material moving occupations',
    'C24050_002E': 'Civilians employed in the agriculture, forestry, fishing and hunting, and mining industry',
    'C24050_003E': 'Civilians employed in construction',
    'C24050_004E': 'Civilians employed in manufacturing',
    'C24050_005E': 'Civilians employed in the wholesale trade',
    'C24050_006E': 'Civilians employed in the retail trade',
    'C24050_007E': 'Civilians employed in transportation and warehousing, and utilities',
    'C24050_008E': 'Civilians employed in the information industry',
    'C24050_009E': 'Civilians employed in finance and insurance, and real estate, and rental and leasing',
    'C24050_010E': 'Civilians employed in professional, scientific, and management, and administrative, and waste management services',
    'C24050_011E': 'Civilians employed in educational services, and health care and social assistance',
    'C24050_012E': 'Civilians employed in arts, entertainment, and recreation, and accommodation and food services',
    'C24050_013E': 'Civilians employed in other services, except public administration',
    'C24050_014E': 'Civilians employed in public administration',
    'B19055_002E': 'Households with social security income',
    'B19055_003E': 'Households without social security income',
    'B19059_002E': 'Households with retirement income',
    'B19059_003E': 'Households without retirement income',
    # Income data is organized by race and may be added at a later stage
}

# Fetch data for each variable in dictionary above
def fetch_data(variable, api_key):
    params = {
        'get': f'NAME,{variable}',
        'for': 'zip code tabulation area:*',
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        headers = data[0]
        rows = data[1:]
        df = pd.DataFrame(rows, columns=headers)
        df = df.rename(columns={variable: variables[variable]})
        return df
    else:
        raise Exception(f"Error fetching data: {response.status_code}")

# Fetch data and merge into single dataframe
dfs = []
for var in variables:
    df = fetch_data(var, api_key)
    if dfs:
        dfs[0] = pd.merge(dfs[0], df, on=['zip code tabulation area', 'NAME'])
    else:
        dfs.append(df)

final_df = dfs[0]

if 'zip code tabulation area' in final_df.columns:
    final_df = final_df.drop(columns=['zip code tabulation area'])

# Save to CSV file
final_df.to_csv('socioeconomic_data_by_zcta.csv', index=False)

print("Data saved to socioeconomic_data_by_zcta.csv")