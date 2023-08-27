from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extract = URLExtract()


def fetch_stat(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    no_msg = df.shape[0]
    word = []
    for msg in df['message']:
        word.extend(msg.split())
    no_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]
    link = []
    for msg in df['message']:
        link.extend(extract.find_urls(msg))

    return no_msg, len(word), no_media_msg, len(link)


def busy_user(df):
    x = df['user'].value_counts()
    dd=round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percentage'})
    return x,dd
def word_cloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep = " "))
    return df_wc
def common_words(selected_user, df):
    f = open('stop.txt', 'r')
    stop = f.read()


    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop:
                words.append(word)

    common_df = pd.DataFrame(Counter(words).most_common(20))
    return  common_df
def emoji_total(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis=[]
    for msg in df['message']:
        emojis.extend([c for c in msg if c in emoji.UNICODE_EMOJI['en']])
        emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df
def monthly_time(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+" "+"-"+ str(timeline['year'][i]))
    timeline['time']=time
    return timeline


def daily_time(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()
    return daily_timeline

def weekly_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def monthly_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap