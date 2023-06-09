import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
	'''
	Asks user to specify a city, month, and day to analyze.
	
	Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    '''
	print('Hello! Let\'s explore some US bikeshare data!')
	# get user input for city (chicago, new york city, washington); only valid input breaks the loop; if input is not valid, user will be asked to provide input again
	while True:
		city=input('Would you like to see data for Chicago, New York City, or Washington?').casefold()
		if city in CITY_DATA:
			break
		else: 
			print('That is not a valid city name. Please choose Chicago, New York, or Washington')
	while True:
		# get user input for the filter that will be applied
		filter_by=input('Would you like to filter the data by month, day, or not at all?').casefold()
		if filter_by in ['month','day','not at all']:
			break
		else:
			print('That is not a valid filter.Please choose month, day, or not at all.')
	# get user input for the month (january, february, ... , june)
	if filter_by=='month':
		day='all'
		while True:
			month=input('Which month - January, February, March, April, May, or June?').casefold()
			if month in ['january', 'february', 'march', 'april', 'may', 'june']:
				break
			else: 
				print('That is not a valid month. Please choose January, February, March, April, May, or June.')
	# get user input for the the day (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday)
	elif filter_by=='day':
		month='all'
		while True:
			day=input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?').casefold()
			if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
				break
			else:
				print('That is not a valid day. Please choose Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday.')
	else:
		month='all'
		day='all'
	print('-'*40)
	print('City: ', city)
	print('The data is filtered by: ',filter_by)
	print('The month included: ', month)
	print('The day included: ', day)
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
	#loads data for the city
	df = pd.read_csv(CITY_DATA[city])
	#Filters by day and months if applicable
	df['Start Time'] = pd.to_datetime(df['Start Time'])
	df['month']=df['Start Time'].dt.month
	df['day_of_week']=df['Start Time'].dt.day_name()
	if month != 'all':
		months = ['january', 'february', 'march', 'april', 'may', 'june']
		month = months.index(month) + 1
		df = df[df['month'] == month]
	if day != 'all':
		df = df[df['day_of_week'] == day.title()]
	return df

def show_data(df):
	"""
	Ask user whether they want to see the raw data. If yes, first 5 rows are displayed. 
	Then the user is asked again whether they want to see 5 more rows. If yes, 10 rows are displayed. This goes on until user says no.
	"""
	number=5
	while True:
		prompt=input('Do you want to see the first/next five rows if data? Enter yes or no.').casefold()
		if prompt=='yes':
			print(df.head(number))
			number+=5
		elif prompt=='no':
			break
		else: 
			print('That is not a valid input. Enter yes or no.')

def time_stats(df):
	"""Displays statistics on the most frequent times of travel."""
	print('\nCalculating The Most Frequent Times of Travel...\n')
	# display the most common month
	start_time = time.time()
	popular_month = df['month'].mode()[0]
	# display the most common day of week
	popular_day_of_week = df['day_of_week'].mode()[0]
	# display the most common start hour
	df['hour']=df['Start Time'].dt.hour
	popular_hour = df['hour'].mode()[0]
	print('The most popular month is: ', popular_month)
	print('The most popular day of week is: ',popular_day_of_week)
	print('The most popular hour is: ', popular_hour)
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)

def station_stats(df):
	"""Displays statistics on the most popular stations and trip."""
	start_time = time.time()
	# display most commonly used start station
	popular_start_station = df['Start Station'].mode()[0]
	# display most commonly used end station
	popular_end_station = df['End Station'].mode()[0]
	# display most frequent combination of start station and end station trip
	df['trips']=df['Start Station'] + ' to ' + df['End Station']
	popular_trip = df['trips'].mode()[0]
	print('The most popular start station is: ', popular_start_station)
	print('The most popular end station is: ', popular_end_station)
	print('The most popular trip is: ', popular_trip)
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)

def trip_duration_stats(df):
	"""Displays statistics on the total and average trip duration."""
	start_time = time.time()
	# display total travel time
	total_travel_time=df['Trip Duration'].sum()
	# display mean travel time
	avg_travel_time=df['Trip Duration'].mean()
	print('The total travel time is: ', total_travel_time)
	print('The average travel time is: ', avg_travel_time)
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)

def user_stats(df,city):
	"""Displays statistics on bikeshare users."""
	start_time = time.time()
	# Display counts of user types
	value_counts_user_type=df['User Type'].value_counts()
	print('The distribution of user types is: ', value_counts_user_type)
	# Display counts of gender and earliest, most recent, and most common year of birth only for Chicago and New York City
	if city=='chicago' or city=='new york city':
		value_counts_gender=df['Gender'].value_counts()
		earliest_birth_year=df['Birth Year'].min()
		recent_birth_year=df['Birth Year'].max()
		common_birth_year = df['Birth Year'].mode()[0]
		print('The distribution of gender is: ', value_counts_gender)
		print('The earliest birth year is: ', int(earliest_birth_year))
		print('The most recent birth year is: ', int(recent_birth_year))
		print('The most common birth year is: ', int(common_birth_year))
	else:
		print ('For Washington no gender and birth year statistics is available')
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        show_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()
