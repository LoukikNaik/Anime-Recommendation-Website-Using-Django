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
    anime=open("./data.txt", "r")
    anime_data=anime.read()
    anime.close()
    data=pd.read_csv('anime.csv')
    def get_index_from_title(title):
            title=title.replace(" ","")
            title=title.lower()
            i=0
            for name in data['Name']:
                k=name.replace(" ","")
                k=k.lower()
                if title in k:
                    return i
                i+=1
            return -1
    
    user_likes=request.GET['Anime']
    str2=anime_data.split("\n")
    k=get_index_from_title(user_likes)
    str3=str2[k][1:-1].split("', ")
    list1=[]
    for i in str3:
        s=i[1:]
        list1.append(s)
    return render(request,'result.html',{'ans':list1})