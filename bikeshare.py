import time
import pandas as pd
import numpy as np


CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}
#End input validation function

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    """Filter and load the data based of user input"""
    
    print('Hello! Let\'s explore some US bikeshare data!')
    

    city = input(
        'Would you like to see data for Chicago, New York, or Washington? ').lower()
    while city not in ['chicago', 'new york', 'washington']:
        print("that's invalid input")
        city = input(
            'please input the city? :choose either chicago, new york city,washington : ').lower()
    months = ["january", "february", "march",
              "april", "may", "june", "all"]
    month = input(
        "Which month - January, February, March, April, May, June, or all?").lower()
    while month not in months:
        print("invalid month input")
        month = input(
            "Which month - January, February, March, April, May, or June, or all?").lower()
    days = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = input(
        "which day - Monday, tuesday, wednesday,thursday,friday,saturday,sunday  or all ?").lower()
    while day not in days:
        print('invalid day input')
        day = input(
            "which day - Monday, tuesday, wednesday,thursday,friday,saturday,sunday, or all ?").lower()
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

   
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

  
    if month != 'all':
     
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
 
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    popular_month = df['month'].mode()[0]

 
    popular_day = df['day_of_week'].mode()[0]


    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("the most popular hour is ", popular_hour)
    print("the most popular month is ", popular_month)
    print("the most popular day is ", popular_day)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    common_start_station = df["Start Station"].mode()[0]
    count_start = df[df["Start Station"] == common_start_station].count()[0]

    common_end_station = df["End Station"].mode()[0]
    count_end = df[df["End Station"] == common_end_station].count()[0]

 
    df['route'] = df['Start Station'] + "-" + df['End Station']
    common_route = df['route'].mode()[0]
    common_route_count = df[df['route'] == common_route].count()[0]
    print("the most common start station is ",
          common_start_station, "/count:", count_start)
    print("the most common end station is ",
          common_end_station, "/count:", count_end)
    print("the most common route is ", common_route,
          "/count :", common_route_count)
  

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

  
    total_travel_time = df["Trip Duration"].sum()


    average_travel_time = df["Trip Duration"].mean()

    print("total travel time is : {} minutes".format(total_travel_time / 60))
    print("average travel time is : {}  minutes".format(average_travel_time / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    user_types_count = df["User Type"].value_counts().to_frame()
    print("user types:\n", user_types_count)


    try:
        counts_of_gender = df["Gender"].value_counts().to_frame()
        print("user gender:\n", counts_of_gender)
    except:
        print("no data available about gender for Washington")

   
    try:
        earlies_year_of_birth = int(df["Birth Year"].min())
        print("earliest year of birth is:", earlies_year_of_birth)

        most_recent_year_of_birth = int(df["Birth Year"].max())
        print("most recent year of birth  is:", most_recent_year_of_birth)

        most_common_year_of_birth = int(df["Birth Year"].mode())
        print("most common year of birth is:", most_common_year_of_birth)
    except:
        print("no data available about birth year for Washington")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(city):
    """
    the function displays row data of the choosen city as chunks of 5 rows based on the user's choice.
    """
    df = pd.read_csv(CITY_DATA[city])
    print('If you would , row data is available to view...')

    step = 0
    while True:
        answer = input(
            "Would you like to view indiviual trip data in chunks of 5 rows ? type 'yes' or 'no':").lower()
        if answer not in ["yes", "no"]:
            print("invalid answer! , please type 'yes' or 'no'")
        elif answer == "yes":
            print(df.iloc[step:step + 5])
            step += 5
        elif answer == "no":
            print("exiting now ..")
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
