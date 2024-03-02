from flask import *
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns

  
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
    
    def heat_map(self):
        covar_matrix = self.data1.select_dtypes(exclude = 'object').drop(['artist_count','released_month','released_day','in_spotify_charts','in_apple_charts','in_deezer_charts'],axis=1).corr(method = 'pearson').corr(method='pearson')
        plt.figure(figsize = (25,15))
        sns.set(font_scale=0.6)
        plt.figure(dpi=600)
        sns.heatmap(covar_matrix,vmax = 1, vmin=-1, annot=True)
        plt.savefig("Spotify Data Analysis/static/images/plots/covar.png",format= 'png')
        plt.close()
        
    def get_cols_covar(self):
        data1 = self.data1.select_dtypes(exclude = 'object').drop(['artist_count','released_month','released_day','in_spotify_charts','in_apple_charts','in_deezer_charts'],axis=1).corr(method = 'pearson')
        dict1 = data1.to_dict()
        keys = []
        for i in dict1.keys():
            keys.append(i)
        return keys  
             
    def get_covar_val(self,val1,val2):
        covar_matrix = self.data1.select_dtypes(exclude = 'object').drop(['artist_count','released_month','released_day','in_spotify_charts','in_apple_charts','in_deezer_charts'],axis=1).corr(method = 'pearson').corr(method='pearson')
        val = covar_matrix[val1][val2]
        self.get_relationship_plots(val1,val2)
        return val
    
    def get_relationship_plots(self,val1,val2):
        data_streams = self.data1.select_dtypes(exclude = 'object').drop(['artist_count','released_month','released_day','in_spotify_charts','in_apple_charts','in_deezer_charts'],axis=1)
        plt.figure(dpi=600)
        plt.title("Line Plot")
        sns.lineplot(x=data_streams[val1],y=data_streams[val2])
        plt.savefig('Spotify Data Analysis/static/images/plots/rel_line1.png')
        plt.close()
        
        plt.figure(dpi=600)
        fix,ax = plt.subplots(figsize=(17,6))
        plt.title("Bar Plot")
        sns.barplot(x=data_streams[val1],y=data_streams[val2])
        plt.savefig('Spotify Data Analysis/static/images/plots/rel_bar1.png')
        plt.close()
        
        plt.figure(dpi=600)
        plt.title("Reg Plot")
        sns.regplot(x=data_streams[val1],y=data_streams[val2])
        plt.savefig('Spotify Data Analysis/static/images/plots/rel_reg1.png')
        plt.close()
             
        plt.figure(dpi=600)
        plt.title("Joint Plot")
        sns.jointplot(x=data_streams[val1],y=data_streams[val2], kind='scatter')
        plt.savefig('Spotify Data Analysis/static/images/plots/rel_joint1.png')
        plt.close()
        
        plt.figure(dpi=600)
        plt.title("Scatter Plot")
        sns.scatterplot(x=data_streams[val1],y=data_streams[val2])
        plt.savefig('Spotify Data Analysis/static/images/plots/rel_scatter1.png')
        plt.close()
        
        plt.figure(dpi=600)
        plt.title("Rel Plot")
        sns.relplot(x=data_streams[val1],y=data_streams[val2],legend="auto")
        plt.savefig('Spotify Data Analysis/static/images/plots/rel_rel1.png')
        plt.close()
        
        plt.figure(dpi=600)
        plt.title("KDE Plot")
        sns.kdeplot(data = data_streams, x = val1,y=val2)
        plt.savefig('Spotify Data Analysis/static/images/plots/rel_kde1.png')
        plt.close()
        # Distribution Plots
    def univariate_plots(self,val1):
        data_streams = self.data1.select_dtypes(exclude = 'object').drop(['artist_count','released_month','released_day','in_spotify_charts','in_apple_charts','in_deezer_charts'],axis=1)
         # Hist Plot
        plt.figure(dpi=600)
        sns.histplot(data = data_streams[val1],kde= True)
        plt.savefig('Spotify Data Analysis/static/images/plots/univariate/uni_hist.png')
        plt.close()
        
        # KDE Plot
        plt.figure(dpi=600)
        sns.kdeplot(data=data_streams, x=val1,common_grid=True)
        plt.savefig('Spotify Data Analysis/static/images/plots/univariate/uni_KDE.png')
        plt.close()
        
        # PIE Plot
        x = data_streams[val1].value_counts() 
        plt.figure(dpi = 600)
        plt.pie(x.values, 
        labels=x.index, 
        autopct='%1.1f%%') 
        plt.savefig('Spotify Data Analysis/static/images/plots/univariate/uni_PIE.png')
        plt.close()
        
        # Count Plot
        plt.figure(dpi=800)
        fig,ax = plt.subplots(figsize=(25,6))
        sns.countplot(data_streams,x=val1)
        plt.savefig('Spotify Data Analysis/static/images/plots/univariate/uni_count.png')
        plt.close()
        
        
             
             
             
             
             
             
             
             

app = Flask(__name__)

using_streams1 = using_streams("Spotify Data Analysis/static/res/dataset2023.csv")





# For INDEX PAGE
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
    using_streams1.heat_map()
    return render_template('index.html',top1 = top1 , tracks = tracks,streams = streams,all_tracks = all_tracks)

@app.route("/area")
def hello():
    var1 = pd.DataFrame(dataset())
    artist_name = []
    for i,row in var1.iterrows():
        artist_name.append(row['artist(s)_name'])
    return artist_name
 
# ^ For Index Page
       
    #For Analysis Page 2023
    
@app.route('/get_covar_percentage',methods=['POST','GET'])
def get_covar_percentage():
    if request.method == 'POST':
        val1 = request.form['covar_sel1']
        val2 = request.form['covar_sel2']
        val = using_streams1.get_covar_val(val1,val2)
        covar_keys = using_streams1.get_cols_covar()
        # Calculate Percentage
        covar_percentage = int((((val-(-1))/2)*100))
        # Return only two digits after decimal point
        val3 = (int(val*100))/100
        
        return render_template('analysis2023.html',val1 =val1 ,val2 = val2, val =val,covar_keys=covar_keys,covar_percentage = covar_percentage,val3 = val3)


@app.route("/analysis_2023",methods=['GET','POST'])  
def analysis_2023():
    covar_keys = using_streams1.get_cols_covar()
    
    return render_template("analysis2023.html",covar_keys=covar_keys )
       
@app.route('/sel_covar_analysis')
def sel_covar_analysis():
    covar_keys = using_streams1.get_cols_covar()
    
    return render_template('covar_rel.html',covar_keys=covar_keys)
       
@app.route('/dist_analysis2023',methods=['GET','POST'])
def dist_analysis2023():
    if request.method == 'POST':
        covar_keys = using_streams1.get_cols_covar()
        return render_template('distanalysis2023.html',covar_keys=covar_keys)      
       
@app.route('/get_uni_analysis',methods=['GET','POST'])
def get_uni_analysis():
    if request.method == 'POST':
        val1 = request.form['uni_btn1']
        using_streams1.univariate_plots(val1)
        covar_keys = using_streams1.get_cols_covar()
        return render_template('distanalysis2023.html',covar_keys=covar_keys,val1 = val1)      
       
       
       
       
    
if __name__ == '__main__':
    app.run(debug=True)