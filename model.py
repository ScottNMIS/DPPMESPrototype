# import required libraries
import os
import os.path
import sys
import holoviews as hv
import hvplot.pandas
from xgboost import XGBRegressor
import pandas as pd
import numpy as np
import pickle

from src.Simulation import Simulation
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV
from scipy.interpolate import make_interp_spline
from scipy.signal import savgol_filter

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV


class Model():
    
    def __init__(self,temp_df,strain_df,strain_rate_df):
        self.temp_df = temp_df
        self.strain_df = strain_df
        self.strain_rate_df = strain_rate_df

    def load_simulation_data():
        pwd  = os.getcwd()
        data_temp = pd.DataFrame()
        data_strain = pd.DataFrame()
        data_strain_rate = pd.DataFrame()

        for root, _, files in os.walk("data"):
            if "part_simulation.json" in files:
                os.chdir(root)
                twin = Simulation("part_simulation.json")
                temp_df,strain_df,strain_rate_df = twin.load_sim_files()
                os.chdir(pwd)

                X_Y_Spline = make_interp_spline(temp_df.index, temp_df.temp)
                temp_df.temp = X_Y_Spline(temp_df.index)
                data_temp = pd.concat([data_temp, temp_df],ignore_index=True)
                data_strain = pd.concat([data_strain, strain_df],ignore_index=True)
                data_strain_rate = pd.concat([data_strain_rate, strain_rate_df],ignore_index=True)

        return data_temp,data_strain,data_strain_rate   

    def point_temp_model_train(self,P):

        #point_list = temp_df.Point_name.unique().tolist()
        #for P in point_list:

        P_temp = self.temp_df[self.temp_df['Point_name']==P]
        P_temp = P_temp.reset_index(drop=True)
        P_temp = P_temp.drop(columns = 'Point_name')
        y_temp = P_temp['temp']
        X_temp = P_temp.drop('temp', axis=1)
        #print('Traning temp data model')
        
        self.train_XGB(X_temp,y_temp,P, 'temp')
    
    def point_strain_model_train(self,P):   
        
        P_strain = self.strain_df[self.strain_df['Point_name']==P]
        P_strain = P_strain.reset_index(drop=True)
        P_strain = P_strain.drop(columns = 'Point_name')
        y_strain = P_strain['strain']
        X_strain = P_strain.drop('strain', axis=1)
        #print('Training strain data model')

        if (P == 'P2' or P == 'P3' or P == 'P6' or P == 'P10'or P == 'P11' or P == 'P12'):
            self.train_XGB(X_strain,y_strain,P,'strain')
        else:
            self.train_RF(X_strain,y_strain,P,'strain')
 

    def point_strain_rate_model_train(self,P):  
        
        P_strain_rate = self.strain_rate_df[self.strain_rate_df['Point_name']==P]
        P_strain_rate = P_strain_rate.reset_index(drop=True)
        P_strain_rate = P_strain_rate.drop(columns = 'Point_name')
        y_strain_rate = P_strain_rate['strain_rate']
        X_strain_rate = P_strain_rate.drop('strain_rate', axis=1)
        #print('Training strain rate data model')

        self.train_RF(X_strain_rate,y_strain_rate,P,'strain_rate')


    def train_XGB(self,X,y,point_name,param):
        
        print('Training XGB, point name = '+point_name+', param ='+param)
        X_test, X_train, y_test, y_train = train_test_split(X, y,
                                                        test_size=0.705,
                                                        shuffle=False)
        # use minMax scaler
        min_max_scaler = MinMaxScaler()
        X_train = min_max_scaler.fit_transform(X_train)
        X_test = min_max_scaler.transform(X_test)
        self.save_min_max_scalar(min_max_scaler,param,point_name)
        
        
        xgb1 = XGBRegressor()
        parameters = {'learning_rate': [0.01,0.03, 0.05, 0.07,0.1], #so called `eta` value
                      'max_depth': [1,2,5,6,7, 10],
                      'subsample': [0.1, 0.5, 0.7, 1],
                      'colsample_bytree': [0.1,0,.5, 0.7,1],
                      'n_estimators': [500,1000]}

        xgb_grid = GridSearchCV(xgb1,
                                parameters,
                                cv = 10,
                                n_jobs = 100,
                                verbose=True)

        xgb_grid.fit(X_train,y_train)
        
        XGB_model = XGBRegressor(n_estimators=xgb_grid.best_params_['n_estimators'], max_depth=xgb_grid.best_params_['max_depth'], learning_rate=xgb_grid.best_params_['learning_rate'],
                     subsample=xgb_grid.best_params_['subsample'], colsample_bytree=xgb_grid.best_params_['colsample_bytree'])
        XGB_model.fit(X_train,y_train)
        
        # save the model to disk
        directory = 'results/'+param+'/'
        filename = directory+'trained_model_'+point_name+'.sav'
        pickle.dump(XGB_model, open(filename, 'wb'))
        print(param+' '+point_name+' model trained')        
        

    def train_RF(self,X,y,point_name,param):
        
        print('Training RF, point name = '+point_name+', param ='+param)
        # split into X_train and X_test
        X_test, X_train, y_test, y_train = train_test_split(X, y,
                                                            test_size=0.705,
                                                            shuffle=False)
        # use minMax scaler
        min_max_scaler = MinMaxScaler()
        X_train = min_max_scaler.fit_transform(X_train)
        X_test = min_max_scaler.transform(X_test)
        self.save_min_max_scalar(min_max_scaler,param,point_name)
        
        
        parameters = {
        'n_estimators': [100, 150, 200, 250, 300,1000],
        'max_depth': [1,2,3,4,10],
        'bootstrap': [True,False],
        'max_features':[0.2,0.5,0.8,1.0],
        }
        regr = RandomForestRegressor(random_state=0)

        regr_grid = GridSearchCV(regr, parameters)
        regr_grid.fit(X_train, y_train)
        
        RF_model = RandomForestRegressor(n_estimators=regr_grid.best_params_['n_estimators'], max_depth=regr_grid.best_params_['max_depth'], 
                                      max_features =regr_grid.best_params_['max_features'], bootstrap=regr_grid.best_params_['bootstrap'])
        RF_model.fit(X_train,y_train)
        
        # save the model to disk
        directory = 'results/'+param+'/'
        filename = directory+'trained_model_'+point_name+'.sav'
        pickle.dump(regr_grid, open(filename, 'wb'))
        print(param+' '+point_name+' model trained')
        
    def save_min_max_scalar(self,min_max_scaler,param,point_name):
        
        directory = 'results/'+param+'/' 
        scalerfile = directory+'trained_model_'+point_name+'_scaler.pkl'
        pickle.dump(min_max_scaler, open(scalerfile, 'wb'))                   
        
    def predict_with_actual_data(self,temp_df,strain_df,strain_rate_df):
        
        point_list = self.temp_df.Point_name.unique().tolist()
        param = ['temp','strain','strain_rate']
        
        Y_df_test = pd.DataFrame()
        Predicted_temp_df = pd.DataFrame()
        Predicted_strain_df = pd.DataFrame()
        Predicted_strain_rate_df = pd.DataFrame()
            
        for i,df in enumerate([temp_df,strain_df,strain_rate_df]):
            
            for point_name in point_list:

                directory = 'results/'+param[i]+'/'
                filename_model = directory+'trained_model_'+point_name+'.sav'
                filename_scalar = directory+'trained_model_'+point_name+'_scaler.pkl'

                model = pickle.load(open(filename_model, "rb"))    
                min_max_scaler = pickle.load(open(filename_scalar, "rb"))


                P = df[df['Point_name']==point_name]
                P = P.reset_index(drop=True)
                Y_df_test['Point_name']=P['Point_name']
                P = P.drop(columns = 'Point_name')
                y_t = P[param[i]]
                X_t = P.drop(param[i], axis=1)
                X_test = min_max_scaler.transform(X_t)

                Y_df_test['Actual '+param[i]] = y_t
                Y_df_test['Predicted '+param[i]]=model.predict(X_test)
                
                if (param[i] == 'temp'):
                    
                    Predicted_temp_df = pd.concat([Predicted_temp_df, Y_df_test], axis=0)
                
                if (param[i] == 'strain'):
                    
                    Predicted_strain_df = pd.concat([Predicted_strain_df, Y_df_test[['Actual strain','Predicted strain','Point_name']]], axis=0)

                if (param[i] == 'strain_rate'):
                    
                    Predicted_strain_rate_df = pd.concat([Predicted_strain_rate_df, Y_df_test[['Actual strain_rate','Predicted strain_rate','Point_name']]], axis=0)

                
        return  Predicted_temp_df,Predicted_strain_df,Predicted_strain_rate_df

    def predict(self,df):

        point_list = self.temp_df.Point_name.unique().tolist()
        params = ['temp','strain','strain_rate']
        
        
        Predicted_temp_df = pd.DataFrame()
        Predicted_strain_df = pd.DataFrame()
        Predicted_strain_rate_df = pd.DataFrame()

        for param in params:
            Predicted_df = pd.DataFrame()
            for point_name in point_list:
                Y_df_test = pd.DataFrame()
                directory = 'results/'+param+'/'
                filename_model = directory+'trained_model_'+point_name+'.sav'
                filename_scalar = directory+'trained_model_'+point_name+'_scaler.pkl'

                model = pickle.load(open(filename_model, "rb"))    
                min_max_scaler = pickle.load(open(filename_scalar, "rb"))


                P = df[df['Point_name']==point_name]
                P = P.reset_index(drop=True)
                Y_df_test['Point_name']=P['Point_name']
                Y_df_test['Time (sec)'] = P['Time (sec)']
                Y_df_test['Forging Temp.(deg.c)'] = P['Forging Temp.(deg.c)']
                Y_df_test['Die Temp(deg.c)']=P['Die Temp(deg.c)']
                Y_df_test['Stroke speed(mm per sec.)']=P['Stroke speed(mm per sec.)']
                P = P.drop(columns = 'Point_name')

                #print(point_name)
                X_test = min_max_scaler.transform(P)
                Y_df_test['Predicted '+param]=model.predict(X_test)

                Predicted_df = pd.concat([Predicted_df, Y_df_test], axis=0)
            if (param == 'temp'):
                
                Predicted_temp_df = Predicted_df
            
            if (param == 'strain'):
                
                Predicted_strain_df = Predicted_df
    
            if (param == 'strain_rate'):
                
                Predicted_strain_rate_df = Predicted_df
        
        return Predicted_temp_df,Predicted_strain_df,Predicted_strain_rate_df