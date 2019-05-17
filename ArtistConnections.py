import random
import Graph
import operator  # I used this to derive the max key and value in methods involving dictionaries
from SongLibrary import Song
from Graph import Vertex
import collections


class ArtistConnections:

    def __init__(self):
        self.vertList = {}  # initializtion of vertlist used to store the vertices
        self.numVertices = 0  # iniatiliztion of the number of vertices
        self.count = 0

    """
    Load the artist connections graph based on a given song database
    Add the edges based on the last column of the collaborative artists 

    """

    def load_graph(self, songLibaray):
        file = open(songLibaray, 'r')  # opens file in a readable format
        lines = file.readlines()  # gets all the lines of the dile
        count = 0  # Variable used to insure that all the lines have been read
        for line in lines:  # iterates through the text lines
            count += 1
            self.insertRecord(line)  # calls the function which will add to the graph for each song/line

        print("finish load data " + str(count))  # Tells user the total number of lines read
        return self.numVertices  # returns the number of vertices

    """
    Return song libary information
    """

    def graph_info(self):  # prints the number of vertices in the graph
        return "Vertex Size: " + str(self.numVertices)

    def insertRecord(self, record):  # recieves a line of the text file and is used to build the graph
        tokens = record.split(',')  # splits the line via the split method
        if len(tokens) != 6:  # check regarding whether the line has 6 commas
            print('Incorrect Song Record')
        song = tokens[1]  # assings the song
        artist = tokens[2]  # assings the artist
        neighbors = tokens[5][:len(tokens[5]) - 1].split(';')  # via the split method again, it creates a
        #  list of coArists AKA neighbors

        for i in range(0, len(neighbors)):  # This for loop checks if an artist is listed in the list neighbors
            # this prevents repeated edges when creating the graph
            if artist in neighbors:
                neighbors.remove(artist)

        currentVert = None  # inializion of the current vertice
        if artist in self.vertList:  # checks if artist is in the the graph
            currentVert = self.vertList[artist]  # the vertice is set to the artist at that postion
        else:
            currentVert = Vertex(artist)  # creation of vertex
            self.vertList[artist] = currentVert  # Vertex is conneccted to the node
            self.numVertices += 1  # number of vertices is incremented
        ## insert info  for this artist

        arr = []
        currentVert.addsong(song)  # the song is added to the array of songs in the Graph file
        for nb in neighbors:  # iterates through the array neigbors and connects the neighbors together bidirectionally
            nbVert = None
            if nb in self.vertList:
                nbVert = self.vertList[nb]
            else:
                nbVert = Vertex(nb)
                self.vertList[nb] = nbVert
                self.numVertices += 1

            currentVert.addNeighbor(nbVert)
            nbVert.addNeighbor(currentVert)

            # print(currentVert).
            # print(nbVert)

    """
    Search the information of an artist based on the artist name
    Return a tuple (the number of songs he/she wrote, the collaborative artist list)

    """

    def search_artist(self, artist_name):
        numSongs = 0;
        artistLst = []
        dict = {}
        arr = []
        sum = 0
        for i in self.vertList:  # searches through every node
            if self.vertList[
                i].id == artist_name:  # when found the numSongs is incremented via the number of songs the
                # artist has worked on
                numSongs += len(self.vertList[i].songs)
                artistLst = self.vertList[i].coArtists  # the dictionary coArtists is assigned to a variable
        for key in artistLst.keys():  # for loop dervies an array of  keys from the dictioary
            arr.append(key.id)
        arr.sort()
        return numSongs, arr  # returns the number of songs and coArtists

    """
    Return a list of two-hop neighbors of a given artist
    """

    def min_search(self, artist_name):  # Helper method that only returns the array of coArtists
        artistLst = []
        dict = {}
        arr = []
        sum = 0
        for i in self.vertList:
            if self.vertList[i].id == artist_name:
                artistLst = self.vertList[i].coArtists
        for key in artistLst.keys():
            arr.append(key.id)
        arr.sort()
        return arr

        return d

    def min_searchKeys(self, artist_name):  # Helper method that returns the max value dictionary
        artistLst = []
        dict2 = {}
        arr = []
        arr2 = None
        j = 0
        sum = 0
        for i in self.vertList:  # Searches throgh vertList
            if self.vertList[i].id == artist_name:
                artistLst = (self.vertList[i].coArtists)  # assigns dictionary of coArtists to a variable
        for key in artistLst.keys():  # derives a list of keys from the dictionary
            arr.append(key.id)
        arr2 = list(artistLst.values())  # creates an array of values
        dict2 = dict(zip(arr, arr2))  # creates a dictionary by ziping the array of keys and the array of values
        maxKey = max(dict2.items(), key=operator.itemgetter(1))[0]  # derives the Key with the max value
        maxvalue = max(dict2.values())  # dervies the max value in the dictionary
        dict3 = ((maxKey, maxvalue))  # creates a dictionary with the max key and the max value
        # print(dict2)

        return dict3  # returns dictionary

    def find_new_friends(self, artist_name):
        two_hop_friends = []
        arr = []
        arr2 = []
        arr3 = []
        arr4 = []
        for i in self.vertList:
            if self.vertList[i].id == artist_name:
                artistLst = self.vertList[i].coArtists  # assings the coArtists dictionary to a variable
        for key in artistLst.keys():  # Derives array of keys from the dictionary
            arr.append(key.id)
            arr.sort()
        for j in range(0, len(arr)):  # searches through the array again and appends each array returned by min Search
            arr2.append(self.min_search(arr[j]))  # appends array returned by minSearch

            for k in range(0, len(arr2)):  # converts array into a 2D array
                arr3.append(arr2[k])
        arr3.sort()
        for l in range(0, len(arr3)):  # The nested for loop serves to convert the 2D array into a 1D array
            for m in range(0, len(arr3[l])):
                arr4.append(arr3[l][m])
        arr4.sort()
        arr.append(artist_name)

        two_hop_friends = list(set(arr4) - set(arr))  # removes duplicates from the ccode
        two_hop_friends.sort()  # sorts the list to be in alphebetical order

        #
        # Write your code here
        #
        return two_hop_friends  # returns the array of 2 hops

    """
    Search the information of an artist based on the artist name

    """

    def recommend_new_collaborator(self,
                                   artist_name):  # find the best collaborators overall organize them by max number of songs
        artist = ""
        numSongs = 0
        count = 0
        arr = []
        coList = []
        result = {}
        b = {}
        arr2 = []
        arr = self.find_new_friends(artist_name)  # gets array from the search method
        coList = self.min_search(artist_name)
        # print(arr2[i])
        for i in range(0, len(coList)):
            # print(self.min_searchKeys(coList[i]))
            arr2.append(self.min_searchKeys(coList[i]))  # Creates an array of dictionarys with the max Key and values
            # print(arr2[i])
        a = dict((x, y) for x, y in arr2)  # itertes through the dictioanary and pulls out the max dictinary
        artist = max(a.items(), key=operator.itemgetter(1))[0]  # derives the max key
        numSongs = max(a.values())  # derives the max value

        return artist, numSongs  # returns the max key and value

    """
    Search the information of an artist based on the artist name

    """

    # Djkstra's print out a dictionary for all vertices
    # Distance is the number of hops, number of hops is 1
    # have to import a unch of stuff
    def shortest_path(self, artist_name):
        path = {}
        blist = []
        store = []
        alist = self.min_search(artist_name) # gets first hops hop neighbors
        clist = []
        dlist = []
        elist = []
        flist = []

        for x in alist:# loop that appends to the path
            path[x] = 1
        for i in alist:
            store.append(i)
        while len(alist) > 0:
            next = alist.pop()
            blist += self.min_search(next) # creation of second hop neigbors

        for i in blist:
            if i == artist_name:
                path[i] = 0
            if i not in path: # will append to the path if not already there
                path[i] = 2
                store.insert(0, i)
        while len(blist) > 0:
            next = blist.pop()
            clist += self.min_search(next) # creation of 3rd hop neigbors

        for i in clist:
            if i == artist_name:
                path[i] = 0
            if i not in path: # appends to path if not already there
                path[i] = 3
                store.insert(0, i)
        while len(clist) > 0:
            next = clist.pop()
            dlist += self.min_search(next) # creation of four hop neighbors
        alist += dlist
        for i in dlist:
            if i == artist_name:
                path[i] = 0
            if i not in path: # appends to path if not already there
                path[i] = 4
                store.insert(0, i)
        while len(dlist) > 0:
            next = dlist.pop()
            elist += self.min_search(next) # creation of 5th hop neigbors
        for i in elist:
            if i == artist_name:
                path[i] = 0
            if i not in path: # appends to path if not already
                path[i] = 5

        '''for i in range(0,len(elist)):
            flist=list(set(flist)-set(elist))
            flist+=self.min_search(elist[i])

        for i in flist:
            if i == artist_name:
                path[i]=0
            if i not in path:
                path[i]=6'''

        return path


# WRITE YOUR OWN TEST UNDER THAT IF YOU NEED
if __name__ == '__main__':
    artistGraph = ArtistConnections()
    artistGraph.load_graph('TenKsongs_proj2.csv')
    # artistGraph.shortest_path('Mariah Carey')
    # print(artistGraph.search_artist("Charlie Peacock"))
    # print(artistGraph.sdf("Mariah Carey"))
    # print(artistGraph.search_artist('Jean-Jacques Goldman;Edith Lefel;Malavoi'))

    # print(artistGraph.find_new_friends("Mariah Carey"))
    print(artistGraph.shortest_path('Mariah Carey'))

    # ArtistConnections.generate_data("TenKsongs_proj2.csv")
