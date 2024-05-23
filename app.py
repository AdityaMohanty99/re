import streamlit as st
import numpy as np
from math import sin, cos, radians, degrees, acos, asin, tan




import streamlit as st
from datetime import datetime
from math import sin, radians

# Constants for days per month
MONTHS = {
    "January": 31, "February": 28, "March": 31, "April": 30,
    "May": 31, "June": 30, "July": 31, "August": 31,
    "September": 30, "October": 31, "November": 30, "December": 31
}

# Function to calculate day of year
def calculate_day_of_year(month, day):
    month_days = list(MONTHS.values())
    month_keys = list(MONTHS.keys())
    index = month_keys.index(month)
    return sum(month_days[:index]) + day

# Function to calculate declination
def calculate_declination(n):
    return 23.45 * sin(radians((360 / 365) * (284 + n)))

# Streamlit interface setup
st.title("Solar Declination Calculator")

# Create two columns for inputs
col1, col2 = st.columns(2)

with col1:
    st.write("Select date:")
    selected_month = st.selectbox("Select Month", list(MONTHS.keys()), key='select_month')
    # Updating day selectbox to dynamically regenerate based on month selection with a unique key
    selected_day = st.selectbox("Select Day", range(1, MONTHS[selected_month]+1), key='select_day')

with col2:
    st.write("Or enter the day of the year:")
    # Unique key for direct day of year input
    day_of_year_input = st.number_input("Day of the year (1-365):", min_value=1, max_value=365, value=1, key='day_of_year_input')

# Checkbox to choose input method with a unique key
use_day_of_year = st.checkbox("Use day of the year input", key='use_day_of_year')

# Calculation
if use_day_of_year:
    day_of_year = day_of_year_input
else:
    day_of_year = calculate_day_of_year(selected_month, selected_day)

declination = calculate_declination(day_of_year)

# Display the result
st.write(f"The solar declination for day {day_of_year} is approximately {declination:.2f} degrees.")

















































# Function to calculate declination
def calculate_declination(day_of_year):
    return 23.45 * sin(radians((360 / 365) * (284 + day_of_year)))

# Function to calculate hour angle
def calculate_hour_angle(time, longitude_correction=0):
    return 15 * (time - 12) + longitude_correction

# Function to calculate the cosine of the angle of incidence
def calculate_cos_theta(declination, hour_angle, latitude, slope, azimuthal_angle):
    declination_rad = radians(declination)
    hour_angle_rad = radians(hour_angle)
    latitude_rad = radians(latitude)
    slope_rad = radians(slope)
    azimuthal_angle_rad = radians(azimuthal_angle)

    cos_theta = (sin(declination_rad) * sin(latitude_rad) * cos(slope_rad) -
                 sin(declination_rad) * cos(latitude_rad) * sin(slope_rad) * cos(azimuthal_angle_rad) +
                 cos(declination_rad) * cos(latitude_rad) * cos(slope_rad) * cos(hour_angle_rad) +
                 cos(declination_rad) * sin(latitude_rad) * sin(slope_rad) * cos(azimuthal_angle_rad) * cos(hour_angle_rad) -
                 cos(declination_rad) * sin(slope_rad) * sin(azimuthal_angle_rad) * sin(hour_angle_rad))

    return cos_theta

# User inputs
st.title("Solar Geometry Solver")
day_of_year = st.number_input("Enter the day of the year (1-365):", min_value=1, max_value=365, value=1)
latitude = st.number_input("Enter the latitude in degrees:", value=0.0)
time = st.number_input("Enter the time in hours (LAT):", value=12.0)
slope = st.number_input("Enter the slope of the surface (degrees):", value=0.0)
azimuthal_angle = st.number_input("Enter the azimuthal angle of the surface (degrees):", value=0.0)
longitude_correction = st.number_input("Enter the longitude correction if any (degrees):", value=0.0)

# Calculations
declination = calculate_declination(day_of_year)
hour_angle = calculate_hour_angle(time, longitude_correction)
cos_theta = calculate_cos_theta(declination, hour_angle, latitude, slope, azimuthal_angle)
angle_of_incidence = degrees(acos(cos_theta))

# Display results
st.write(f"Declination Angle: {declination:.2f} degrees")
st.write(f"Hour Angle: {hour_angle:.2f} degrees")
st.write(f"Cosine of the Angle of Incidence: {cos_theta:.2f}")
st.write(f"Angle of Incidence: {angle_of_incidence:.2f} degrees")













