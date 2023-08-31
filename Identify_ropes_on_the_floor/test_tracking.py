# -*- coding: utf-8 -*-
"""
@author: AranaCorp
https://www.aranacorp.com/pt/detectar-uma-linha-com-python-e-a-opencv/

updated by Wander to identify blue ropes 
wanderok@msn.com

"""
#by Wander:
#This code identify blue ropes

import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from time import sleep


class LineTracking():
    """
    AranaCorp: 
    Classe permettant le traitement d'image, la délimitation d'un contour et permet de 
    trouver le centre de la forme detectée
    
    Translated by Wander:
    Class allowing the image processing, the delimitation of an outline and allows to
    find the center of the detected shape    

    """
    def __init__(self,img_file):
        """The constructor."""
        self.img = cv2.imread(img_file)
        self.img_inter = self.img
        self.img_final = self.img
        self.cendroids = []
        self.mean_centroids = [0,0]

    def processing(self):
        """
        AranaCorp:
        Méthode permettant le traitement d'image

        Translated by Wander:
        Method for image processing
        """
        #self.img=cv2.resize(self.img,(int(self.img.shape[1]*0.2),int(self.img.shape[0]*0.2))) #redimensionar imagem original
        #self.img=cv2.resize(self.img,(int(self.img.shape[1]*0.5),int(self.img.shape[0]*0.5))) #redimensionar imagem original
        
        print(self.img.shape)

        # refocus the image excluding the outer areas to have greater precision in the rest
        #self.img = self.img[199:391, 149:505] 

        # change the image to grayscale
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY) 

        # blur the image
        blur = cv2.GaussianBlur(gray,(5,5),0) 

        #by Wander:
        #This did not work with de last video file sended by Prof.Ramos at 2023/08/10
        #but the line below works with other videos...
        #ret,thresh = cv2.threshold(blur,180,255,cv2.THRESH_BINARY_INV) # binarizamos a imagem
        
        #by Wander: I changed it like below:
        testing=170
        ret,thresh = cv2.threshold(blur,testing,255,cv2.THRESH_BINARY_INV) # binarizamos a imagem

        self.img_inter=thresh
        
        """
        AranaCorp:
        Une ouverture permet d'enlever tous les élements qui sont plus petits que l'élement structurant (ou motif)
        Une fermeture permet de "combler" les trous qui ont une taille inférieur à l'élement structurant 
        
        Translated by by Wander:
        An opening makes it possible to remove all the elements which are smaller than the structuring element (or pattern)
        A closure makes it possible to "fill" the holes which have a size less than the structuring element        

        """
        # create the structuring element of the opening
        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)) # criamos o elemento estruturante da abertura

        # create the closing structuring element
        kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10)) # criamos o elemento estruturante do fechamento

        # make an opening following a pattern
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_open) # fazemos uma abertura seguindo um padrão

        # fazemos um fechamento seguindo um padrão# make a closure following a pattern
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_close) # fazemos um fechamento seguindo um padrão

        connectivity = 8

        # delimit a shape
        output = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S) 

        num_labels = output[0]
        labels = output[1]
        stats = output[2]
        
        #returns the centers of the image shape(s)
        self.centroids = output[3] 
        #print('self.centroids=',self.centroids)   
        for c in self.centroids :
            print('c=',c)
            """
            AranaCorp: 
               Permet de faire la moyenne des centres de la forme, en effet sur l'image test,
               il y a deux centres qui sont très proches et la moyenne de deux convient.
               On pourra imaginer que dans un cas général on modifie cela

            Translated by by Wander:
               Allows to average the centers of the shape, indeed on the test image,
               there are two centers that are very close and the average of two is fine.
               We can imagine that in a general case we modify this               
            """
            self.mean_centroids[0] += c[0]/len(self.centroids)
            self.mean_centroids[1] += c[1]/len(self.centroids)

        self.img_final = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        """
        AranaCorp: 
        permet de rajouter un carré rouge à l'endroit du centre de la forme
        lets we add a red square in the center of the shape
        
        Translated by Wander:        
        allows you to add a red square at the center of the shape
        lets we add a red square in the center of the shape                
        """

        #self.img_final[int(self.mean_centroids[1])-10 : int(self.mean_centroids[1])+20, int(self.mean_centroids[0])-10 : int(self.mean_centroids[0])+20] = [0,0,255]
        try:
           self.img_final[int(self.mean_centroids[1])-10 : int(self.mean_centroids[1])+20, int(self.mean_centroids[0])-10 : int(self.mean_centroids[0])+20] = [0,0,255]
           #for c in self.centroids :
           #   if (c[1]>0):
           #      self.img_final[int(c[1])-5 : int(c[1])+10, int(c[0])-5 : int(c[0])+10] = [0,255,0]
        except:
           print("An exception occurred")

if __name__ == '__main__' :
    #by Wander:
    #to capture images from the drone camera or a webcam   
    #camera = cv2.VideoCapture(0) 

    #by Wander: 
    # to load a video file
    # this video was recored and sended to me by professor Alexandre Ramos
    camera = cv2.VideoCapture('video.mp4')

    if camera.isOpened():
        validacao, frame = camera.read()
        while validacao:
            validacao, frame = camera.read()
            
            #by Wander: 
            # generate a frame of the captured image
            frame=cv2.resize(frame,(int(frame.shape[1]*0.5),int(frame.shape[0]*0.5))) #redimensionar imagem original
            cv2.imwrite('imgTmp.png',frame)

            #by Wander: 
            #process the image 
            #create a LineTracking object which is the Class created above .png or .jpg
            test = LineTracking('imgTmp.png') #créer un objet LineTracking qui est la Classe créée au dessus .png ou .jpg
            
            test.processing()

            """
            AranaCorp: 
            affiche l'image original après redimensionnement
            
            translated by Wander: 
            displays the original image after resizing
            """
            cv2.imshow('image',frame) 

            #by Wander: 
            # show the processed image            
            ##cv2.imshow('process',test.img_inter ) #affiche l'image après traitement
            cv2.imshow('cable',test.img_final) #affiche l'image après traitement

            #by Wander: 
            #to finish, press the "space bar" key
            key= cv2.waitKey(1);

            """
            AranaCorp: 
            pour fermer les fenêtres appuyer sur la barre 'espace'

            Translated by Wander: 
            to close the windows press the 'space' bar
            """

            if  key == ord(' '): 
                break

        #by Wander: 
        #to free memory
        camera.release()    

        #by Wander: 
        #to close the opened windows
        cv2.destroyAllWindows()