import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city = ' '
        #use .keys to retrieve data from the city data dictionary
    while city not in CITY_DATA.keys():
        print ("The cities you are able to look at today are: Chicago, New York City, or Washington")
        print ("Which city will you be looking at today?")
            #.lower helps make things standard
        city = input().lower()
        if city not in CITY_DATA.keys():
            print ("please try again, we did not like that answer.")
    print ("You have chosen to look at:", city)
    
    # get user input for month (all, january, february, ... , june)
    # creates a list/dictionary of months that are from january to june
    MONTH_DATA = {'all': 1, 'january': 2, 'february': 3, 'march': 4, 'april': 5, 'may': 6, 'june': 7}
    #so you can then just use month instead of months
    month = ' '
    while month not in MONTH_DATA.keys():
        print ("Plase enter what month you would like to look at. We provide informatino from January- June.")
        print ("if you want to see data for all months, type ALL")
        month = input().lower()
        if month not in MONTH_DATA.keys():
            print ("somehow, we dont know that answer, check your spelling and try again")
    print ("You have chosen the month of:", month)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week_data = {'all': 1, 'monday': 2, 'tuesday': 3, 'wednesday': 4, 'thursday': 5, 'friday': 6, 'saturday': 7, 'sunday': 8}
    #same idea as months and cities, makes a list of the days of the week
    day = ' '
    while day not in day_of_week_data.keys():
        print ("What day are you looking for?")
        print ("If looking for every day, type all")
        day = input().lower()
        if day not in day_of_week_data.keys():
            print ("please check your spelling, we do not know that day")
    print ("You chose:", day)

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
    #all of this will load the the data for city, time, and month
    print ("let me load your infomation")
    df = pd.read_csv(CITY_DATA[city])
    #will need to convert the start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #to make it easier to read and understand
    #create new columns from the start time that will read as month and day
    df['month'] = df['Start Time'].dt.month
    #filter the month by using not equal, pretty much due to the all option
    if month != 'all':
        months = ['january', 'febuary', 'march', 'april', 'june']
        month = months.index(month) + 1
    df['day'] = df['Start Time'].dt.weekday_name
    #will need to filter the days to...
    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    #use .mode to find the information that is repeated most often
    pop_month = df['month'].mode()[0]
    print ("The most popular month is:", pop_month)
        
    # display the most common day of week
    pop_day = df['day'].mode()[0]
    print ("The most popular day is:", pop_day)

    # display the most common start hour
    #this first line takes the hour from the start time column
    df['hour'] = df['Start Time'].dt.hour
    pop_start_hour = df['hour'].mode()[0]
    print ("The most popular start hour is:", pop_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    #use .mode here like in time, if finds the most reoccuring station in that collumn
    common_start = df['Start Station'].mode()[0]
    print ("the most common starting station is:", common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print ("the most common end station is:", common_end)

    # display most frequent combination of start station and end station trip
    start_station = df['Start Station'].mode()
    end_station = df['End Station'].mode()
    Start_To_End = start_station.str.cat(end_station)
    combo = Start_To_End.mode()[0]
    print ('Most commonly used combination of stations is:', combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    #use .sum to find the total (or sum) of time
    total_travel = df['Trip Duration'].sum()
    #since that collumn is in seconds, this finds the minutes
    minute, second = divmod(total_travel, 60)
    print ("The total travel time, in minutes, is: {minute} min and {seconds} sec.")

    # display mean travel time
    # will use round () to give a decimal
    #use mean, to find the mean...
    mean_travel = round(df['Trip Duration'].mean())
    print ("The mean amount of travel, in seconds, is:", mean_travel)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    #use .value_count becuase these are considered unique data
    user_type_count = df['User Type'].value_counts()
    print ("The user type count is", user_type_count)

    # Display counts of gender
    #since there is no washington gender info, we have to do this
    # try lets you test for erros
    #if there is an error,fix or handle the error with except 
    try:
        gender = df['Gender'].value_counts()
        print ("The count of gender types are", gender)
    except:
        print ("you have chose Washington, there is no gender data for that city.")
        

    # Display earliest, most recent, and most common year of birth
    #the same concept will apply to birth related data as it did gender
    try:
        birth_year = df['Birth Year'].mode()
        earlist_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        print ("Most common user birth year:", birth_year)
        print ("Earlist birth year:", earlist_year)
        print ("Most recent birth year:", most_recent_year)
    except:
        print ("There is no birth information in this file, since you chose the evergood Evergreen state...")
        print ("aka Washington...")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

