#importing the libraries
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
import statsmodels.api as sm
import matplotlib.pyplot as plt
import plotly.express as px
import base64
import io
import os


class DiD:

    def __init__(self, dataset=None):
        # self.dataset = dataset
        self.dataset = dataset
        print(dataset)


    # #pulling the data
    def read_csv_df(self):
        self.dataset = pd.read_csv(os.environ['SAMPLE-FILE'])
        print(self.dataset)
        return self.dataset

    def read_uploaded_data(self, uploaded_data:str=None):
        if not uploaded_data:
            print("No Data read yet")
        else:
            print(uploaded_data + " data read")
            return uploaded_data


    #check our data
    def describe_data(self):
        summary_stats = self.dataset.describe()
        return summary_stats

    pd.set_option('display.max_columns', None)

    #check if there are more NAs
    def check_for_nans(self):
        any_nans = self.dataset.isnull().any()
        return any_nans

    #replacing NAs with averages
    def replace_nans(self):
        missingvalues = SimpleImputer(missing_values = np.nan,
                                      strategy = 'mean')
        missingvalues = missingvalues.fit(self.dataset[['fte', 'demp']])
        self.dataset[['fte', 'demp']] = missingvalues.transform(self.dataset[['fte', 'demp']])
        return self.dataset

    #check if there are more NAs
    # dataset.isnull().any()

    #isolating the X and Y variables
    def split_x_y_dataset(self):
        X = self.dataset.iloc[:, 0:3].values
        Y = self.dataset.iloc[:, 3].values
        return X, Y

    #creating the first model
    def create_first_model(self):
        X, Y = self.split_x_y_dataset()
        X = sm.add_constant(X)
        model1 = sm.OLS(Y, X).fit()
        model_summary = model1.summary(yname = "FTE",
                       xname = ("intercept", "New Jersey", "After April 1992",
                                "New Jersey and after April 1992"))
        return model_summary


    #isolating the X and Y variables part 2
    def split_x_y_variables_2(self):
        X = self.dataset.loc[:, ['NJ', 'POST_APRIL92', 'NJ_POST_APRIL92',
                    'bk', 'kfc', 'wendys']].values
        Y = self.dataset.loc[:, ['FTE']].values
        return X, Y

    #creating the second model
    def create_second_model(self):
        X, Y = self.split_x_y_variables_2()
        X = sm.add_constant(X)
        model2 = sm.OLS(Y, X).fit()
        model_summary = model2.summary(yname = "FTE",
                       xname = ("intercept", "New Jersey", "After April 1992",
                                "New Jersey and after April 1992",
                            "Burger King", "KFC", "Wendy's"))
        return model_summary

    #isolating the X and Y variables part 2
    def split_x_y_variables_3(self):
        X = self.dataset.loc[:, ['NJ', 'POST_APRIL92', 'NJ_POST_APRIL92',
                        'bk', 'kfc', 'wendys',
                    'co_owned', 'centralj', 'southj']].values

        Y = self.dataset.loc[:, ['FTE']].values
        return X, Y

    #creating the third model
    def create_second_model(self):
        X, Y = self.split_x_y_variables_3()
        X = sm.add_constant(X)
        model3 = sm.OLS(Y, X).fit()
        model_summary = model3.summary(yname = "FTE",
                       xname = ("intercept", "New Jersey", "After April 1992",
                                "New Jersey and after April 1992",
                                "Burger King", "KFC", "Wendy's",
                                "Co-owned", "Central J", "South J"))
        return model_summary


    def model_summary_result(self, model_summary=None, model_name='did'):
        plt.rc('figure', figsize=(12, 7))
        # plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 12}) old approach
        plt.text(0.01, 0.05, str(model_summary), {'fontsize': 10},
                 fontproperties='monospace')  # approach improved by OP -> monospace!
        plt.axis('off')
        plt.tight_layout()
        image_path = 'assets/'+model_name+'.png'
        # image_path = io.BytesIO()  # in-memory files
        plt.savefig(image_path)
        # plt.close()
        # data = base64.b64encode(image_path.getbuffer()).decode("utf8")  # encode to html elements
        # return "data:image/png;base64,{}".format(data)
        return image_path

#
# if __name__ == "__main__":
#     did = DiD()
#     model_summary = did.create_first_model()
#     print(model_summary.as_text())
#     image = did.model_summary_result(model_summary)
#     print(dir(model_summary))










































































