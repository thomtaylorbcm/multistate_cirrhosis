# multistate_cirrhosis
This repository contains Risk Profiling Application (RPA) for modeling forward progression through states of liver disease, including development of Ascities, Hepatic Encephalopathy, Varicael Bleeding, Hepatocellular Carcinoma (HCC) and Death, 

## Description
### Modeling Context
This model is based on a cohort of patients with confirmed cirrhosis who are followed through time in care within the U.S. Department of Veterans Affairs Veterans Health Administration health care systems. Further details of the project, data extration, and data characterization are available at at the [VA HSR&D 
Project Website](https://www.hsrd.research.va.gov/research/abstracts.cfm?Project_ID=2141706339). This resource contains papers and publications emanating from this project.

### Data Sources
The data source for all analyses is the VA Corporate Data Warehouse. Data are not publicly available. 

### Analyses
Analyses and exact cohort details are currently in the manuscript preparation phase. However, currently, a large 8 state, 22 transition model is the source for this Risk Profiling Application. Python Plotly and Dash are the primary APIs used for risk profiling. The unit of analysis is the month within each patient. The forward transition model is depicted below. The starting state for all patients was Compensated Cirrhosis. In each month, a patient could progress to any of 7 other states (or not progress, i.e., stay in the same state). Multistate transition intensities were computed with Accelerated Failure Time (AFT) models for transition intensities across observable time in each patient using the exponential distribution and time-homogenous forward progression of time from index date of compensated cirrhosis. Subsequent to fitting each of the 22 AFTs, we fit a multistate model. Analyses were conducted in R 4.12 in the VA's Research platform (VINCI). 

The resulting multistate model provides risk predictions across time for a patient base on her/his state are the estimates that can be queried in this Risk Profiling Application. 

#### Forward Progression Multistate Model Specified:
![forward progression](https://github.com/thomtaylorbcm/multistate_cirrhosis/assets/158203493/5c674816-2379-4e88-bdcd-099edd2bfb62")




### Estimates

