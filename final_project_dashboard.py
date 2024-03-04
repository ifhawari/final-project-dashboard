# import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style = "whitegrid")

# define helper functions
def create_hourly_rental(data):
    hourly_rental = data[["dteday", "hr", "cnt"]]
    hourly_rental.rename(columns = {
        "dteday": "date",
        "hr": "hour",
        "cnt": "total_rent"
    }, inplace = True)
    return hourly_rental

def create_daily_rental(data):
    daily_rental = data.groupby(by = "dteday").agg({
        "cnt": "sum"
    }).reset_index()
    daily_rental.rename(columns = {
        "dteday": "date",
        "cnt": "total_rent"
    }, inplace = True)
    return daily_rental

def create_monthly_rental(data):
    monthly_rental = data.groupby(by = "mnth").agg({
        "cnt": "sum"
    }).reset_index()
    monthly_rental.rename(columns = {
        "mnth": "month",
        "cnt": "total_rent"
    }, inplace = True)
    order_month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_rental["month"] = pd.Categorical(monthly_rental["month"], categories = order_month, ordered = True)
    monthly_rental = monthly_rental.sort_values(by = "month")
    return monthly_rental

def create_temp_rent(data):
    temp_rent = data.groupby(by = "dteday").agg({
        "temp": "mean",
        "registered": "sum",
        "casual": "sum"
    }).reset_index()
    temp_rent.drop(columns = "dteday", inplace = True)
    temp_rent = pd.melt(temp_rent, id_vars = "temp", var_name = "users", value_name = "total_rent")
    temp_rent.rename(columns = {"temp": "temperature"}, inplace = True)
    return temp_rent

def create_rental_per_weekday(data):
    rental_per_weekday = data.groupby(by = "weekday").agg({
        "registered": "sum",
        "casual" : "sum"
    }).reset_index()
    rental_per_weekday = pd.melt(rental_per_weekday, id_vars = "weekday", var_name = "users", value_name = "total_rent")
    order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    rental_per_weekday["weekday"] = pd.Categorical(rental_per_weekday["weekday"], categories = order, ordered = True)
    rental_per_weekday = rental_per_weekday.sort_values(by = "weekday")
    return rental_per_weekday

def create_rental_workingday_per_hour(data):
    rental_workingday_per_hour = data.groupby(by = ["yr", "hr", "workingday"]).agg({
        "cnt": "sum"
    }).reset_index()
    rental_workingday_per_hour.rename(columns = {
        "yr": "year",
        "hr": "hour",
        "cnt": "total_rent"
    }, inplace = True)
    return rental_workingday_per_hour

def create_rental_seasons_per_hour(data):
    rental_seasons_per_hour = data.groupby(by = ["yr", "hr", "season"]).agg({
        "cnt": "sum"
    }).reset_index()
    rental_seasons_per_hour.rename(columns = {
        "yr": "year",
        "hr": "hour",
        "cnt": "total_rent"
    }, inplace = True)
    return rental_seasons_per_hour

def create_rental_users_per_month(data):
    rental_users_per_month = data.groupby(by = ["yr", "mnth"]).agg({
        "registered": "sum",
        "casual": "sum"
    }).reset_index()
    rental_users_per_month = pd.melt(rental_users_per_month, id_vars = ["yr", "mnth"], var_name = "users", value_name = "total_rent")
    rental_users_per_month.rename(columns = {
        "yr": "year",
        "mnth": "month"
    }, inplace = True)
    order_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    rental_users_per_month["month"] = pd.Categorical(rental_users_per_month["month"], categories = order_months, ordered = True)
    rental_users_per_month = rental_users_per_month.sort_values(by = "month")
    return rental_users_per_month

def create_rental_per_weather(data):
    rental_per_weather = data.groupby(by = "weathersit").agg({
        "registered": "sum",
        "casual" : "sum"
    }).reset_index()
    rental_per_weather = pd.melt(rental_per_weather, id_vars = "weathersit", var_name = "users", value_name = "total_rent")
    rental_per_weather.rename(columns = {"weathersit": "weather_cond"}, inplace = True)
    return rental_per_weather

def format_num(num):
    if abs(num) < 1000:
        return num
    elif abs(num) < 1000000:
        return "{:.2f}K".format(num/1000)
    else:
        return "{:.2f}M".format(num/1000000)

# load data
bike_share_hour = pd.read_csv("clean_bikeshare_hour.csv")

