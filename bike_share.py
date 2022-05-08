"""
This project helps us to explore data for a BikeShare company
in some cities ('Chicago', 'New York', 'Wsahingtone')
"""

import time
import numpy as np
import pandas as pd


data_names = {'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv', 'washington': 'washington.csv'}
time_list = ['month', 'day', 'both', 'none']
month_list = ['January', 'February', 'March', 'April', 'May', 'June']
day_list = ['Sunday', 'Monday', 'Tuesday',
            'Wednesday', 'Thursday', 'Friday', 'Saturday']
day_dict = {'Sunday': 1, 'Monday': 2, 'Tuseday': 3,
            'Wendsday': 4, 'Thursday': 5, 'Friday': 6, 'Saturday': 7}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    month, day = 'all', 'all'

    correct_filter = False
    while not correct_filter:
        city = input(
            "Which city do you want to see data from (chicago - new york - washington)?\n").lower().strip()
        if city in data_names:
            correct_filter = True
        else:
            print("You can only choose from (chicago - new york - washington).\n")

    correct_filter = False
    while not correct_filter:
        time_filter = input(
            "Do you want to filter you data by month, day, both or none of them (month - day - both - none)?\n").lower().strip()
        if time_filter in time_list:
            correct_filter = True
        else:
            print("You can only choose from (month - day - both - none).\n")

    if time_filter == 'month' or time_filter == 'both':
        correct_filter = False
        while not correct_filter:
            month = input(
                "Which month do you want to get your in (January - February - March - April - May - June)?\n").title().strip()
            if month in month_list:
                month = month_list.index(month)+1
                correct_filter = True
            else:
                print(
                    "You can only choose from (January - February - March - April - May - June).\n")

    if time_filter == 'day' or time_filter == 'both':
        correct_filter = False
        while not correct_filter:
            day = input(
                "Which day do you want to get your on?\n").title().strip()
            if day in day_list:

                correct_filter = True
            else:
                print("You can only choose from week days.\n")

    return city, month, day, time_filter


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(data_names[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day'] == day]

    return df


def raw_data(df):
    """
    Asks the user if he wants to display 5 rows of data.
    Prints:
        Five rows of data.
    """

    number_of_rows = len(df.index)
    loopp = True
    i = 0

    while(i+5 <= number_of_rows) and loopp:
        choise = input(
            "Do you want to see 5 rows of date (y,n)?\n").lower().strip()
        if choise == 'y':
            print(df[i:i+5])
            i = i+5
        if choise == 'n':
            loopp = False
        if choise not in ['y', 'n']:
            print('You can only choose from (y - n).\n')

    print('\n', '*'*100)


def time_stats(df, time_filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['hour'] = df['Start Time'].dt.hour

    if time_filter == 'month':
        print("The most frequent day is : ", df['day'].mode()[0])
        print("The most frequent hour is : ", df['hour'].mode()[0])
        print('\tYour filter is : '.expandtabs(3), time_filter)

    if time_filter == 'day':
        print("The most frequent month is : ", df['month'].mode()[0])
        print("The most frequent hour is : ", df['hour'].mode()[0])
        print('\tYour filter is : '.expandtabs(3), time_filter)

    if time_filter == 'both':
        print("The most frequent hour is : ", df['hour'].mode()[0])
        print('\tYour filter is : '.expandtabs(3), time_filter)

    if time_filter == 'none':
        print("The most frequent month is : ", df['month'].mode()[0])
        print("The most frequent day is : ", df['day'].mode()[0])
        print("The most frequent hour is : ", df['hour'].mode()[0])
        print('\tYour filter is : '.expandtabs(3), time_filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most common start station is : ', df['Start Station'].mode()[0])
    print('Most common end station is : ', df['End Station'].mode()[0])
    df['Route'] = df['Start Station'] + ' to ' + df['End Station']
    print('Most common route is : ', df['Route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("The total travel time is : ", df['Trip Duration'].sum(
    ), ' seconds or : ', df['Trip Duration'].sum()/3600, 'hours.')
    print("The average travel time is : ", df['Trip Duration'].mean(
    ), ' seconds or : ', df['Trip Duration'].mean()/3600, 'hours.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("The count of user type is :\n", df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print("The count of user gender is :\n", df['Gender'].value_counts())

    if 'Birth Year' in df.columns:
        print('The earliest user\'s date of birth is : ',
              df['Birth Year'].min())
        print('The most recent user\'s date of birth is : ',
              df['Birth Year'].max())
        print('The most common user\'s date of birth is : ',
              df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    while True:

        print('Hello! Let\'s explore some US bikeshare data!\n')

        city, month, day, time_filter = get_filters()
        df = load_data(city, month, day)
        raw_data(df)
        time_stats(df, time_filter)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input(
            '\nWould you like to restart? Enter yes or no.\n').lower().strip()
        if restart.lower() != 'yes':
            break

        print('\n', '*'*100, '\n')


if __name__ == "__main__":
    main()