import streamlit as st
from math import sin, cos, radians, degrees, acos, tan

# Constants for days per month
DAY_OF_YEAR = {
    "January": 31, "February": 28, "March": 31, "April": 30,
    "May": 31, "June": 30, "July": 31, "August": 31,
    "September": 30, "October": 31, "November": 30, "December": 31
}

# Helper functions
def calculate_day_of_year(month, day):
    month_days = list(DAY_OF_YEAR.values())
    month_keys = list(DAY_OF_YEAR.keys())
    index = month_keys.index(month)
    return sum(month_days[:index]) + day

def calculate_declination(n):
    return 23.45 * sin(radians((360 / 365) * (284 + n)))

def calculate_hour_angle(declination, latitude, beta=0, orientation="Horizontal"):
    declination_rad = radians(declination)
    latitude_rad = radians(latitude)
    beta_rad = radians(beta)

    cos_H = -tan(latitude_rad) * tan(declination_rad)  # Hour angle for horizontal surface
    
    if orientation == "Inclined Surface Facing South":
        # Adjust for inclined surface
        cos_H_beta = -tan(latitude_rad - beta_rad) * tan(declination_rad)
        hour_angle_deg = min(
            degrees(acos(max(min(cos_H, 1), -1))),  # Ensure within valid range for acos
            degrees(acos(max(min(cos_H_beta, 1), -1)))
        )
    else:
        hour_angle_deg = degrees(acos(max(min(cos_H, 1), -1)))

    return hour_angle_deg



# Streamlit interface setup
st.title("HOUR ANGLE AT SUN-RISE AND SUN_SET")

# Input section
month = st.selectbox("Select Month", list(DAY_OF_YEAR.keys()))
day = st.number_input("Enter Day", min_value=1, max_value=31, value=1)
latitude = st.number_input("Enter Latitude in Degrees", value=0.0)
orientation = st.selectbox("Select Surface Orientation", ["Horizontal Plane", "Inclined Surface Facing South"])

slope = 0
if orientation == "Inclined Surface Facing South":
    slope = st.number_input("Enter Slope of the Surface in Degrees (β)", value=10.0)

# Calculation
day_of_year = calculate_day_of_year(month, day)
declination = calculate_declination(day_of_year)
hour_angle_sunrise_sunset = calculate_hour_angle(declination, latitude, slope, orientation)

# Display Results
st.write(f"Day of the Year: {day_of_year}")
st.write(f"Declination: {declination:.2f} degrees")
st.write(f"Hour Angle at Sunrise/Sunset: ±{hour_angle_sunrise_sunset:.2f} degrees")






import streamlit as st
from datetime import datetime, timedelta

def calculate_lat(ist_time, local_longitude, standard_longitude, equation_of_time):
    try:
        # Convert IST string to datetime object
        ist_datetime = datetime.strptime(ist_time, '%H.%M')
    except ValueError:
        return "Invalid time format. Please use HH.MM (e.g., 14.30 for 2:30 PM)"
    
    # Calculate the time adjustment due to longitude difference
    longitude_correction = (standard_longitude - local_longitude) * 4  # in minutes
    # Adjust IST using the equation of time and the longitude correction
    # Since we're subtracting minutes, we need to add a negative sign here
    time_correction = timedelta(minutes=-longitude_correction + equation_of_time)
    # Calculate LAT by applying the time correction
    lat_datetime = ist_datetime + time_correction
    return lat_datetime.strftime('%H:%M')

# Set up the Streamlit interface
st.title('Local Apparent Time (LAT) Calculator')

# User inputs
ist_time = st.text_input('Enter IST (e.g., 14.30 for 2:30 PM):', '14.30')
local_longitude = st.number_input('Enter Local Longitude (e.g., 72.85 for Mumbai):', value=72.85)
standard_longitude = st.number_input('Enter Standard Longitude for IST (e.g., 82.5):', value=82.5)
equation_of_time = st.number_input('Enter Equation of Time on the selected day (in minutes, e.g., -3.5):', value=-3.5)

# Button to perform calculation
if st.button('Calculate LAT'):
    lat = calculate_lat(ist_time, local_longitude, standard_longitude, equation_of_time)
    st.write(f'The Local Apparent Time (LAT) is: {lat}')




































import streamlit as st
import numpy_financial as npf

def calculate_replacement_cost(replacement_cost, interest_rate, years):
    interest_rate /= 100  # Convert percentage to decimal
    return replacement_cost / ((1 + interest_rate) ** years)

