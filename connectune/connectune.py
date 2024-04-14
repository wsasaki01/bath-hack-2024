import sqlite3


def getSongInfo(results):
    info = []
    for _, item in enumerate(results['items']):
       info.append((item['name'], item['artists'][0]['name'], item['id'], item['album']['images'][0]['url']))
    
    return info

def spotipy():
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    sc = "user-top-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = 'b6deea05a49345a88e35cdcf4d45a438',
                                                        client_secret = 'c41b00cdf04b4f308671e58236f9f25d',
                                                        redirect_uri = 'https://localhost:5500',
                                                        scope=sc))

    return getSongInfo(sp.current_user_top_tracks(50, 0, "short_term"))


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

def register (username, password, displayName):  
  if executeSQL( f"SELECT Username FROM Accounts WHERE Username = '{username}';") != []:
    print(f"Couldnt register {username}, {password}, {displayName}")
    return False
    #fix this
  else:
    executeSQL(f"""
    INSERT INTO Accounts (Username, Password, DisplayName) 
    VALUES ('{username}', '{password}', '{displayName}');
    """)
    print(f"Welcome!! Registered {username}, {password}, {displayName}")
    return True


def login (username, password):
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
  for (song, artist, songID, url, danceability, energy, acousticness, instrumentalness) in songs:
    # add all new songs found into the songs database
    if (executeSQL(f"SELECT * FROM Songs WHERE SongID = '{songID}';") == []):
      executeSQL('''INSERT INTO Songs (Username, SongName, Artist, SongID, AlbumArtURL, Time) VALUES (?, ?, ?, ?, ?, ?, ?, ?);''',
                 (songID, song, artist, url, danceability, energy, acousticness, instrumentalness))
    
    if (executeSQL(f"SELECT * FROM RecentSongs WHERE Username = '{username}' AND SongID = '{songID}';") == []):
      executeSQL(f"""
      INSERT INTO RecentSongs (Username, SongID) 
      VALUES ('{username}, {songID}');
      """)
    else:
      executeSQL(f"""
      UPDATE TABLE RecentSongs
      SET SongID = '{songID}'
      WHERE Username = '{username}';
      """)
    
    



createDefaultTables()

print(executeSQL("SELECT * FROM Accounts"))
print(executeSQL("SELECT * FROM Connections"))
print(executeSQL("SELECT * FROM RecentSongs"))
print(executeSQL("SELECT * FROM Songs"))


