import pandas as pd 
from sklearn import preprocessing
from sklearn.utils import resample
pd.options.mode.chained_assignment = None

class PreProcessingData:
    
    def __init__(self):
        self.le = preprocessing.LabelEncoder()
        
        
    def __getCSV(self):
        df = pd.read_csv('bitnetflowNormal.csv')
        return df 
    
    #função que gera novamente (ou pela primeira vez) os dados preprocessados
    def generateData(self,reduce_factor=1):
        
        self.__ParseData(self.__getCSV(),reduce_factor)
    
    def __ParseData(self,df,reduce_factor):
        #df['Label']=df['Label'].replace(to_replace=r'[\w\W]*Bot[\w\W]*', value='bot', regex=True)
        #df['Label']=df['Label'].replace(to_replace=r'[\w\W]*Background[\w\W]*', value='background', regex=True)
        #df['Label']=df['Label'].replace(to_replace=r'[\w\W]*Normal[\w\W]*', value='normal', regex=True)
        
        # excluindo os erros de nan dos fluxos
        
        #df = df[(~df.sTos.isnull())&(~df.dTos.isnull())]
        #deixando apenas os normais e backgrounds
        #df = df[(df.Label=='normal')|(df.Label=='bot')]
        # colunas tiradas a princípio 
        df.drop(['StartTime','DstAddr','SrcAddr','Dport','Sport'],axis=1,inplace=True)    
    
        #estou fazendo um regex para trocar as interrogações por setas , mas isso deve ser conferido
        df['Dir']=df['Dir'].apply(str.strip)
        df['Dir']=df['Dir'].replace('<?>','<->').replace('?>','->').replace('<?','<-')
    
        # por enquanto estou deixando fora a coluna State(discreta) 
        df.drop('State',axis=1,inplace=True)
        
        #balanceamento de classes
        
        self.df_data,self.df_target=self.__LabelBalance(df,reduce_factor)
        
        #discrete features : proto , dir
        #one hot encoder -> valores que nao faz sentido serem comprados, devem ser transformados em colunas diferentes para melhor análise dos dados
        self.df_data = pd.get_dummies(self.df_data,prefix=['Proto','Dir'])
        
        self.__LabelEncoder()
            
    def __LabelEncoder(self):
        self.le.fit(self.df_target)
        self.df_target = self.le.transform(self.df_target)
        # 0->bot
        # 1->normal
        print(list(self.le.inverse_transform([0, 1])))
        
    def LabelDecoder(self,target):
        return self.le.inverse_transform(target)
    
    def getData(self):
        return self.df_data.as_matrix(),self.df_target
    
    def __LabelBalance(self,df,reduce_factor=1):
        df_majority = df[df.Label=='normal']
        df_minority = df[df.Label=='bot']
        
        df_majority_downsampled = resample(df_majority, 
                                         replace=False,
                                         n_samples=(len(df_majority)//reduce_factor),    
                                         random_state=123)
        df_minority_downsampled = resample(df_minority, 
                                         replace=False,    
                                         n_samples=len(df_minority)//reduce_factor,     
                                         random_state=123)
        
        df_downsampled = pd.concat([df_majority_downsampled, df_minority_downsampled])
        print(df_downsampled.Label.value_counts())
        
        df_target = df_downsampled['Label']
        df_downsampled.drop('Label',axis=1,inplace=True)
        df_downsampled.reindex()
        
        return df_downsampled,df_target
        
if __name__ == "__main__":
    prep = PreProcessingData()
    prep.generateData()
    data,target = prep.getData()
    exit()
#    prep.Generate_TrainingTestSet(data,target)

