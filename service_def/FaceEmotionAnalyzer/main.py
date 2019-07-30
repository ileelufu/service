"""
    NEUTRAL
    HAPPINES
    SADNESS
    ANGER
    FEAR
    SURPRISE
    DISGUST """
    
import sys
import argparse
import cv2
import argparse
import json
from collections import OrderedDict

from faces import FaceDetector
from data import FaceData
from gabor import GaborBank
from emotions import EmotionsDetector

#---------------------------------------------
class VideoData:
    """
    Helper class to present the detected face region, landmarks and emotions.
    """

    #-----------------------------------------
    def __init__(self):
        """
        Classe construtor.
        """

        self._faceDet = FaceDetector()
        '''
        A instância do detector de face.
        '''

        self._bank = GaborBank()
        '''
        A instância do banco de filtros Gabor.
        '''

        self._emotionsDet = EmotionsDetector()
        '''
        A instância do detector de emoções.
        '''

        self._face = FaceData()
        '''
        Dados da última face detectada.
        '''

        self._emotions = OrderedDict()
        '''
        Dados das últimas emoções detectadas.
        '''

    #-----------------------------------------
    def detect(self, frame):
        """
        Detecta uma face e as emoções prototípicas na imagem do frame.

        """

        ret, face = self._faceDet.detect(frame)
        if ret:
            self._face = face

            # Cortar apenas a região da face
            frame, face = face.crop(frame)

            # Filtrar com o banco Gabor
            responses = self._bank.filter(frame)

            # Detectar as emoções prototípicas com base nas respostas do filtro
            self._emotions = self._emotionsDet.detect(face, responses)

            return True
        else:
            self._face = None
            return False

    #-----------------------------------------
    def draw(self, frame):
        """
        Desenha os dados detectados da imagem do frame fornecida.
        """
        empty = True

         # Traçar os marcos da face e distância do rosto
        x = 5
        y = 0
        w = int(frame.shape[1]* 0.2)
        try:
            face = self._face
            empty = face.isEmpty()
            face.draw(frame)
        except:
            pass 

        # Plot the emotion probabilities
        try:
            emotions = self._emotions
            if empty:
                labels = []
                values = []
            else:
                labels = list(emotions.keys())                                  ## Lista com as emoções disponíveis
                values = list(emotions.values())                                ## Lista com 
                bigger = labels[values.index(max(values))]                      ## MAIOR PROBABILIDADE
                data = {"emotionDetection":bigger,
                        "emotionsProbabilities":emotions
                       }

                print('', json.dumps(data, indent=2))
                #print(bigger)                                                   ## PRINTANDO A EMOÇÃO COM MAIOR PROBABILIDADE

        except Exception as e:
            print(e)
            pass

ap = argparse.ArgumentParser();
ap.add_argument("-i", "--image", required = True, help = "path to the image file");
args = vars(ap.parse_args());

# Read the image
image = cv2.imread(args["image"]);

# Clone the image
frame = image.copy();

data = VideoData()

data.detect(frame)
data.draw(frame)