# change data type of datetime and categorical columns
bike_share_hour["dteday"] = pd.to_datetime(bike_share_hour["dteday"])
bike_share_hour["season"] = bike_share_hour["season"].astype("category")
bike_share_hour["yr"] = bike_share_hour["yr"].astype("category")
bike_share_hour["mnth"] = bike_share_hour["mnth"].astype("category")
bike_share_hour["hr"] = bike_share_hour["hr"].astype("category")
bike_share_hour["holiday"] = bike_share_hour["holiday"].astype("category")
bike_share_hour["weekday"] = bike_share_hour["weekday"].astype("category")
bike_share_hour["workingday"] = bike_share_hour["workingday"].astype("category")
bike_share_hour["weathersit"] = bike_share_hour["weathersit"].astype("category")

# create date filter for data
st.sidebar.header("Filter Date")
min_date = bike_share_hour["dteday"].min()
max_date = bike_share_hour["dteday"].max()

with st.sidebar:
    start, end = st.date_input(
        label = "Date",
        min_value = min_date,
        max_value = max_date,
        value = [min_date, max_date]
    )

df = bike_share_hour[(bike_share_hour["dteday"] >= str(start)) & (bike_share_hour["dteday"] <= str(end))]

# Create dataframes with helper functions
hourly_rental = create_hourly_rental(df)
daily_rental = create_daily_rental(df)
monthly_rental = create_monthly_rental(df)
temp_rent = create_temp_rent(df)
rental_per_weekday = create_rental_per_weekday(df)
rental_workingday_per_hour = create_rental_workingday_per_hour(df)
rental_seasons_per_hour = create_rental_seasons_per_hour(df)
rental_users_per_month = create_rental_users_per_month(df)
rental_per_weather = create_rental_per_weather(df)

# create header
st.header("Capital Bikeshare Rental Dashboard")

total_rent = format_num(daily_rental["total_rent"].sum())
st.metric("Total Rental", value = total_rent)

# create subheader for hourly rental
st.subheader("Hourly Rental")

# create KPI for hourly rental
col1, col2, col3 = st.columns(3)

with col1:
    hourly_highest_rent = format_num(hourly_rental["total_rent"].max())
    st.metric("Hourly Highest Rental", value = hourly_highest_rent)

with col2:
    hour_max_rent = hourly_rental[hourly_rental["total_rent"] == hourly_rental["total_rent"].max()]
    hour_highest_rent = hour_max_rent["hour"].values[0]
    st.metric("Hour of the Hourly Highest Rental", value = hour_highest_rent)

with col3:
    date_hourly_max_rent = str(hour_max_rent["date"].max().date())
    st.metric("Date of the Hourly Highest Rental", value = date_hourly_max_rent)

# create chart for hourly rental

# total of bike sharing rental by working day per hour
workingday_year_2011 = rental_workingday_per_hour[rental_workingday_per_hour["year"] == 2011]
workingday_year_2012 = rental_workingday_per_hour[rental_workingday_per_hour["year"] == 2012]

fig, ax = plt.subplots(nrows = 2, figsize = (15, 12))
sns.pointplot(
    data = workingday_year_2011,
    x = "hour",
    y = "total_rent",
    hue = "workingday",
    palette = ["#34ae91", "#3ba3ec"],
    ax = ax[0]
)
sns.pointplot(
    data = workingday_year_2012,
    x = "hour",
    y = "total_rent",
    hue = "workingday",
    palette = ["#34ae91", "#3ba3ec"],
    ax = ax[1]
)
fig.suptitle("Total of Bike Sharing Rental by Working Day per Hour", fontsize = 20, fontweight = "bold")
ax[0].set_title("Year 2011", fontsize = 14, fontweight = "bold")
ax[1].set_title("Year 2012", fontsize = 14, fontweight = "bold")

for a in [0,1]:
    ax[a].set_xlabel("Hour of The Day")
end

for i in [0,1]:
    ax[i].set_ylabel("Total Rent")
end

st.pyplot(fig)

# total of bike sharing rental by season per hour
season_year_2011 = rental_seasons_per_hour[rental_seasons_per_hour["year"] == 2011]
season_year_2012 = rental_seasons_per_hour[rental_seasons_per_hour["year"] == 2012]

fig, ax = plt.subplots(nrows = 2, figsize = (15, 12))
sns.pointplot(
    data = season_year_2011,
    x = "hour",
    y = "total_rent",
    hue = "season",
    palette = ["#34ae91", "#bb83f4", "#3ba3ec", "#f77189"],
    ax = ax[0]
)
sns.pointplot(
    data = season_year_2012,
    x = "hour",
    y = "total_rent",
    hue = "season",
    palette = ["#34ae91", "#bb83f4", "#3ba3ec", "#f77189"],
    ax = ax[1]
)
fig.suptitle("Total of Bike Sharing Rental by Season per Hour", fontsize = 20, fontweight = "bold")
ax[0].set_title("Year 2011", fontsize = 14, fontweight = "bold")
ax[1].set_title("Year 2012", fontsize = 14, fontweight = "bold")

