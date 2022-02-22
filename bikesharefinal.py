import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input("Please enter the name of the city(either chicago or new york city or washington) to analyze: ").lower()
    while True:
        if city in cities:
            print('  ')
            print('Thanks for the input.The city name you have selected is: {}'.format(city))
            break
        else:
            print(' ')
            print("The city name you entered is not a valid one . Please enter a city name among chicago, new york city or washington without any typo. Let us start again.")
            print(' ')
            city = input("Please enter the name of the city(either chicago or new york city or washington) to analyze: ").lower()

    print('  ')
    # get user input for month (all, january, february, ... , june)
    month = input("Plese enter a month from january to june. Please enter 'all' if you don't want to filter by month: ").lower()
    while True:
        if month in months:
            print('  ')
            print("Thank you. The month filter you have entered is: {}".format(month))
            break
        else:
            print(' ')
            print("The option entered for filtering the data by month is not a valid one. Please enter a month from january through june without any typo or enter 'all' in order not to filter by any month")
            print(' ')
            month = input("Plese enter the month for which you would like to analyze the data from january to june. Please enter 'all' if you don't want to filter by month: ").lower()
    print('  ')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter a day of the week.Please enter 'all' if you don't want to filter by day: ").lower()
    while True:
        if day in days:
            print('  ')
            print("Thank you. The day filter you have entered is: {}".format(day))
            break
        else:
            print('  ')
            print("The option entered for filtering the data by day is not a valid one. Please enter the name of a day without any typo or enter 'all' in order not to filter by any day")
            print(' ')
            day = input("Please enter the day of the week for which you would like to analyze the data.Please enter 'all' if you don't want to filter by day: ").lower()

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months_only = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months_only.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month:',common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of week:',common_day)

    # display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print('The most common start hour:',common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station:',common_start_station)
    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station:',common_end_station)

    # display most frequent combination of start station and end station trip
    df['combination_of_stations'] = df['Start Station']+' AND '+df['End Station']
    frequent_combination = df['combination_of_stations'].mode()[0]
    print('The most frequent combination of start station and end station trip:', frequent_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is:',total_travel_time/3600,'hrs')


    # display mean travel time
    average_trip_duration = df['Trip Duration'].mean()
    print('Mean travel time is:',average_trip_duration/60,'mins')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('Count of user types:\n', user_types_count)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('Count of gender:\n',gender_count)
    else:
        print('Gender information is not availabe for washington city')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_yob = df['Birth Year'].min()
        print('The earliest year of birth is:',earliest_yob)
        latest_yob = df['Birth Year'].max()
        print('The most recent year of birth is:',latest_yob)
        common_yob = df['Birth Year'].mode()[0]
        print('The most common year of birth is:',common_yob)
    else:
        print('Year of birth information is not availabe for washington city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def req_raw_data(df):
    raw_data = input("Would you like to see the raw data? Plese enter y or n: ").lower()
    n = 0
    while True:
        if raw_data == 'y':
            print(df.iloc[n:n+5, 1:9])
            more_data = input("Would you like to see more raw data? Please enter y or n: ").lower()
            if more_data == 'y':
                n +=5
            elif more_data == 'n':
                break
            else:
                print("please enter y or n. Please do not enter anything else.")
                more_data = input("Would you like to see more raw data? Please enter y or n: ").lower()
        elif raw_data == 'n':
            print("Thanks for your input. You have chosen not to see the raw data.")
            break
        else:
            print("please enter y or n. Please do not enter anything else.")
            raw_data = input("Would you like to see the raw data? Plese enter y or n: ").lower()
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        req_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
