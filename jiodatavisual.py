import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.cluster import KMeans

def calculate_duration(start_time_str, end_time_str, screen_store, time_format='%Y-%m-%d %H:%M:%S'):
    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)
    duration = end_time - start_time
    duration_obj = datetime.strptime(str(duration), "%H:%M:%S")
    duration_sec = duration_obj.hour * 3600 + duration_obj.minute * 60 + duration_obj.second   
    return duration_sec 
def calculate_duration1(start_time_str, end_time_str, screen_store, time_format='%Y-%m-%d %H:%M:%S'):
    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)
    duration = end_time - start_time
    duration_obj = datetime.strptime(str(duration), "%H:%M:%S")
    duration_sec = duration_obj.hour * 3600 + duration_obj.minute * 60 + duration_obj.second   
    duration_list=[screen_store, duration_sec]
    return duration_list
#Enter the File name here
df = pd.read_csv('testdata.csv')
screen_name = ['Mobile', 'Fiber', 'Music', 'TV', 'Shop', 'UPI', 'Bank', 
               'play&Win', 'Health', 'Movies', 'Events', 'JioStore', 'Pharmacy',
               'Banner1', 'Banner2', 'Banner3', 'Banner4', 'Banner5', 'Banner6', 
               'Banner7', 'Banner8', 'Banner9', 'nonjio_no', 'port_no', 'bookfiber', 
               'getjofiber', 'getprepaid', 'getpostpaid', 'porttojio', 'App kill']
journey_times = []
for index, row in df.iterrows():
    screen = row['Screen']
    time = row['Time']
    if screen in screen_name:
        screen_store = screen
    elif screen == 'App Launch':
        start_time = time
    elif screen == 'App Kill':
        end_time = time
        journey_times.append(calculate_duration1(start_time, end_time, screen_store))
labels = []
values = []
for item in journey_times:
    if item[0] in screen_name:
        labels.append(item[0])
        values.append(item[1])
st.sidebar.title('Navigation')
selection = st.sidebar.radio("", ['Home','Visualizer','Kmean Clustering','About'])
if selection == 'Home':
    st.title('Welcome to Data visualzier for JIO data')
    st.markdown("&nbsp;")
    st.markdown("&nbsp;")
    st.write('This is a data visualizer for Jio data. It provides insights into the user journey on the Jio app. The data is collected from the Jio app and contains information about the screens visited by the users and the time spent on each screen. The visualizer provides different visualizations to help understand the user behavior and preferences. The visualizer includes a time series plot of the time spent on different screens, a bar plot of the app versions per OS distribution, and a line plot of the events per screen. The visualizer also includes a K-means clustering analysis of the screens based on screen time.')
    st.markdown("&nbsp;")
    st.warning('Please select the option from the sidebar to view the visualizations.')
