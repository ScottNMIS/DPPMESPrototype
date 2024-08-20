#import plotly.graph_objects as go
import holoviews as hv
import hvplot.pandas
import numpy as np
import os
import sympy as sym
import numpy as np
import math
import pandas as pd
from sympy import lambdify

class Instability():
    
        def __init__(self,predicted_temp_df,predicted_strain_df,predicted_strain_rate_df):
            self.predicted_temp_df = predicted_temp_df
            self.predicted_strain_df = predicted_strain_df
            self.predicted_strain_rate_df = predicted_strain_rate_df
            
        def instability_map(self): 
            
            x , y, t = sym.symbols('x y t')
            
            R = 8.3145
            initial_stress = 10
            C7 = initial_stress*initial_stress
            B = 70
            
            # Calculations for stress before peak stress and after
            D5 = np.power(10,x)*sym.exp(584089/(R*(273+t))) # taking x power because x-log(strain rate)
            c = 0.000000003*np.power((sym.log(D5,10)),7.61)

            initial_stress = 0.000000003*np.power(sym.log(D5,10),7.5625)
            C7 = initial_stress*initial_stress
            steady_state_stress = c*c
            peak_strain = 0.00000002*np.power(sym.log(D5,10),4.5805)
            saturation_stress = 0.0000000003*np.power(sym.log(D5,10),8.2067)

            # before peak stress/strain
            stress_a = ((steady_state_stress+(C7-steady_state_stress)*sym.exp(-2*B*y)))**0.5

            # after peak stress
            intial_stress = ((steady_state_stress+(C7-steady_state_stress)*sym.exp(-2*B*y)))**0.5
            fraction_of_recrystalisation = 1-sym.exp(-(4)*np.power((y-peak_strain),1.5))
            stress_b = intial_stress-fraction_of_recrystalisation*(intial_stress-saturation_stress)

            # calculate instability factor
            f_a = sym.log(stress_a,10)
            m_a = f_a.diff(x)
            derivative_f_a = sym.log((m_a /(m_a +1)),10).diff(x)
            instability_a = derivative_f_a+m_a

            f_b = sym.log(stress_b,10)
            m_b = f_b.diff(x)
            derivative_f_b = sym.log(m_b/(m_b+1),10).diff(x)
            instability_b = derivative_f_b+m_b
            
            f1 = lambdify([x,y,t], instability_a)
            f2 = lambdify([x,y,t], instability_b)

            self.predicted_strain_rate_df['Predicted strain_rate(log)'] = np.log(self.predicted_strain_rate_df['Predicted strain_rate'])


            contour_function1 = f1(self.predicted_strain_rate_df['Predicted strain_rate(log)'],self.predicted_strain_df['Predicted strain'], self.predicted_temp_df['Predicted temp'])
            contour_function2 = f2(self.predicted_strain_rate_df['Predicted strain_rate(log)'],self.predicted_strain_df['Predicted strain'], self.predicted_temp_df['Predicted temp'])
            
            df1 = pd.DataFrame(contour_function2)
            df2 = pd.DataFrame(contour_function1)
            
            instability_df = pd.DataFrame(data = df1.combine_first(df2).to_numpy(),columns = ['instability'])     
            instability_df['Predicted strain_rate(log)'] = self.predicted_strain_rate_df['Predicted strain_rate(log)']
            instability_df['Predicted strain']=self.predicted_strain_df['Predicted strain']
            instability_df['Predicted temp'] = self.predicted_temp_df['Predicted temp']
            instability_df['Point_name'] = self.predicted_temp_df['Point_name']
            
            #instability_df = instability_df.dropna()
            
            # stress calculations
            
            f1 = lambdify([x,y,t], stress_a)
            f2 = lambdify([x,y,t], stress_b)

            self.predicted_strain_rate_df['Predicted strain_rate(log)'] = np.log(self.predicted_strain_rate_df['Predicted strain_rate'])


            stress_function1 = f1(self.predicted_strain_rate_df['Predicted strain_rate(log)'],self.predicted_strain_df['Predicted strain'], self.predicted_temp_df['Predicted temp'])
            stress_function2 = f2(self.predicted_strain_rate_df['Predicted strain_rate(log)'],self.predicted_strain_df['Predicted strain'], self.predicted_temp_df['Predicted temp'])
            
            df3 = pd.DataFrame(stress_function2)
            df4 = pd.DataFrame(stress_function1)
            
            stress_df = pd.DataFrame(data = df3.combine_first(df4).to_numpy(),columns = ['stress'])     
            stress_df['Predicted strain_rate(log)'] = self.predicted_strain_rate_df['Predicted strain_rate(log)']
            stress_df['Predicted strain']=self.predicted_strain_df['Predicted strain']
            stress_df['Predicted temp'] = self.predicted_temp_df['Predicted temp']
            stress_df['Point_name'] = self.predicted_temp_df['Point_name']
            #stress_df['Point_name']=self.predicted_temp_df['Point_name']
            #stress_df = stress_df.dropna()
            
            '''
            fig = go.Figure(data=[go.Scatter3d(
            x= instability_df['Predicted strain_rate(log)'],
            y= instability_df['Predicted temp'],
            z= instability_df['Predicted strain'],
            mode='markers',
            marker=dict(
                size=6,
                color=instability_df['instability'],
                cmin = instability_df['instability'].min(),
                cmax = instability_df['instability'].max(),# set color to an array/list of desired values
                colorscale='Viridis',   # choose a colorscale
                colorbar=dict(thickness=20,title = 'Instability'),
                opacity=0.8
                )

            )])

            # tight layout
            fig.update_layout(autosize=False,scene=dict(
                    xaxis_title='Strain rate (log)',
                    yaxis_title='Temperature',
                    zaxis_title='Strain'),
                margin=dict(l=0, r=0, b=0, t=0))
            #fig.show()
            '''
            
            return instability_df,stress_df