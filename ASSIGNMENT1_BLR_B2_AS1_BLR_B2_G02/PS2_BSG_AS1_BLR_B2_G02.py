# -*- coding: utf-8 -*-
"""
Created on Thu Jul 09 10:22:03 2019

@author: basavaraj
"""

from collections import defaultdict;
import re;
import os;
import sys;

'''
Constants to indicate the Type of node
'''
class NodeType:
    movie = 1;
    actor = 2;

'''
Node Class for storing the Actor and Movie information
name - name of actor or movie
type - Indication for Movie or actor
'''
class Node:
    def __init__(self,name,nodetype):
        self.name = name;
        self.nodetype = nodetype;
    
    def __hash__(self):
        return hash((self.name,self.nodetype));
    
    def __eq__(self,other):
        return (self.name,self.nodetype) == (other.name,other.nodetype);
    
    def __ne__(self,other):
        return not(self==other);
        
'''
Graph implementation for PS2 - Big Screen graph
'''   
class Graph:
    #Initialize empty graph
    def __init__(self):
        self.ActMovGrapgh = defaultdict(list);
        
    '''
    Add Relation between Movies and actors    
    '''
    def addEdge(self,actor,movie):
        if not self.ActMovGrapgh.get(movie) is None:
            if len(self.ActMovGrapgh[movie]) < 2:
                if not actor in self.ActMovGrapgh[movie]:
                    self.ActMovGrapgh[movie].append(actor);
        else :
            self.ActMovGrapgh[movie].append(actor);
        if not movie in self.ActMovGrapgh[actor]:
            self.ActMovGrapgh[actor].append(movie);
    '''
    Dispaying the Movies and actors which stored in graph data structure
    Parameters
        filewrite - write result content to file
    '''
    def displayActMov(self,filewrite):
        # Write to File  outputPS2.txt
        filewrite.write("--------Function displayActMov--------")
        #print("--------Function displayActMov-------- ")
        #Filter actors
        actors = list(filter(lambda actor: actor.nodetype == NodeType.actor,self.ActMovGrapgh.keys()));
        #Filter movies
        movies = list(filter(lambda movie: movie.nodetype == NodeType.movie,self.ActMovGrapgh.keys()));
        filewrite.write("\nTotal no. of movies:"+ str(len(movies)))
        filewrite.write("\nTotal no. of actors:"+  str(len(actors)))
        filewrite.write("\n\nList of Movies:")
        #Write Movies information to file
        for movie in movies:
            filewrite.write("\n"  + movie.name );
        
        filewrite.write("\n\nList of Actors:")
        #Write Actors information to file
        for actor in actors:
            filewrite.write("\n" + actor.name);
        filewrite.write("\n-----------------------------------------\n")
     
    '''
    Display all the movies acted by an actor
    parameter
        name - name of actor
        filewrite - write result content to file
    '''
    def displayMoviesOfActor(self,name,filewrite):
        filewrite.write("\n--------Function displayMoviesOfActor-------- ")
        filewrite.write("\nActor name:"+ str(name));
        filewrite.write("\nList of Movies:");
        actor = Node(name,NodeType.actor);
        # No Movies found for Actor
        if not self.ActMovGrapgh[actor]:
             filewrite.write("\nNo Movies found for Actor:"+str(name))
        # Movies exists for actor
        else:
            for movie in self.ActMovGrapgh[actor]:
                filewrite.write("\n" + movie.name)          
        filewrite.write("\n-----------------------------------------\n\n")
    '''
     Display Actors performed in Movie
     parameter
         moviename - name of movie
         filewrite - write result content to file    
    '''
    def displayActorsOfMovie(self, moviename,filewrite):
        filewrite.write("\n\n--------Function displayActorsOfMovie -------- ");
        filewrite.write("\nMovie name:" + str(moviename))
        movie = Node(moviename,NodeType.movie)
        filewrite.write("\nList of Actors:")
        # No actors are acted in movie
        if not self.ActMovGrapgh[movie]:
            filewrite.write("\nNo Actors found for Movie" + str(moviename));
        #Actors performed in movie
        else:
            for actor in self.ActMovGrapgh[movie]:
                filewrite.write("\n" + actor.name);
        filewrite.write("\n-----------------------------------------\n")
    
    '''
    Find MovieA and MovieB has commong actors
    Parameters
        movA = MovieA Node
        movB = MoveB Node
    return 
        Actors in MovieA and MovieB
    '''
    
    def findMovieRelation(self, movA, movB):
        
        #visited = [Node] * len(self.ActMovGrapgh[movA]);
        visitedqueue = [];
        visitedqueue.append(movA);
        actors = [];
        while visitedqueue:
            popnode = visitedqueue.pop();
            #listofactors = filter(lambda actor:actor.nodetype == NodeType.actor,);
            for node in self.ActMovGrapgh[popnode]:
                if (node.name == movB.name) and (node.nodetype == NodeType.movie):
                    actors.append(popnode.name);
                if (node.nodetype == NodeType.actor):
                    visitedqueue.append(node);
        return actors;
    
    '''
    Find Path between NodeA and NodeB using BFS
    Parameter
        nodesrc - Source Node
        nodedest - Destination Node
        visited - Visited Nodes
        path - path between nodesrc and nodetest
        filewrite - write result content to file
    '''
    def findroute(self,nodesrc,nodedest,visited,path,filewrite):
        visited[nodesrc]= True;
        path.append(nodesrc)
        if (nodesrc.name == nodedest.name) and (nodesrc.nodetype == nodedest.nodetype):
           filewrite.write("\nRelated: Yes,")
           filewrite.write( path[0].name);
           for node in path[1:]:
               filewrite.write( " -> " + node.name );
           return True    
        else:
            for node in self.ActMovGrapgh[nodesrc]:
                if visited[node] == False:
                    #print("loop",visited.get(node))
                    if self.findroute(node,nodedest,visited,path,filewrite):
                        return True
            else:
                return False;
    
    '''
    Find transitive relation between nodesrc and nodedest
    parameter
        nodesrc - MovieA Source
        nodedest - MovieB destination
        filewrite - write result content to file
    '''    
    def findMovieTransRelation(self,nodesrc,nodedest,filewrite):
        #print("--------Function findMovieTransRelation -------- ")
        #print("Movie A: ",nodesrc.name);
        #print("Movie B: ",nodedest.name);
        visited = {};
        for node in self.ActMovGrapgh.keys():
            visited[node] = False;
        path = [];
        if not self.findroute(nodesrc,nodedest,visited,path,filewrite):
            filewrite.write("\nRelated: NO  Relation does not exist between the movies " + nodesrc.name + " and " + nodedest.name);
        #print("----------------------------------------- ")

