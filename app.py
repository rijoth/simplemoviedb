from flask import Flask, render_template, redirect, url_for, request
import requests
import json
import random
#flask app
app = Flask(__name__)
#secret key
app.secret_key='lleh;on;si;ereth' #use ur custom key 

#API Key of OMDB
API_KEY = '' #get from omdb

#choose between some random names
tmpnames = ['neram', 'Bhaag', 'pyar', 'time', 'man', 'knight', 'samay']
mv_name = random.choice(tmpnames)
#Dummy info below but don't delete because it may cause issues because its used by a below function as default values
url = "http://www.omdbapi.com/?s=%s&plot=full&apikey=%s" % (mv_name, API_KEY)
response = requests.get(url)
data = json.loads(response.text) 
infos = data['Search']
vlen = len(infos) 

#index page route
@app.route('/')
def index(): 
    url = "http://www.omdbapi.com/?s=%s&plot=full&apikey=%s" % (mv_name, API_KEY)
    response = requests.get(url)
    data = json.loads(response.text) 
    infos = data['Search']
    return render_template('index.html', vlen = vlen ,infos=infos)

@app.route('/search', methods = ['POST', 'GET'])
def search():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        print(movie_name) #debugging purpose 
        if movie_name == "":
            return redirect(url_for('error'))
        else:
            return redirect(url_for('movie', name=movie_name))
    
#get the movie details using JSON
@app.route('/movie/<name>')
def movie(name):
    #print("Entering movie func") #debug
    url = "http://www.omdbapi.com/?s=%s&plot=full&apikey=%s" % (name, API_KEY)
    response = requests.get(url)
    data = json.loads(response.text)
    movies = data['Search']
    mlen = len(movies)
    #print(movies)

    # title = data['Title']
    # director = data['Director']
    # Writer = data['Writer']
    # released = data['Released']
    # Ratings = data['Ratings'][0]['Value']
    # plot = data['Plot']
    # image = data['Poster']
    # language = data['Language']
    # country = data['Country']
    # genre = data['Genre']
    # awards = data['Awards']
    # runtime = data['Runtime']
    # stype = data['Type']
    return_type = data['Response']
    if return_type == "False":
        got_data = False
    else:
        got_data = True
    
    return render_template('index.html', mlen = mlen, movies=movies, vlen=vlen, infos=infos, got_data=True)
    #return render_template('index.html', title=title, plot=plot, image=image, got_data=got_data, director = director, writer=Writer, rating=Ratings, released=released, language=language, country=country, genre=genre, awards=awards, runtime=runtime, stype = stype, vlen=vlen, infos=infos)

@app.route('/details/<name>/<year>')
def details(name,year):
    url = "http://www.omdbapi.com/?t=%s&plot=full&y=%s&apikey=%s" % (name,year, API_KEY)
    response = requests.get(url)
    data = json.loads(response.text)
    title = data['Title']
    director = data['Director']
    Writer = data['Writer']
    released = data['Released']
    Ratings = data['Ratings'][0]['Value']
    plot = data['Plot']
    image = data['Poster']
    language = data['Language']
    country = data['Country']
    genre = data['Genre']
    awards = data['Awards']
    runtime = data['Runtime']
    stype = data['Type']
    year = data['Year']
    return_type = data['Response']
    if return_type == "False":
        got_data = False
    else:
        got_data = True
    
    return render_template('details.html', title=title, plot=plot, image=image, got_data=got_data, director = director, writer=Writer, rating=Ratings, released=released, language=language, country=country, genre=genre, awards=awards, runtime=runtime, stype = stype,year=year, vlen=vlen, infos=infos)


#Error page
@app.route('/Error')
def error():
    return render_template('error.html')

#this was for test purpose only probably will delete in future
@app.route('/page/<title>')
def page(title):
    url = "http://www.omdbapi.com/?t=%s&plot=full&apikey=%s" % (title, API_KEY)
    response = requests.get(url)
    data = json.loads(response.text)
    title = data['Title']
    plot = data['Plot']
    image = data['Poster']
    return render_template('index.html', title=title, plot=plot, image=image)

if __name__ == '__main__':
    app.run()

