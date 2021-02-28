import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
months_list = ['january', 'february', 'march', 'april', 'may', 'june']
week_list = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']


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
    while True:
        city = input('\nPlease choose one city of your interest: Chicago, New York, Washington:\n').strip().lower()
        if city in ['chicago', 'new york', 'washington']:
            print('\nYou\'ve chosen city: {}'.format(city))
            break
        else:
            print('Please check your typing...')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nPlease choose one month of your interest: January, February, March, April, \
May or June (Type "all" for all months):\n').strip().lower()
        if month in months_list or month == 'all':
            print('\nYou\'ve chosen month: {}'.format(month))
            break
        else:
            print('Please check your typing...')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nPlease choose one day of week of your interest: (e.g. 0=Monday) \
(Type "all" for all months)\n').strip().lower()
        if day in '0123456':
            print('\nYou\'ve chosen day of week: {}'.format(week_list[int(day)]))
            break
        elif day == 'all':
            print('\nYou\'ve chosen day of week: all')
            break
        else:
            print('Please check your typing...')

    print('-'*40)
    print('\nYou\'ve chosen city: {}, month: {}, day of week: {}'.format(city, month, day))
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
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    # Display raw data if useer wants to.
    count = 0
    while True:
        display_raw = input('\nWould you like to see raw data, with 5 lines a time? (Yes/No)\n').strip().lower()
        if display_raw == 'yes':
            print(df.iloc[count:count+5])
            count = count + 5
        else:
            break
    # Convert time to datetime datatype and extract month and day of week to new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        month = months_list.index(month) + 1
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day if applicable
    if day != 'all':
        day = int(day)
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day]

    # Display raw data if useer wants to.
    count = 0
    while True:
        display_pro = input('\nWould you like to see filtered data, with 5 lines a time? (Yes/No)\n').strip().lower()
        if display_pro == 'yes':
            print(df.iloc[count:count+5])
            count = count + 5
        else:
            break

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        pop_month = df['month'].mode()[0]
        print('Result: the most common month: {}'.format(pop_month))

    # display the most common day of week
    if day == 'all':
        pop_day = df['day_of_week'].mode()[0]
        print('The most common day of week: {}'.format(week_list[pop_day]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    pop_hour = df['hour'].mode()[0]
    print('The most common start hour: {}'.format(pop_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # display most commonly used end station
    pop_start_stat = df['Start Station'].mode()[0]
    pop_end_stat = df['End Station'].mode()[0]
    print('\nThe most popular start station and end station is {} and {}, respectively'.format(pop_start_stat, pop_end_stat))

    # display most frequent combination of start station and end station trip
    pop_combo_stat = df[['Start Station','End Station']].value_counts().index.tolist()[0]
    print('\nThe most popular combination of start and end stations: {}'.format(pop_combo_stat))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # display mean travel time
    tot_dur = df['Trip Duration'].sum()/3600
    mean_dur = df['Trip Duration'].mean()/3600
    print('\nTotal and mean travel time (hours) in the selected months and/or days is {} and {}, respectively'.format(tot_dur, mean_dur))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    utype_index = df['User Type'].value_counts().index
    utype_value = df['User Type'].value_counts().values
    print('\nUser type 1: {}, counts: {};\nUser type 2: {}, counts: {};\n'.format(utype_index[0], utype_value[0], utype_index[1], utype_value[1]))

    if city.lower() == 'washington':
        print('We are lack of info about gender and birth year of users in Washington.')
    else:
        # Display counts of gender
        gender_index = df['Gender'].value_counts().index
        gender_value = df['Gender'].value_counts().values
        print('\nGender: {}, counts: {};\nGender: {}, counts: {};\n'.format(gender_index[0],gender_value[0],gender_index[1],gender_value[1]))
        # Display earliest, most recent, and most common year of birth
        early_birth = int(df['Birth Year'].min())
        recent_birth = int(df['Birth Year'].max())
        pop_birth = int(df['Birth Year'].mode()[0])
        print('\nYear of birth:\nearlies: {}\nmost recent: {}\nmost common: {}'.format(early_birth, recent_birth, pop_birth))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