for a in [0,1]:
    ax[a].set_xlabel("Hour of The Day")
end

for i in [0,1]:
    ax[i].set_ylabel("Total Rent")
end

st.pyplot(fig)


# create subheader for daily rental
st.subheader("Daily Rental")

# create KPI of daily rental
col1, col2 = st.columns(2)

with col1:
    daily_highest_rent = format_num(daily_rental["total_rent"].max())
    st.metric("Daily Highest Rental", value = daily_highest_rent)

with col2:
    date_max_rent = daily_rental[daily_rental["total_rent"] == daily_rental["total_rent"].max()]
    date_highest_rent = str(date_max_rent["date"].max().date())
    st.metric("Date of the Highest Rent", value = date_highest_rent)

# create chart for daily rental

# total of bike sharing rental by day
fig, ax = plt.subplots(figsize = (8, 6))
sns.barplot(
    data = rental_per_weekday,
    x = "weekday",
    y = "total_rent",
    hue = "users",
    palette = ["#34ae91", "#3ba3ec"],
    ax = ax
)
ax.set_title("Total of Bike Sharing Rental by Day", fontsize = 20, fontweight = "bold")
ax.set_xlabel("Day of The Week")
ax.set_ylabel("Total Rent")

st.pyplot(fig)


# create subheader for monthly rental
st.subheader("Monthly Rental")

# create KPI for monthly rental
col1, col2 = st.columns(2)

with col1:
    monthly_highest_rent = format_num(monthly_rental["total_rent"].max())
    st.metric("Monthly Highest Rental", value = monthly_highest_rent)

with col2:
    month_max_rent = monthly_rental[monthly_rental["total_rent"] == monthly_rental["total_rent"].max()]
    month_highest_rent = month_max_rent["month"].values[0]
    st.metric("Month of the Highest Rental", value = month_highest_rent)

# create chart for monthly rental

# total of bike sharing rental by users per month
user_year_2011 = rental_users_per_month[rental_users_per_month["year"] == 2011]
user_year_2012 = rental_users_per_month[rental_users_per_month["year"] == 2012]

fig, ax = plt.subplots(nrows = 2, figsize = (15, 12))
sns.pointplot(
    data = user_year_2011,
    x = "month",
    y = "total_rent",
    hue = "users",
    palette = ["#34ae91", "#3ba3ec"],
    ax = ax[0]
)
sns.pointplot(
    data = user_year_2012,
    x = "month",
    y = "total_rent",
    hue = "users",
    palette = ["#34ae91", "#3ba3ec"],
    ax = ax[1]
)
fig.suptitle("Total of Bike Sharing Rental by Users per Month", fontsize = 20, fontweight = "bold")
ax[0].set_title("Year 2011", fontsize = 14, fontweight = "bold")
ax[1].set_title("Year 2012", fontsize = 14, fontweight = "bold")

for a in [0,1]:
    ax[a].set_xlabel("Month of The Year")
end

for i in [0,1]:
    ax[i].set_ylabel("Total Rent")
end

st.pyplot(fig)


# create subheader for weather condition
st.subheader("Bike Sharing Rental by Weather")

# best weather for rental bikeshare
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize = (8, 6))
    sns.scatterplot(
        data = temp_rent,
        x = "temperature",
        y = "total_rent",
        hue = "users",
        style = "users",
        palette = ["#34ae91", "#3ba3ec"],
        ax = ax
    )
    ax.set_title("Total Rent with Temperature by Users", fontsize = 20, fontweight = "bold")
    ax.set_xlabel("Temperature in Celsius")
    ax.set_ylabel("Total Rent")
    st.pyplot(fig)
    
with col2:
    fig, ax = plt.subplots(figsize = (8, 6))
    sns.barplot(
        data = rental_per_weather,
        x = "weather_cond",
        y = "total_rent",
        hue = "users",
        palette = ["#34ae91", "#3ba3ec"],
        ax = ax)
    ax.set_title("Total of Bike Sharing Rental by Weather", fontsize = 20, fontweight = "bold")
    ax.set_xlabel("Weather Condition")
    ax.set_ylabel("Total Rent")
    st.pyplot(fig)

st.caption("Copyright Isnayni Feby Hawari 2024")