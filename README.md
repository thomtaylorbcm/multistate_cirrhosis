# multistate_cirrhosis
This repository contains Risk Profiling Application (RPA) for modeling forward progression through states of liver disease, including development of Ascities, Hepatic Encephalopathy, Varicael Bleeding, Hepatocellular Carcinoma (HCC) and Death, 

## Description
### Modeling Context
This model is based on a cohort of patients with confirmed cirrhosis who are followed through time in care within the U.S. Department of Veterans Affairs Veterans Health Administration health care systems. Further details of the project, data extration, and data characterization are available at at the [VA HSR&D 
Project Website](https://www.hsrd.research.va.gov/research/abstracts.cfm?Project_ID=2141706339). This resource contains papers and publications emanating from this project.

### Data Sources
The data source for all analyses is the VA Corporate Data Warehouse. Data are not publicly available. We refer interested readers to data characterization the [VA HSR&D 
Project Website](https://www.hsrd.research.va.gov/research/abstracts.cfm?Project_ID=2141706339) to understand data characterization while the manuscript is currently under review. 

### Analyses
Analyses and exact cohort details are currently in the manuscript preparation phase. However, currently, a large 8 state, 22 transition model is the source for this Risk Profiling Application. Python Plotly and Dash are the primary APIs used for risk profiling. The unit of analysis is the month within each patient. The forward transition model is depicted below. The starting state for all patients was Compensated Cirrhosis. In each month, a patient could progress to any of 7 other states (or not progress, i.e., stay in the same state). Multistate transition intensities were computed with Accelerated Failure Time (AFT) models for transition intensities across observable time in each patient using the exponential distribution and time-homogenous forward progression of time from index date of compensated cirrhosis. Subsequent to fitting each of the 22 AFTs, we fit a multistate model. Models were fit adjusting for patient time-varying age (age at entry to a given state) as well as the cirrhosis etiology including 1) Alcohol, 2) Metabolic dysfunction-Associated Steatohepatitis (MASH), 3) Hepatitis C (HCV), or 4) Alcohol + HCV. Analyses were conducted in R 4.12 in the VA's Research platform (VINCI). Risk estimates were then exported from this secure system in CSV form. These risk predictions are accessible in this repository. Further detail of the files are below. 

The resulting multistate model provides risk predictions across time for a patient base on her/his state are the estimates that can be queried in this Risk Profiling Application. 

#### Forward Progression Multistate Model Specified
![forward progression](https://github.com/thomtaylorbcm/multistate_cirrhosis/assets/158203493/5c674816-2379-4e88-bdcd-099edd2bfb62")

### Data Source for Risk Profiling Application
The main file for all profiling is a serialized pickle Python file based on a CSV exported from multistate modeling completed in the VA's non-public VINCI platform. 
- stacked_multistate_model_risk_probabilities.csv
- stacked_multistate_model_risk_probabilities.pkl

### Main .py application script
- app.py
  - This file references the pkl file above and the application associated CSS file in this repo.
  - If run, it *should* launch a browser on port 8050 on the local machine with the Risk Profiling Application



