class Model():
    
    def __init__(self):
        
        
    def train()
    
        loc_ref_list_XG = ['P3','P4','P10','P11']
        loc_ref_list_GPR = ['P1','P2','P5','P6''P7','P8','P9','P12','P13']

        for loc_ref in loc_ref_list_XG:

            P1 = temp_df[temp_df['Point_name']==loc_ref]
            P1 = P1[P1['Time (sec)']>10]
            P1 = P1.reset_index(drop=True)
            P1 = P1.drop(columns = 'Point_name')

            y = P1['temp']
            X = P1.drop('temp', axis=1)

            # use minMax scaler
            min_max_scaler = MinMaxScaler()
            X_train = min_max_scaler.fit_transform(X_train)

            model = XGBRegressor(n_estimators=1000, max_depth=6, eta=0.03, subsample=0.1, colsample_bytree=0.7)
            model.fit(X_train,y_train)

        for loc_ref in loc_ref_list_GPR:  

            P2 = temp_df[temp_df['Point_name']==loc_ref]
            P2 = P2[P2['Time (sec)']>10]
            P2 = P2.reset_index(drop=True)
            P2 = P2.drop(columns = 'Point_name')
            standardised_df = P2.copy()
            for col in P2.columns:
                if (np.std(P2[col])> 0):
                    standardised_df[col] = standardise(P2[col],np.mean(P2[col]),np.std(P2[col]))
                else:
                    standardised_df = standardised_df.drop(columns=col)

            X_P2 = standardised_df.loc[:, standardised_df.columns != 'temp']
            Y_P2 = standardised_df['temp']
            
            kernel = 1.0 * Matern(length_scale=1.0, nu=1.5)
            gpr = GaussianProcessRegressor(kernel=kernel,random_state=0,n_restarts_optimizer=0).fit(X_P2, Y_P2)
        
    
    def standardise(x, offset, width):
    """
    Description
    -----------
        Standardise the array, x, so that it removes 'offset' then divides
            by 'width'.

    Parameters
    ----------
        x : signal to be standardised
        offset : fairly obvious...
        width : also fairly obvious...

    Returns
    -------
        xs : standardised signal
    """

    if width == 0:
        print('Warning: standard deviation equal to zero')
        xs = x - offset
    else:
        xs = (x - offset) / width

    return xs

    def predict(X_predict):
        
        Y_df_test ['Predicted']=model.predict(X_test)
        Y_df_test

        y_std = np.std(P2['temp'])
        y_mean = np.mean(P1['temp'])

        y_gpr_mean, y_gpr_std = gpr.predict(X_predict, return_std=True)
        y_actual = Y_P1[234:].reset_index(drop=True)
        Y_df = pd.DataFrame(y_gpr_mean*y_std+y_mean, columns=['Predicted temp'])
        Y_df['Actual temp'] = y_actual*y_std+y_mean

        Y_df['Upper bound'] = (y_gpr_mean-3*y_gpr_std)*y_std+y_mean
        Y_df['Lower bound'] = (y_gpr_mean+3*y_gpr_std)*y_std+y_mean
