import sqlite3


def getSongInfo(results):
    info = []
    for _, item in enumerate(results['items']):
       info.append([item['id'], 
                    item['name'], 
                    item['artists'][0]['name'], 
                    item['album']['images'][0]['url']])  
      
    return info

def getSpotifyInfo():
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    sc = "user-top-read, playlist-modify-public"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = 'b6deea05a49345a88e35cdcf4d45a438',
                                                        client_secret = 'c41b00cdf04b4f308671e58236f9f25d',
                                                        redirect_uri = 'https://localhost:5500',
                                                        scope=sc))
   
    basicInfo = getSongInfo(sp.current_user_top_tracks(50, 0, "short_term")) # LIST OF LIST WITHOUT AUDIO FEATURES
    fullInfo = []

    for track in basicInfo:
      audioFeatures = sp.audio_features(track[0])[0]
      track += [audioFeatures['danceability'], 
                       audioFeatures['energy'], 
                       audioFeatures['acousticness'], 
                       audioFeatures['instrumentalness'], 
                       audioFeatures['tempo']]
      fullInfo.append(tuple(track))
    

    return fullInfo
  

def executeSQL(command, t = ()):
  connection = sqlite3.connect("connectune.db") # create database
  cursor = connection.cursor()

  fetched = []

  if (t == ()):
    fetched = cursor.execute(command).fetchall()
  else:
    fetched = cursor.execute(command, t).fetchall()

  connection.commit()
  connection.close()
  
  return fetched


def createDefaultTables():
  executeSQL("""
  CREATE TABLE IF NOT EXISTS Accounts(
    Username VARCHAR(12) COLLATE BINARY,
    Password VARCHAR(12) COLLATE BINARY,
    DisplayName VARCHAR(12),
    PRIMARY KEY(Username));
  """)

  executeSQL("""
  CREATE TABLE IF NOT EXISTS Connections(
    Username1 VARCHAR(12) COLLATE BINARY,
    Username2 VARCHAR(12) COLLATE BINARY,
    FOREIGN KEY(Username1) REFERENCES Accounts(Username),
    FOREIGN KEY(Username2) REFERENCES Accounts(Username),
    PRIMARY KEY(Username1, Username2));
  """)

  executeSQL("""
  CREATE TABLE IF NOT EXISTS Songs(
    SongID VARCHAR(50),
    SongName VARCHAR(300),
    Artist VARCHAR(300),
    AlbumArtURL VARCHAR(300),
    Danceability FLOAT,
    Energy FLOAT,
    Acousticness FLOAT,
    Instrumentalness FLOAT,
    Tempo FLOAT,
    PRIMARY KEY(SongID));
  """)

  executeSQL("""
  CREATE TABLE IF NOT EXISTS RecentSongs(
    Username VARCHAR(12),
    SongID VARCHAR(50),
    FOREIGN KEY (Username) REFERENCES Accounts(Username),
    FOREIGN KEY (SongID) REFERENCES Songs(SongID),
    PRIMARY KEY(Username, SongID));
  """)

def validateAlnum(string, lngth=12):
  if string.isalnum() and len(string) <= lngth:
    return True
  else:
    return False

def connectuneRegister (username, password, displayName):  
  if not (validateAlnum(username) and validateAlnum(password), validateAlnum(displayName)):
    return False
  if executeSQL( f"SELECT Username FROM Accounts WHERE Username = '{username}';") != []:
    print(f"Couldnt register {username}, {password}, {displayName}")
    return False
  else:
    executeSQL(f"""
    INSERT INTO Accounts (Username, Password, DisplayName) 
    VALUES ('{username}', '{password}', '{displayName}');
    """)
    print(f"Welcome!! Registered {username}, {password}, {displayName}")
    return True

def connectuneLogin (username, password):
  if executeSQL(f"""
  SELECT * FROM Accounts
  WHERE Username = '{username}' 
  AND Password = '{password}';
  """) == []:
    print("Couldn't log in "+username)
    return False # error!!!! fix this lols this person doesnt exist
  else:
    print("Successfully logged in! Welcome back "+ username)
    return True

