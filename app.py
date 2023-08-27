import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import preprocessing,helper
import seaborn as sns

st.sidebar.title("whats-app analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    #st.text(data)
    df = preprocessing.preprocess(data)

    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.remove('Porosh started a call\n3/1/22, 10:49\u202fAM - Samael')
    user_list.remove("Porosh changed this group's icon\n10/17/22, 11:03\u202fPM - piyal")
    user_list.insert(0,'Overall')


    select_user = st.sidebar.selectbox("Show analysis wrt",user_list)


    if st.sidebar.button("Show analysis"):
        no_msg, word, no_media_msg, no_link = helper.fetch_stat(select_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total messages")
            st.title(no_msg)
        with col2:
            st.header("Total words")
            st.title(word)
        with col3:
            st.header("Media shared total")
            st.title(no_media_msg)
        with col4:
            st.header("Total shared links")
            st.title(no_link)

        #busy user
        value_to_remove = 'Porosh started a call\n3/1/22, 10:49\u202fAM - Samael'
        df = df.drop(df[df['user'] == value_to_remove].index)
        val = "Porosh changed this group's icon\n10/17/22, 11:03\u202fPM - piyal"
        df = df.drop(df[df['user'] == val].index)

        if select_user == 'Overall':
            st.header("Most busy user")
            x,dd = helper.busy_user(df)
            fig, ax = plt.subplots()
            col5,col6 = st.columns(2)
            with col5:
                ax.bar(x.index, x.values, color='red')
                st.pyplot(fig)

            with col6:
                st.dataframe(dd)


        #wordCloud
        st.title("Wordcloud")
        df_wc = helper.word_cloud(select_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        common_df = helper.common_words(select_user,df)
        st.title("Most used words")

        fig, ax = plt.subplots()
        ax.barh(common_df[0],common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.dataframe(common_df)


        emoji_df = helper.emoji_total(select_user,df)
        st.title("Most used emojis")
        col7,col8 = st.columns(2)

        with col7:
           st.dataframe(emoji_df)
        with col8:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1],labels=emoji_df[0],autopct="%0.2f")
            st.pyplot(fig)


        timeline = helper.monthly_time(select_user,df)
        st.title('Monthly messages numbers')
        col9,col10 = st.columns(2)


        with col9:
             new_timeline = timeline.drop('time', axis=1)
             #p = new_timeline.groupby(['year', 'month', 'message']).mean().reset_index()
             st.write(new_timeline)

        with col10:
            fig, ax = plt.subplots()
            plt.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        daily_timeline = helper.daily_time(select_user, df)
        st.title('Daily messages numbers')
        col11, col12 = st.columns(2)
        with col11:
            #new_daily = daily_timeline.drop('time', axis=1)

            st.write(daily_timeline)

        with col12:
            fig, ax = plt.subplots()
            plt.plot(daily_timeline['only_date'], daily_timeline['message'], color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Activity Map")
        col13,col14 = st.columns(2)
        with col13:
            st.title("Most busy day")
            busy_day = helper.weekly_activity(select_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)
        with col14:
            st.title("Most busy month")
            busy_month = helper.monthly_activity(select_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='pink')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Heatmap")
        user_heatmap = helper.activity_heatmap(select_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
