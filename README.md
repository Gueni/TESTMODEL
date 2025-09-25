in my project i use lists like     X1 = [0, 1, 2]
    X2 = [0]
    X3 = [10, 20]
    X4 = [0, 0.5, 1.0]
    X5 = [0] etc ... as for example input voltage values , out power , temperature .... to feed them in my plecs model and simulate , so after sweep simulation is done i get a csv map matrix values in it the rows correspond to the iteration ( each iteration then correspond to combination of values from the X lists ) and the columns are for example rms current , rms voltage average power loss etc .... the csv hs no headers names so i have a list of headers to know .     csv_path = r'D:\WORKSPACE\BJT-MODEL\parameter_data.csv' # CSV produced by your sweeps (no header) . i want to generate an html report containing 3d plots if 2 or more of the X lists is not = to [0] or 2D plots else . i want the plots to be one subplots figure which has 2 columns so 2 plots side by side . for 3d i want to select which 2 X lists to vary and all the others to be constants (meaning for example for one 3d plot x axis is X2 and y axis is X5 and Z axis is the column from csv and inthe title of the 3d subplot it says for X1 = 10.5 , X3 = 5.3 etc... ) and for 2d it will be X axis is the only X list that is not = [0] and y axis is the columns from csv . i want the plots to be in an html file generated .here is the correct working code but manual in matlab i want to make one that is generic and automatic in python. if X2 = [0] in the json for example that means we did not use it so ignore it {

  "X1"            :  "[0]",
  "X2"            :  "[35,75]",
  "X3"            :  "[200,300]",
  "X4"            :  "[10.5,11.5]",
  "X5"            :  "[500]",
  "X6"            :  "[0]",
  "X7"            :  "[0]",
  "X8"            :  "[0]",
  "X9"            :  "[0]",
  "X10"           :  "[0]",
  "sweepNames"    :   ["X1","X2","X3","X4","X5","X6","X7","X8","X9","X10"],
  "Var1"          :   "X3",
  "Var2"          :   "X5",
  "startPoint"    :   "[0,35,200,10.5,500,0,0,0,0,0]",

  "permute"       :   true

} main is the code you gave me


the x and y axis are the names of the X lists and the z is the column from the csv , also this Traceback (most recent call last):
  File "d:\WORKSPACE\BJT-MODEL\data\phymos\main.py", line 603, in <module>
    main()
    ~~~~^^
  File "d:\WORKSPACE\BJT-MODEL\data\phymos\main.py", line 600, in main
    report.generate_html_report('automatic_plecs_report.html')
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "d:\WORKSPACE\BJT-MODEL\data\phymos\main.py", line 478, in generate_html_report
    figures = self.generate_automatic_plots()
  File "d:\WORKSPACE\BJT-MODEL\data\phymos\main.py", line 419, in generate_automatic_plots
    fig.layout.annotations[i].update(text=title)
    ~~~~~~~~~~~~~~~~~~~~~~^^^
IndexError: tuple index out of range and i want on figure with subplots 2 columns and n rows . and what you did is wrong 500 is not constant the logic is that each time you select 2 x lists which are varrying one for x axis and one for y axis and the rest of x lists will take from them one value of each as constat for example for 1 3d plot x2 x axis and x5 y axis and column no 3 from csv file as z axis and it the title of the subplot rms current for x1 =10.5 and x3 = 1500 and x4 = 35 ... and don't include the x = [0] because it was never used because it is empty