'''
Execution for PS2
'''
if __name__ =="__main__":
    '''
    Creating the Big Screen Graph
    The Graph class has implementation for the problem PS2
    '''
    graph = Graph();
    os.chdir(os.getcwd());
    inputfile = open("inputPS2.txt","r");
    '''    
    Build Graph by using inputPS2 file
    Read input file inputPS2.txt and build graph
    '''
    for line in inputfile:
        line = line.strip();
        inputdata = line.split("/");
        moviename = inputdata[0];
        moviename = re.sub('\s+', ' ',moviename);
        moviename = moviename.strip();
        movie = Node(moviename,NodeType.movie);
        for actorname in inputdata[1:]:
            actorname = re.sub('\s+', ' ',actorname);
            actorname = actorname.strip();
            actor = Node(actorname,NodeType.actor);
            graph.addEdge(actor,movie);
    
    inputfile.close();
    
    '''Exit if no Vertices or edges were created'''
    if len(graph.ActMovGrapgh.keys()) == 0:
        print("Graph is empty");
        sys.exit();
    #else:
    #    print("Graph is not empty - ",len(graph.ActMovGrapgh.keys()));

    '''
    Read promptsPS2 input file and write the result to output file outputPS2
    '''
    inputfile = open("promptsPS2.txt","r");
    filewrite = open("outputPS2.txt","w+");
    graph.displayActMov(filewrite);
    for line in inputfile:
        line = line.strip();
        inputdata = line.split(":");
        key = inputdata[0];
        if "searchActor" in key:
            actorname = re.sub('\s+', ' ',inputdata[1]);
            actorname = actorname.strip();
            graph.displayMoviesOfActor(actorname,filewrite);
        elif "searchMovie"  in key:
            moviename = re.sub('\s+', ' ',inputdata[1]);
            moviename = moviename.strip();
            graph.displayActorsOfMovie(moviename,filewrite);
        elif "RMovies" in key:
            filewrite.write("\n\n--------Function findMovieRelation --------");
            moviename1 = re.sub('\s+', ' ',inputdata[1]);
            moviename1 = moviename1.strip();
            moviename2 = re.sub('\s+', ' ',inputdata[2]);
            moviename2 = moviename2.strip();
            movie1 = Node(moviename1,NodeType.movie);
            movie2 = Node(moviename2,NodeType.movie);
            filewrite.write("\n\nMovie A:" + moviename1);
            filewrite.write("\nMovie B:" + moviename2);
            actors = graph.findMovieRelation(movie1,movie2);
            if(len(actors) > 0):
                filewrite.write("\nRelated: Yes,")
                for actor in actors:
                    filewrite.write(" " + actor)
            else:
                filewrite.write("\nRelated: NO, Relation does not exist between the movies " + moviename1 + " and " + moviename2);
            #print(actors);
            filewrite.write("\n-----------------------------------------\n")
        elif "TMovies" in key:
            filewrite.write("\n\n--------Function findMovieTransRelation--------");
            moviename1 = re.sub('\s+', ' ',inputdata[1]);
            moviename1 = moviename1.strip();
            moviename2 = re.sub('\s+', ' ',inputdata[2]);
            moviename2 = moviename2.strip();
            movie1 = Node(moviename1,NodeType.movie);
            movie2 = Node(moviename2,NodeType.movie);
            filewrite.write("\n\nMovie A:" + moviename1);
            filewrite.write("\nMovie B:" + moviename2);
            graph.findMovieTransRelation(movie1,movie2,filewrite);
            filewrite.write("\n-----------------------------------------\n")
            
            
    inputfile.close();
    filewrite.close();
    print("Execution completed,Please check for Output file")