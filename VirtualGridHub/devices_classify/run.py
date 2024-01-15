import os
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout, Activation, Flatten
from tensorflow.keras import optimizers
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image

import numpy as np
import tensorflow as tf
import pandas as pd
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from matplotlib import rc
from pandas.plotting import register_matplotlib_converters
import math
import glob
from sklearn.model_selection import train_test_split
import cv2
from skimage import feature,filters
from PIL import Image
import sys
from scipy import signal

# 以下の２行はJupyter環境の場合のみ必要
#%matplotlib inline
#from IPython import display
#%config InlineBackend.figure_format='retina'

register_matplotlib_converters()
sns.set(style='whitegrid', palette='muted', font_scale=1.5)

rcParams['figure.figsize'] = 22, 10

RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

#print(tf.__version__)


def my_model_load():
    input_tensor = Input(shape=(img_rows, img_cols, 3))
    vgg16 = VGG16(include_top=False, weights=None, input_tensor=input_tensor)
    top_model = Sequential()
    top_model.add(Flatten(input_shape=vgg16.output_shape[1:]))
    top_model.add(Dense(256, activation='relu'))
    top_model.add(Dropout(0.5))
    top_model.add(Dense(nb_classes, activation='softmax'))
    model = Model(inputs=vgg16.input, outputs=top_model(vgg16.output))
    model.load_weights(os.path.join('model', 'VirtualGridHub/devices_classify/model/product_classify_cwt_cnn_pdnego_ep50_ba32.hdf5'))
    return model

# 一つのcsvファイルから VBUS V I W  を返す
def ImportCSVandConvertDF(FILE):
    data=pd.read_csv(FILE)
    data_V=data.iloc[:,1]
    data_C=data.iloc[:,2]
    data_W=data.iloc[:,3]
    npdata_V=data_V.values
    npdata_V
    npdata_C=data_C.values
    npdata_C
    npdata_W=data_W.values
    npdata_W
    return npdata_W

'''# wattage を CWT変換
def calcuate_cwt(sig):
    widths = np.arange(1, 31)
    cwtmatr = signal.cwt(sig, signal.ricker, widths)
    return cwtmatr'''

'''#CWTを画像で保存
def plot_cwt_save(cwtmatr_,figure_size,SAVEPATH,FILENAME):
    #figure_size=(50,50)
    plt.figure(figsize=figure_size)
    #plt.imshow(cwtmatr_, extent=[-1, 1, 1, 31], cmap='gray', aspect='auto',
    #          vmax=abs(cwtmatr_).max(), vmin=-abs(cwtmatr_).max())
    plt.imshow(cwtmatr_, extent=[-1, 1, 1, 31], cmap='gray', aspect='auto')
    plt.axis("off")
    plt.show()#kore wo kesuto dame
    plt.savefig(SAVEPATH+'/'+FILENAME+'.png')
    
    plt.close('all')'''

def plot_cwt_save(cwtmatr_,figure_size,SAVEPATH,FILENAME):
    #figure_size=(10,10)
    fig, ax = plt.subplots(figsize=figure_size)
    #plt.figure(figsize=figure_size)
    #plt.imshow(cwtmatr_, extent=[-1, 1, 1, 31], cmap='gray', aspect='auto',
    #           vmax=abs(cwtmatr_).max(), vmin=-abs(cwtmatr_).max())
    plt.imshow(cwtmatr_, extent=[-1, 1, 1, 31], cmap='gray', aspect='auto')
    plt.axis("off")
    #fig.subplots_adjust(left=0, right=1, bottom=0, top=1) #この1行を入れる
    #plt.show()
    plt.savefig(SAVEPATH+'/'+FILENAME+'.png',dpi=20)
    plt.close('all')

'''#データセット分の画像を生成
def make_cwt_dataset(data_path, save_a_path):
    for j, d in enumerate(data_path):
        w = ImportCSVandConvertDF(d)
        #print(j)
        cwt_arr=calcuate_cwt(w)
        figure_size=(50,50)
        plot_cwt_save(cwt_arr,figure_size,save_a_path,str(j))
    print('CWT DATASET DONE...')'''

# ricker ウェーブレット
def calcuate_cwt_ricker(sig):
    widths = np.arange(1, 50)
    cwtmatr = signal.cwt(sig, signal.ricker, widths)
    return cwtmatr

import pywt
# メキシカンウェーブレット
def calcuate_cwt_pywt_mexh(sig):
    widths = np.arange(1, 100)
    cwtmatr = pywt.cwt(sig, widths, 'mexh')[0]
    return cwtmatr

# morl wavelet
def calcuate_cwt_pywt_morl(sig):
    widths = np.arange(1, 100)
    cwtmatr = pywt.cwt(sig, widths, 'morl')[0]
    return cwtmatr

def make_cwt_dataset(data_path, save_path):
    figure_size=(20,20)
    for j, d in enumerate(data_path):
        w = ImportCSVandConvertDF(d)
        #print(j)
        cwt_arr=calcuate_cwt_ricker(w)
        length_path = len(str(d).split("/"))
        save_filename = str(d).split("/")[length_path-1].split(".csv")[0]+"_ricker"
        print(save_filename)
        plot_cwt_save(cwt_arr,figure_size,save_path,save_filename)
    for j, d in enumerate(data_path):
        w = ImportCSVandConvertDF(d)
        cwt_arr=calcuate_cwt_pywt_mexh(w)
        length_path = len(str(d).split("/"))
        save_filename = str(d).split("/")[length_path-1].split(".csv")[0]+"_mexh"
        print(save_filename)
        plot_cwt_save(cwt_arr,figure_size,save_path,save_filename)
    for j, d in enumerate(data_path):
        w = ImportCSVandConvertDF(d)
        cwt_arr=calcuate_cwt_pywt_morl(w)
        length_path = len(str(d).split("/"))
        save_filename = str(d).split("/")[length_path-1].split(".csv")[0]+"_morl"
        print(save_filename)
        plot_cwt_save(cwt_arr,figure_size,save_path,save_filename)
    print('CWT DATASET DONE...')

ROOT_DIR = 'eval_csv'
TARGET_PATTERN = "**.csv"
SAVEPATH = 'eval_cwt'
classes = ['Pixel_IK','Pixel_MA','Pixel_SE']
nb_classes = len(classes)
img_rows, img_cols = 224, 224

def predict():
    root_a_path=[]
    root_a_path.extend(glob.glob(os.path.join(ROOT_DIR, TARGET_PATTERN)))
    root_a_test_path = root_a_path
    #csvからcwtの画像を生成し，データセットに保存
    #make_cwt_dataset(root_a_test_path, SAVEPATH)
    filename = glob.glob(os.path.join(SAVEPATH, '*.png'))
    model = my_model_load()
    for target in filename:
        #img = np.array( Image.open(target))
        #plt.imshow( img )
        img = load_img(target, target_size=(img_rows, img_cols))
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        predict = model.predict(preprocess_input(x))
        for pre in predict:
            y = pre.argmax()
            print("filename =", target)
            print("test result =",classes[y], pre)

predict()