def makeFriends (username1, username2):
  if username1 == username2:
    print("Same users? Not cool")
    return False

  check = executeSQL(f"""
  SELECT * FROM Accounts 
  WHERE Username = '{username1}' 
  OR Username = '{username2}';
  """)
  
  if check == [] or len(check) != 2:
    print("One or more of the users dont exist. what the flip")
    return False
  elif executeSQL(f"""
  SELECT Username1 FROM Connections 
  WHERE (Username1 = '{username1}' AND Username2 = '{username2}') 
  OR (Username1 = '{username2}' AND Username2 = '{username1}');
  """):
    print("We're already friends, nice!")
    return False
  else:
    executeSQL(f"""
    INSERT INTO Connections (Username1, Username2) 
    VALUES ('{username1}', '{username2}');
    """)
    print(f"{username1} and {username2} are now friends!!!!!")
    return True

def populateSongTables(username, songs):
  executeSQL(f"DELETE FROM RecentSongs WHERE Username = '{username}';")

  for (songID, song, artist, url, danceability, energy, acousticness, instrumentalness, tempo) in songs:
    # add all new songs found into the songs database
    if (executeSQL(f"SELECT * FROM Songs WHERE SongID = '{songID}';") == []):
      executeSQL('''INSERT INTO Songs (SongID, SongName, Artist, AlbumArtURL, Danceability, Energy, Acousticness, Instrumentalness, Tempo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                 (songID, song, artist, url, danceability, energy, acousticness, instrumentalness, tempo))
      executeSQL(f"""
      INSERT INTO RecentSongs (Username, SongID) 
      VALUES ('{username}', '{songID}');
      """)


def generateDescription(songID):
  descs = ["danceable", "energetic", "acoustic", "instrumental", "tempo"]
  audioFeatures = executeSQL(f"""SELECT Danceability, Energy, Acousticness, Instrumentalness, Tempo FROM Songs 
             WHERE SongID = '{songID}';""")[0]
  
  fullDesc = ""
  audioFeatures = [float(i) for i in audioFeatures]
  zipped = zip(descs, audioFeatures)
  for d, f in zipped:
    if d != "tempo":
      if f > 0.7:
        fullDesc += " very " + d + ","
      elif f > 0.5:
        fullDesc += d + ","
      elif f > 0.3:
        fullDesc += " slightly " + d + ","
      else:
        fullDesc += " not-" + d + ","
    else:
      if f > 210:
        fullDesc += " beat fast as possible,"
      elif f > 180:
        fullDesc += " extremely fast beat,"
      elif f > 120:
        fullDesc += " beat fast and lively"
      elif f > 100:
        fullDesc += " moderate speed"
      else:
        fullDesc += " slow song"

  return fullDesc 


  def exportPlaylist(name, description, songs):
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    sc = "user-top-read, playlist-modify-public"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = 'b6deea05a49345a88e35cdcf4d45a438',
                                                        client_secret = 'c41b00cdf04b4f308671e58236f9f25d',
                                                        redirect_uri = 'https://localhost:5500',
                                                        scope=sc))
    
    userID = sp.current_user()['id']
    playlist = sp.user_playlist_create(userID, name, True, False, description)
    playlistID = playlist['id']
    sp.user_playlist_add_tracks(playlistID, songs)

  def search(name, artist):
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    sc = "user-top-read, playlist-modify-public"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = 'b6deea05a49345a88e35cdcf4d45a438',
                                                        client_secret = 'c41b00cdf04b4f308671e58236f9f25d',
                                                        redirect_uri = 'https://localhost:5500',
                                                        scope=sc))
    result = sp.search(q="artist:" + artist + " track:" + name, type="track")
    
    return result[0]['id']
    

    



#createDefaultTables()
#connectuneRegister("pee", "poo", "d")

#if(connectuneLogin("pee", "poo")):
#  user = "pee"
 # populateSongTables(user, getSpotifyInfo())

#print(executeSQL("SELECT * FROM Songs"))
#print(executeSQL("SELECT * FROM Accounts"))
#print(executeSQL("SELECT * FROM Connections"))
#print(executeSQL("SELECT * FROM RecentSongs"))


