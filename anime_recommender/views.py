from django.http import HttpResponse
from django.shortcuts import render
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib 

def home(request):
    return render(request,"home.html")

def result(request):
    anime_data=pd.read_csv('./anime.csv')
    features=["Genres","Type","Source","Producers","Rating"]
    class anime_model:
        def __init__(self):
            print("Model inititalize")
        
        def combine_feature(self,row):
            s=""
            for feature in self.features:
                k=row[feature].split(",")
                for i in k:
                    try:
                        s+=i
                    except:
                        print('Error:',row)
                    s+=" "
            return s

        def fit(self,data,features):
            self.data=data
            self.features=features
            self.data['combined_features']=self.data.apply(self.combine_feature,axis=1)
            cv=CountVectorizer()
            self.count_matrix=cv.fit_transform(self.data['combined_features'])
            self.cosine_sim=cosine_similarity(self.count_matrix)
        
        def get_title_from_index(self,index):
            title=self.data[self.data.index==index]['Name'].values[0]
            return title

        def get_index_from_title(self,title):
            title=title.replace(" ","")
            title=title.lower()
            i=0
            for name in self.data['Name']:
                k=name.replace(" ","")
                k=k.lower()
                if title in k:
                    return i
                i+=1
            return -1
        
        def predict(self,user_likes):
            anime_index=self.get_index_from_title(user_likes)
            list1=[]
            if anime_index==-1:
                return list1
            similar_anime=list(enumerate(self.cosine_sim[anime_index]))
            sorted_similar_anime=sorted(similar_anime,key=lambda x:x[1],reverse=True)
            i=0
            for anime in sorted_similar_anime:
                list1.append(self.get_title_from_index(anime[0]))
                i+=1
                if i==50:
                    return list1
    model=anime_model()
    model.fit(anime_data,features)
    user_likes=request.GET['Anime']
    k=model.predict(user_likes)
    print(k)
    return render(request,'result.html',{'ans':k})