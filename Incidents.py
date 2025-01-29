import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


incidents = pd.read_csv("C:\VS Code\LA_Fires\mapdataall.csv")

#southern cali counties
socal_counties = np.array([
    "Los Angeles","San Diego","Orange",
    "Riverside","San Bernardino","Ventura",
    "Santa Barbara","San Luis Obispo","Imperial",
    "Kern","Mono"
])

#standardize and replace counties
std_counties = incidents['incident_county'].str.strip().str.lower()
incidents['std_incident_county'] = std_counties
incidents.drop(columns=['incident_county'])
socal_counties = [county.strip().lower() for county in socal_counties]

#query incident df --> socal_incident df
#NIFC says a wildfire is atleast 100 acres

def is_socal(county):
    return county in socal_counties
def acres100(size):
    return size>=100
    
socal_incidents = incidents[incidents['std_incident_county'].apply(is_socal)]
socal_incidents = socal_incidents[socal_incidents['incident_acres_burned'].apply(acres100)]

socal_incidents = socal_incidents.drop(columns = ['incident_is_final', 'incident_date_last_update', 'incident_administrative_unit',
       'incident_administrative_unit_url',
       'incident_location', 'incident_containment',
       'incident_control', 'incident_cooperating_agencies', 'incident_type',
       'incident_url', 'incident_dateonly_extinguished', 'incident_dateonly_created',
       'is_active', 'calfire_incident', 'notification_desired',
       'std_incident_county'])

#organize by dates
def return_year(date):
    return date[:4]
def year_month(date):
    return date[:7].replace('-','_')

date_created = np.sort(socal_incidents['incident_date_created'].apply(year_month))

def correct_years(date):
    year = int(date[:4])
    if (year>=2014)and(year<2025):
        return True
    else:
        return False

socal_incidents = socal_incidents.drop(columns='incident_date_created')
socal_incidents['date_created'] = date_created
socal_incidents = socal_incidents[socal_incidents['date_created'].apply(correct_years)].set_index('incident_id')

#plotting
socal_incidents['year'] = socal_incidents['date_created'].str[:4]
filtered_years = socal_incidents['year'].value_counts().sort_index()

ax = filtered_years.plot(kind='bar', color='grey', title='Wildfires Per Year')
plt.xticks(rotation=0)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Number of Fires', fontsize=12)
plt.title('Wildfires Per Year', fontsize=20, fontweight='bold')
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.plot(filtered_years.index, filtered_years.values, color='red', marker='o', linestyle='--', label='Trend Line')

# plt.legend()
# plt.show()

print(socal_incidents)