def calculate_maintenance_cost(maintenance_cost, interest_rate, years):
    interest_rate /= 100  # Convert percentage to decimal
    return maintenance_cost * (1 / interest_rate) * (1 - (1 / (1 + interest_rate) ** years))

def calculate_ALCC(LCC, interest_rate, years):
    interest_rate /= 100  # Convert percentage to decimal
    if interest_rate == 0:
        return LCC / years
    else:
        return LCC / ((1 / interest_rate) * (1 - (1 / (1 + interest_rate) ** years)))

def main():
    st.title('Energy System Cost Calculations')
    if 'total_LCC' not in st.session_state:
        st.session_state.total_LCC = 0

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.header("Capital Cost")
        number_of_elements = st.number_input('Number of Elements', min_value=1, value=1, step=1)
        total_capital_cost = sum(
            st.number_input(f'Price of Element {i+1}', value=0.0) * st.number_input(f'Quantity of Element {i+1}', value=0.0)
            for i in range(number_of_elements)
        )
        st.write("Total Capital Cost: ", total_capital_cost)

    with col2:
        st.header("Replacement Cost")
        number_of_replacements = st.number_input('Number of Replacement Items', min_value=1, value=1, step=1, key='num_replacements2')
        total_replacement_cost = sum(
            calculate_replacement_cost(
                st.number_input(f'Replacement Cost for Item {j+1}', value=0.0, key=f'replace_cost{j}'),
                st.number_input(f'Interest Rate for Item {j+1} (%)', value=5.0, key=f'interest{j}'),
                st.number_input(f'Years for Item {j+1}', value=5.0, key=f'years{j}')
            )
            for j in range(number_of_replacements)
        )
        st.write("Total Replacement Cost (Present Worth): ", total_replacement_cost)

    with col3:
        st.header("Maintenance Cost")
        number_of_maintenance_items = st.number_input('Number of Maintenance Items', min_value=1, value=1, step=1, key='num_maintenance3')
        total_maintenance_cost = sum(
            calculate_maintenance_cost(
                st.number_input(f'Annual Maintenance Cost for Item {k+1}', value=0.0, key=f'maint_cost{k}'),
                st.number_input(f'Interest Rate for Maintenance Item {k+1} (%)', value=5.0, key=f'maint_interest{k}'),
                st.number_input(f'Years for Maintenance Item {k+1}', value=5.0, key=f'maint_years{k}')
            )
            for k in range(number_of_maintenance_items)
        )
        st.write("Total Maintenance Cost (Present Worth): ", total_maintenance_cost)

    st.session_state.total_LCC = total_capital_cost + total_replacement_cost + total_maintenance_cost
    st.write("Total Life Cycle Cost (LCC): ", st.session_state.total_LCC)

    interest_rate = st.number_input("Interest Rate for ALCC (%)", value=5.0, step=0.1)
    project_years = st.number_input("Total Project Lifespan (years)", value=20, step=1)
    if st.button('Calculate ALCC'):
        ALCC = calculate_ALCC(st.session_state.total_LCC, interest_rate, project_years)
        st.write("Annualized Life Cycle Cost (ALCC): ", ALCC)
        units_per_year = st.number_input("Units Consumed Per Year", value=1000, step=100)
        per_unit_cost = ALCC / units_per_year if units_per_year else 0
        st.write("Per Unit Cost Per Year: ", per_unit_cost)




        # Existing code from above goes here...

    # Additional section for ALCC and per unit cost calculation
    st.write("### Additional ALCC and Per Unit Cost Calculation")
    input_LCC = st.number_input("Enter Life Cycle Cost (LCC)", value=st.session_state.total_LCC, format='%f')
    input_interest_rate = st.number_input("Enter Annual Interest Rate (%) for ALCC", value=5.0, format='%f')
    input_project_years = st.number_input("Enter Total Project Lifespan (years)", value=20, format='%f')
    input_units_per_year = st.number_input("Enter Units Consumed Per Year", value=1000, format='%f')

    if st.button('Calculate Additional ALCC and Per Unit Cost'):
        additional_ALCC = calculate_ALCC(input_LCC, input_interest_rate, input_project_years)
        st.write("Calculated Annualized Life Cycle Cost (ALCC): ", additional_ALCC)
        additional_per_unit_cost = additional_ALCC / input_units_per_year if input_units_per_year else 0
        st.write("Calculated Per Unit Cost Per Year: ", additional_per_unit_cost)

if __name__ == "__main__":
    main()











