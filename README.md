# east
A script for finding crystal orientation from a couple of wedges.


### Dependencies
East requires a recent build of [DIALS](https://dials.github.io/installation.html) and uses the included Python interpreter to run. Do not try to run East with your own Python interpreter.


# Usage Example
East only needs two pieces of info to refine a scan static model of crystal geometry. 

### Gain Setting
Firstly, an appropriate gain setting must be supplied using the `-g` option.
The gain is available from the detector manufacturer. 
For photon counting detectors (Dectris Pilatus or Eiger), 1 is the optimal gain setting. 

### Space Group
A space group number which is an integer suppplid with the `-s` flag. 
For instance, `-s 19` for `P212121`.

### Run East on Sample Data
6 is a reasonable gain setting for the included sample data which is two wedges in space group 19.
To run east, just type:

`./east -s 19 -g 6. data/A1_0deg_1_000??.mccd data/A1_90deg_2_000??.mccd`

to output the following analysis:
    nalysis of wedge starting with image: /home/kmdalton/opt/east/data2/A1_0deg_1_00001.mccd   
    goniometer rotation axis: (1.0, 0.0, 0.0)                                                   
    incoming beam wavevector: (-0.00039032492293883766, 0.0, -0.8368269953886467)               
    first image phi: 81.02                                                                      
    Real space axes at phi:81.02                                                                
        A axis:   -51.387,    2.823,   -4.439                                                   
        B axis:     6.252,   22.047,  -58.353                                                   
        C axis:    -1.454,  -65.830,  -25.027                                                   
                                                                                                
                                                                                                
    Analysis of wedge starting with image: /home/kmdalton/opt/east/data2/A1_90deg_2_00001.mccd  
    goniometer rotation axis: (1.0, 0.0, 0.0)                                                   
    incoming beam wavevector: (-0.00039032492293883766, 0.0, -0.8368269953886467)               
    first image phi: 171.02                                                                     
    Real space axes at phi:171.02                                                               
        A axis:   -51.387,    4.439,    2.823                                                   
        B axis:     6.252,   58.353,   22.047                                                   
        C axis:    -1.454,   25.027,  -65.830                                                   

