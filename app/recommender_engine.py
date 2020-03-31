# -*- coding: utf-8 -*-
import datetime, time
import numpy as np 
import pandas as pd
from bin import *

recommend_threshold = 0.8 #
update_frequency = 60 * 15 # set update frequency to 15 minutes
last_update = '2020-01-01T00:00:00Z' 
wiki = Wiki()
database = Database()
classifier = Classifier(max_features=19000)
ds = pd.read_csv('./data/45_dataset_merged_nodup.csv', encoding='utf-8')
classifier.set_data(ds, ['Economy', 'Entertainment', 'Politics', 'Science and Technology', 'Sports'], test_size=0.01)

while True:
    profiles = database.get_profiles()
    print('Started getting recent pages...')
    try:
        pages = wiki.recentchanges(rclimit=50, rcstart='now', rcend=last_update)
    except:
        print('\nAPI Error :(')
        break
    print('DONE')
    pages = pages.iloc[::-1] # order pages from the oldest to the newest
    last_update = datetime.datetime.utcnow().isoformat() # set current timestamp
    for index, page in pages.iterrows():
        users_interested = []
        prediction = classifier.get_predict_proba(page['summary']) 
        for profile in profiles:
            similarity = classifier.similarity(np.asarray(profile[2:]), prediction['features'][0])
            if similarity >= recommend_threshold:
                users_interested.append(profile[0])
        database.insert_page(page, prediction['label'][::])
        for userid in users_interested:
            database.insert_recommendations(userid, page['pageid'])
    database.commit()
    database.execute(statement='sp_page')
    print('Next update scheduled on : ', datetime.datetime.now() + datetime.timedelta(seconds=update_frequency))
    time.sleep(update_frequency)