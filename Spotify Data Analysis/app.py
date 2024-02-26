from flask import *
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime as dt


# With Classes
class using_streams:
    dataset_path = ""
    def __init__(self,dataset_path):
        self.dataset_path = dataset_path
        self.data1 = pd.read_csv(dataset_path)
        # Sort Values by stream in descending Order
        self.data1 = self.data1.sort_values('streams',ascending = False)
        self.data1 = self.data1.reset_index() #allocates the index
    # Returns Top 10 Tracks
    def top_10(self):
        # Convert Series to Dataframe because .head() represents series
        top_10_tracks = pd.DataFrame(self.data1.head(10))
        track_name = []
        streams = []
        dict1 = {}
        for index,row in top_10_tracks.iterrows():
            track_name.append(row['track_name'])
            streams.append(row['streams'])
        dict1['track_name'] = track_name
        dict1['streams'] = streams
        
        # use ['key in dict']['item in list'] to retrieve the item in list inside key of dict
        return dict1
    
    def top_1(self):
         top_1_track = pd.DataFrame(self.data1.head(1))
         top_1_track = top_1_track.iloc[0].to_dict() #Convert the values to perfect Dictionary
         return  top_1_track
          
    def all_tracks(self):
         all_tracks = self.data1['track_name']
         all_tracks_list = all_tracks.iloc[:].to_list()
         return all_tracks_list
         
    def all_artists(self):
        all_artists = self.data1['artist(s)_name']
        all_artists_list = all_artists.iloc[:].to_list()
        return all_artists
                
    def get_track_details(self,track_name):
        
        index_of_track = self.data1.index[self.data1['track_name']==track_name].to_list()
        print(index_of_track)
        if len(index_of_track) >0:
            record_dict = self.data1.iloc[index_of_track[0]].to_dict()
            return record_dict
        else:
            return "Track Not Found"
             

app = Flask(__name__)

using_streams1 = using_streams("Spotify Data Analysis/static/res/dataset2023.csv")

@app.route("/top_tracks")
def top_tracks():
    return using_streams1.top_10()

@app.route('/top1')
def top_1_tracks():
    return using_streams1.top_1()

@app.route("/all_tracks")
def tracks_list():
    return using_streams1.all_tracks()

@app.route('/get_track')
def get_track_details():
    return using_streams1.get_track_details("vampire")

@app.route('/search_song',methods=['GET','POST'])
def search_song():
    if request.method =='POST':
        song_name = request.form['s_song']
        song_details = using_streams1.get_track_details(song_name)
        top10 = using_streams1.top_10()
        tracks = top10['track_name']
        streams = top10['streams']
        all_tracks = using_streams1.all_tracks()
        return render_template('index.html', top1 = song_details, tracks= tracks,streams=streams,all_tracks=all_tracks,song_name = song_name)

@app.route('/get_song', methods=['GET','POST'])
def get_song():
    if request.method == 'POST':
        song_name = request.form['get_val']
        song_details = using_streams1.get_track_details(song_name)
        top10 = using_streams1.top_10()
        tracks = top10['track_name']
        streams = top10['streams']
        all_tracks = using_streams1.all_tracks()
    return render_template('index.html', top1 = song_details, tracks= tracks,streams=streams,all_tracks=all_tracks)

@app.route("/bst_songs",methods=['GET','POST'])
def bst_songs():
    return index()


@app.route("/")
def index():
    top1 =  using_streams1.top_1()
    top10 = using_streams1.top_10()
    tracks = top10['track_name']
    streams = top10['streams']
    all_tracks = using_streams1.all_tracks()
    return render_template('index.html',top1 = top1 , tracks = tracks,streams = streams,all_tracks = all_tracks)

@app.route("/area")
def hello():
    var1 = pd.DataFrame(dataset())
    artist_name = []
    for i,row in var1.iterrows():
        artist_name.append(row['artist(s)_name'])
    return artist_name
 
   
       
    
if __name__ == '__main__':
    app.run(debug=True)