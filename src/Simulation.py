import json
import pandas as pd

class Simulation():
    
    def __init__(self,js):
        
        with open(js) as train_file:
            self.twin = json.load(train_file)
        
        self.sim_files = self.twin['$OptionalInformationAttributes'][-1]["simulation_files"]
        self.save_sim_files()
    
    def save_sim_files(self):
            
        # read initial forging parameters
        for item in self.twin['$OptionalInformationAttributes']:
            if "$process" in item:   
                df = pd.DataFrame.from_dict(item, orient='index')
                df = df.T
                df.drop(columns = ['$process'],inplace = True)

        #intialising file list
        file_list = []

        for file in self.sim_files:
            # readinag given text file and creating dataframe
            dataframe1 = pd.read_csv(file, header=2,sep='\t')
            dataframe1.drop(['Unnamed: 14'],axis =1, inplace = True)

            dataframe1 = dataframe1.set_index('Time (sec)')
            tf=dataframe1.T.stack()
            filename = (file.split('/')[-1]).split('.')[0]
            new_tf = tf.reset_index().rename(columns={'level_0':'Point_name',0:filename})

            new_tf[df.columns[0]] = df[df.columns[0]][0]
            new_tf[df.columns[1]] = df[df.columns[1]][0]
            new_tf[df.columns[2]] = df[df.columns[2]][0]

            file_name = 'simulation_files/'+new_tf.columns[2]+'.csv'
            new_tf.to_csv(file_name,index = False)
            file_list.append(file_name)

        #save csv files replacing txt
        del self.sim_files
        self.twin['$OptionalInformationAttributes'][-1]["simulation_files"] = file_list

    def load_sim_files(self):
        
        for file in self.twin['$OptionalInformationAttributes'][-1]["simulation_files"]:
            if 'temp' in file:
                temp_df = pd.read_csv(file)
            elif 'strain' and not 'rate' in file:
                strain_df = pd.read_csv(file)
            elif 'strain_rate' in file:
                strain_rate_df = pd.read_csv(file)
                
        return temp_df,strain_df,strain_rate_df 
            