------------------------------------------------ GROUP E---------------------------------------------

Andreia Taboleiros - M20200581
Raquel Castro - R2015528
Ricardo Santos - M20200620
Tiago Faria - M20190773

-----------------------------------------------------------------------------------------------------

For a better organization and in order for the Plotly Dash dashboard to work, the files must be organized into several folders.
This readme file will help you navigate the folders and understand what each file do.

-------------------------------------------FOLDERS-------------------------------------------------

Assets - This folder contains the css code for the dashboard.

Databases - This folder contains all the csv and sav files that are created and used throughout the project. 
Due to size contraints of moodle this folder was sent empty, however there is the possibility to download all the files
using the following link to a onedrive shared folder.

-------Link to the Databases-----
https://liveeduisegiunl-my.sharepoint.com/:f:/g/personal/m20190773_novaims_unl_pt/EoW102J6_d9DimUhShp8il8BwflIyG4THBgpB7-0BjxX4w?e=uUSf4y
---------------------------------

To run the dashboard, the following files are necessary --> final_df ; complementary_df ; substitutes_df
These datasets must be inside the Databases folder for the dashboard to work, unless you change the path on the dashboard.

HTML notebook files - In this folder are all the html files of each of the notebooks in case there are some problems reading the .ipynb files

models -  This folder contains all the .ipynb files used in the project:
	Notebook 1 - Feature enginnering and original dataframe size reduction. (inputs -> original_df, outputs -> df_treated)
	Notebook 2 - Cluster creation (inputs -> df_treated, outputs -> df_clusters)
	Notebook 3 - Association Rules (inputs -> df_clusters, outputs -> complementary, substitutes)
	Notebook 4 - Data Exploration (inputs -> df_clusters, outputs -> dashboard charts)
	Notebook 5 - Forecasts (inputs -> df_clusters, outputs -> prediction models)
		     Each subset (5.1, 5.2, 5.3) represents a different forecast method, with 5.3 being the chosen method
	Notebook 6 - Forecasts (input -> prediction models (QT.sav and new_prediction_data.sav), outputs -> predicitons)

------------------------------------------DASHBOARD------------------------------------------------
The dashboard is not online due to size restrictions, to view and interact with the dashboard it is necessary to run the app.py file.
However the jpeg file 'Dashboard_not-Interactive.jpeg' is a full picture of the entire dashboard, so that you can check the dashboard without running the .py file.

app.py - Run this file to access the dashboard. It will open a server on port= 8050
	 To run the dashboard it is necessary to have final_df, complementary_df, substitutes_df on the Databases folder.

-----------------------------------------Predictions-----------------------------------------------
Due to libray incompatibilities we were not able to implement the forecast in the Dashboard, so we created a simple notebook that allows to quickly make the forecasts.
In order for the predicitons to work, it is necessary for the files 'QT.sav' and 'new_prediction_data.sav' to be present in the Databasesf older 