elif selection == 'Visualizer':
    st.title('Jio App User Analysis')
    st.markdown("&nbsp;")
    st.markdown("&nbsp;")
    option = st.selectbox('Select what you want to see:', ['screen time per section', 'version per OS'], index=0 )
    st.markdown("&nbsp;")
    st.markdown("&nbsp;")
    if option == 'screen time per section':
        st.title('Time Spent on Different Screens')
        st.markdown("&nbsp;")
        for screen in screen_name:
            screen_times = []
            start_time = None
            for index, row in df.iterrows():
                if row['Screen'] == screen:
                    screen_store = screen
                    if start_time is None:
                        start_time = row['Time']
                elif row['Screen'] == 'App Kill' and start_time is not None:
                    end_time = row['Time']
                    duration_sec = calculate_duration(start_time, end_time, screen_store)
                    screen_times.append(duration_sec)
                    start_time = None
            if screen_times:
                plt.figure(figsize=(12, 8))
                plt.hist(screen_times, bins=20, color='skyblue', edgecolor='black')
                plt.xlabel('Time (seconds)')
                plt.ylabel('Frequency')
                plt.title(f'Time spent on {screen}')
                plt.grid(axis='y')
                plt.tight_layout()
                st.title(f'Time spent on {screen}')
                st.pyplot(plt, clear_figure=True)
                st.markdown("&nbsp;")
            else:
                print(f"No data found for {screen}.")
    elif option == 'version per OS':
        st.title('App versions per OS distribution')
        os_app_count = df.groupby(['OS', 'App Version'])['Customer ID'].nunique().reset_index()
        pivot_table = os_app_count.pivot(index='OS', columns='App Version', values='Customer ID')
        fig, ax = plt.subplots(figsize=(10, 6))
        pivot_table.plot(kind='bar', stacked=True, ax=ax)
        plt.title('Number of users per OS per app version')
        plt.xlabel('OS')
        plt.ylabel('Number of Users')
        plt.legend(title='App Version')
        plt.grid(axis='y')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig, clear_figure=True)
        for os_val in pivot_table.index:
            percentages = pivot_table.loc[os_val] / pivot_table.loc[os_val].sum() * 100
            fig, ax = plt.subplots()
            percentages.plot(kind='pie', autopct='%1.1f%%', ax=ax)
            ax.set_title(f'Percentage of app versions for {os_val}')
            ax.set_ylabel('')
            plt.tight_layout()
            st.markdown("&nbsp;")
            st.markdown("&nbsp;")
            st.pyplot(fig, clear_figure=True)
elif selection == 'Kmean Clustering':
    st.title('Applying Kmean Clustering on Data')
    st.markdown("&nbsp;")
    st.markdown("&nbsp;")
    screen_names = [item[0] for item in journey_times]
    screen_times = [item[1] for item in journey_times]
    X = [[time] for time in screen_times]
    k = 3
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)
    cluster_labels = kmeans.labels_
    plt.figure(figsize=(10, 6))
    for cluster_label in range(k):
        cluster_data = [journey_times[i] for i, label in enumerate(cluster_labels) if label == cluster_label]
        cluster_names = [data[0] for data in cluster_data]
        cluster_times = [data[1] for data in cluster_data]
        plt.scatter(cluster_names, cluster_times, label=f'Cluster {cluster_label + 1}')
    plt.title('K-Means Clustering of Screens based on Screen Time')
    plt.xlabel('Screen')
    plt.ylabel('Screen Time (seconds)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt, clear_figure=True)
    st.markdown("&nbsp;")
    st.title('Cluster Analysis')
    st.markdown("&nbsp;")
    st.subheader('Cluster 1')
    st.markdown("&nbsp;")
    st.write('Screens in Cluster 1:')
    st.write('are the screen which get users for more duration')
    st.write('which indicate that they spend more time on these screens')
    st.markdown("&nbsp;")
    st.subheader('Cluster 2')
    st.markdown("&nbsp;")
    st.write('Screens in Cluster 2:')
    st.write('are the screen which get users for moderate duration')
    st.write('which indicate that they spend time on these screens just for work and also explore other things')
    st.markdown("&nbsp;")
    st.subheader('Cluster 3')
    st.markdown("&nbsp;")
    st.write('Screens in Cluster 3:')
    st.write('are the screen which get users for least duration')
    st.write('which indicate that they spend time on these screens just for work and nothing else')
    st.write('These screens can get the modal for checking out other screens as well')
elif selection == 'About':
    st.title('About')
    st.markdown("&nbsp;")
    st.markdown("&nbsp;")
    st.write('This is a data visualizer for Jio data. It provides insights into the user journey on the Jio app. The data is collected from the Jio app and contains information about the screens visited by the users and the time spent on each screen. The visualizer provides different visualizations to help understand the user behavior and preferences. The visualizer includes a time series plot of the time spent on different screens, a bar plot of the app versions per OS distribution, and a line plot of the events per screen. The visualizer also includes a K-means clustering analysis of the screens based on screen time.')


    #-Rishit Jain