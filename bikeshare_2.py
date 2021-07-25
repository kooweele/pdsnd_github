""" Added new comments to Bikeshare.py on 25th July
This file is the run file to analyze bike share data in 3 US States
"""
import time
import pandas as pd
import numpy as np
import os as os
import platform as platform

CITY_DATA = { 'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday','wednesday','thursday','friday','saturday','sunday']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    is_valid_input = False
    while is_valid_input == False:
        print('Hello! Let\'s explore some US bikeshare data!')
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input("Input a City ('chicago','new york city','washington') :").lower()
        if city not in CITY_DATA.keys():
            print("Error: invalid city input")
            continue

        # get user input for month (all, january, february, ... , june)
        month = input("Input a Month ('january','february',..,'june') or 'all' :").lower()
        if month not in months and month != "all":
            print("Error: invalid month input")
            continue

        # get user input for day of week (all, monday, tuesday, ... sunday)
        day =  input("Input a Day ('monday','tuesday',..,'sunday') or 'all':").lower()
        if day not in days and day != "all":
            print("Error: invalid day input")
            continue

        is_valid_input = True
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
    df['Start Time'] =pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['day of week'] = df['Start Time'].dt.weekday
    df['month'] = df['Start Time'].dt.month

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_value = months.index(month) + 1  # convert search variable month to int
        #print(' Search Month: ', month, ' is converted  to ',month_value)
        df = df.loc[df['month'] == month_value]
        #print (month.head(3))
        #print (df[['Start Time','month']].head(3))   ## select to display 2 columns of df

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day_value = days.index(day) # monday = 0 , sun = 6
        df = df.loc[df['day of week'] == day_value]
        #print (' Search Day: ', day , ' is converted to ',day_value)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    '''
    Find:-
    •	most common month
    •	most common day of week
    •	most common hour of day
    '''

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month_df = df[['month','Start Time']].groupby(['month']).count().sort_values('Start Time',ascending=False).head(1)
    most_common_month = most_common_month_df.index[0] -1 # to compensate 0 = january, line 64 of load_data
    most_common_month_riders = most_common_month_df.iat[0,0] #iat = return single cell value by [row_index, column_index]
    #print ('3. most_common_month_count ',most_common_month_count )
    print ('The most common month is ',months[most_common_month].title() , ' with ' ,most_common_month_riders , ' total riders for the month')

    # display the most common day of week
    most_common_wk_day_df = df[['day of week','Start Time']].groupby(['day of week']).count().sort_values('Start Time',ascending=False).head(1)
    most_common_wk_day = most_common_wk_day_df.index[0]  # monday = 0 , sun = 6, line 74 of load_data
    most_common_wk_day_riders = most_common_wk_day_df.iat[0,0]
    #print ('Most common weekeday dataframe')
    print ('The most common weekday is ',days[most_common_wk_day].title() , ' with ' ,most_common_wk_day_riders , ' total riders on the day')

    # display the most common start hour
    df['Start Hr'] = df['Start Time'].dt.hour
    most_common_start_hr_df = df[['Start Hr','Start Time']].groupby(['Start Hr']).count().sort_values('Start Time',ascending=False).head(1)
    most_common_start_hr = most_common_start_hr_df.index[0]
    most_common_start_hr_riders = most_common_start_hr_df.iat[0,0]
    print ('The most common starting hour is ', most_common_start_hr, ' with ' ,most_common_start_hr_riders , ' total riders on the hour')
    #print (most_common_start_hr_df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    '''
    #2 Popular stations and trip
    •	most common start station
    •	most common end station
    •	most common trip from start to end (i.e., most frequent combination of start station and end station)
    '''
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    #print(df.count())
    #print(df.iloc[:, [1,4]])    # print all rows of selected columns 1 and 4

    # display most commonly used start station
    most_common_start_station_df = df[['Start Station','Start Time']].groupby(['Start Station']).count().sort_values('Start Time',ascending=False).head(1)
    most_common_start_station = most_common_start_station_df.index[0]
    most_common_start_station_riders = most_common_start_station_df.iat[0,0]
    #print('DataFrame grouped by start station')
    #print(df[['Start Station','Start Time']].groupby(['Start Station']).count().sort_values('Start Time',ascending=False))
    print ('The popular Start Station is ',most_common_start_station.title() , ' with ' ,most_common_start_station_riders , ' total riders with the Station.')

    # display most commonly used end station
    most_common_end_station_df = df[['End Station','Start Time']].groupby(['End Station']).count().sort_values('Start Time',ascending=False).head(1)
    most_common_end_station = most_common_end_station_df.index[0]
    most_common_end_station_riders = most_common_end_station_df.iat[0,0]
    #print('DataFrame grouped by end station')
    #print(df[['End Station','Start Time']].groupby(['End Station']).count().sort_values('Start Time',ascending=False))
    print ('The popular End Station is ',most_common_end_station.title() , ' with ' ,most_common_end_station_riders , ' total riders with the Station.')

    # display most frequent combination of start station and end station trip
    most_common_startend_station_pair_df =df[['Start Station','End Station','Start Time']].groupby(['Start Station','End Station']).count().sort_values('Start Time',ascending=False)
    #print(most_common_startend_station_pair_df)
    most_common_startend_station_df = most_common_startend_station_pair_df.head(1)
    station_tuple = most_common_startend_station_df.index[0] # group by multiple column returs datafrae where row-index is a tuple of ('Start Station', 'End Station')
    start_station = station_tuple[0]
    end_station = station_tuple[1]
    most_common_startend_station_riders = most_common_startend_station_df.iat[0,0]

    print ('The popular Journey is from ' , start_station.title(), ' to ' , end_station, ' Station with ', most_common_startend_station_riders , ' total riders on this line.')
    #print ("Start:", start_station, " - " , end_station)

    #print ('Counts ', new_df.counts)

    #print ('1.', new_df[['Start Station']])
    #print ('2.', new_df.iat([0],[1]))
    #print ('3.', new_df.iat([0],[2]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    '''
    #3 Trip duration
    •	total travel time
    •	average travel time
    '''
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print ('Total trip duration/travel time is ', df['Trip Duration'].sum(), ' with ' , df['Trip Duration'].count(), ' trips made.')

    # display mean travel time
    print ('Mean trip travel time is ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    '''
    #4 User info
    •	counts of each user type
    •	counts of each gender (only available for NYC and Chicago)
    •	earliest, most recent, most common year of birth (only available for NYC and Chicago)

    '''
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_user_types_df = df[['User Type','Start Time']].groupby(['User Type']).count()
    counts_user_types_df = counts_user_types_df.rename(columns = {'Start Time':'Count of Riders by User Types'})
    #counts_user_types_df.columns = ['Count User Types']  #same effect of rename 1 column

    print ('Summary of Riders by User Types:-')
    print (counts_user_types_df)
    print ("\n")
    # Display counts of gender
    if 'Gender' in df.columns:
        counts_gender_df = df[['Gender','Start Time']].groupby(['Gender']).count()
        counts_gender_df = counts_gender_df.rename(columns = {'Start Time':'Count of Riders by Gender'})
        print ('Summary of Riders by Gender:-')
        print (counts_gender_df)
    else:
        print('No data for Gender classification')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year_df = df[['Birth Year','Start Time']].groupby(['Birth Year']).count()
        #reindex_birth_year_df = birth_year_df.transpose() # change shape by swapping rows to columns of new df
        #print('Dataframe by Birth Year')
        #print(birth_year_df)
        earliest_birth_year = birth_year_df.sort_values(by='Birth Year', ascending = True).head(1).index[0]
        latest_birth_year = birth_year_df.sort_values(by='Birth Year', ascending = False).head(1).index[0]
        count_by_birth_year_df = birth_year_df.sort_values(by='Start Time', ascending = False)#.head(1).index[0]
        most_common_year_of_birth = count_by_birth_year_df.head(1).index[0]
        count_most_common_year_of_birth = count_by_birth_year_df.iat[0,0]
        print('Earliest Birth Year:',earliest_birth_year )
        print('Most Recent Birth Year:',latest_birth_year )
        print('Most Common Birth Year is ',most_common_year_of_birth , ' with ' , count_most_common_year_of_birth , ' riders')
        #print(count_by_birth_year_df)
    else:
        print('No data for Birth Year classification')
    #print(birth_year_df.index.sort())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    '''
    Raw data is displayed upon request by the user in this manner: Script should prompt the user if
    they want to see 5 lines of raw data, display that data if the answer is 'yes', and continue these prompts
    and displays until the user says 'no'.
    '''
    view_data = input("\nWould you like to view 5 rows of individual trip data? Enter 'Y' to view or other key to skip.\n").lower()
    start_loc = 0
    view_more_data = False
    if view_data == 'y':
        view_more_data = True
    while view_more_data:
      print(df.iloc[start_loc:start_loc+5])
      start_loc += 5
      view_data = input("Click 'Y' to view next 5 rows and other key to skip: ").lower()
      if view_data == 'y':
          view_more_data = True
      else:
          view_more_data = False

def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        #print(df.head(5))
        #print(df.count())
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        #print ('OS Name:',os.name)
        #print ('Platform Name:',platform.system())

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        if platform.system() == 'Windows' :
            os.system('cls') #work if script is run on windows not linux

if __name__ == "__main__":
	main()
