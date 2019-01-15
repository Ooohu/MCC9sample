import os, subprocess

#PLOT
def Summarizer(filename):
    import pandas as pd
    import matplotlib.pyplot as plt

    #turns csv into a dataframe type in pandas
    data = pd.read_csv(filename, sep=',') #with argument header=0 as default
    
    #prepare the data frame for frequency count
    sorted_data=data.groupby(['Angle','E1'],sort=True)
    result=pd.DataFrame()#an empty dataframe for storing the sorted dataframe
    first_time = True
     
    #count 0,1,2,2+ track and shower one by one
    column_header = ['Number_of_track','Number_of_shower']#column from the dataframe sorted_data
    
    
    ## First Make a 2D histogram (ref: https://python-graph-gallery.com/83-basic-2d-histograms-with-matplotlib/)

    plt.hist2d(data[column_header[0]], y=data[column_header[1]],bins=(4,4),cmap=plt.cm.BuPu)
    plt.colorbar()
    plt.title('Correlation btw Number of Tracks and Number of Showers')
    plt.xlabel('Number of Tracks',fontsize=12)
    plt.ylabel('Number of Showers',fontsize=12)

    plt.savefig('2d_histogram.png', bbox_inches='tight')


    ##continue counting 0,1,2,2+ track and shower one by one
    track_or_shower = ['track','shower']
    for index in range(0,2): #this loops track and shower; i.e. index=0,1
	for i in range(0,3): #started from i=0, do i+1 3 times; i.e. i=0,1,2
	    new_column_header = str(i)+' '+track_or_shower[index] #name for the new column
	    #the following line sort the original dataframe with a new column
	    update = sorted_data[column_header[index]].apply(lambda x:(x==i).sum()).reset_index(name = new_column_header)
	    if first_time:
		result = update	
		first_time = False
	    else:
		result = result.join(update[new_column_header])
    	#for the 2+ case: 
	new_column_header = '2+ '+track_or_shower[index]
    	update = sorted_data[column_header[index]].apply(lambda x:(x>2).sum()).reset_index(name = new_column_header)
    	result = result.join(update[new_column_header])

#   print(result)

    #plot event rate respected to energy
    ##delete 'Angle' column after summation respected to 'E1' column
    energy_plot = result.groupby(['E1']).sum()
    ##drop the 'Angle' column
#   energy_plot = pd.read_csv("energy_nor.csv")
    energy_plot = energy_plot.drop(energy_plot.columns[0],axis=1)

#   energy_plot.to_csv("energy.csv") #this is used to calculate percentage manually

    energy_plot.plot(kind='bar',stacked=True,rot=0)#plot it!
    ###Below are configuration of the plot
    ####Some tips: https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot/43439132#43439132
    plt.title('Event Rate vs the Weak Shower Energy')
    plt.xlabel('Energy of the Weak Shower (total energy is 0.3GeV) [Unit: GeV]',fontsize=12)
    plt.ylabel('Event Rate',fontsize=12,rotation=0,position=(0,1))
    plt.legend(bbox_to_anchor=(1.04,1),loc = "upper left")

    plt.savefig('energy_plot.png', bbox_inches='tight')
    
    ##REPEAT
    angle_plot = result.groupby(['Angle']).sum()
#    angle_plot = pd.read_csv("angle_nor.csv")
    angle_plot = angle_plot.drop(angle_plot.columns[0],axis=1)
#    angle_plot.to_csv("angle.csv") #this is used to calculate percentage manually

    angle_plot.plot(kind='bar',stacked=True)#plot it!

    plt.title('Event Rate vs Shower Open Angle')
    plt.xlabel('Shower Open Angle [Unit: Degrees]',fontsize=12)
    plt.ylabel('Event Rate',fontsize=12,rotation=0,position=(0,1))
    plt.legend(bbox_to_anchor=(1.04,1),loc = "upper left")

    plt.savefig('angle_plot.png', bbox_inches='tight')
    
    print("See two pngs: energy_plot.png and angle_plot.png")

    #Now try to do it with percentage. or..not

	
#EXTRA INFORMATION FROM OUTPUT
def Analyzer( filename, output_file):

    fp = open(filename,"r")
    f_csv = open(output_file , "w+")
    line = fp.readline() #line is a string
    f_csv.write("Angle,E1,Number_of_track,Number_of_shower\n")

    while line:
	if "Angle" in line:
	    angle = line

	if "Energy" in line:
	    energy = line

	if "N Tracks" in line:
	    f_csv.write(NumberReader(angle))
	    f_csv.write(NumberReader(energy)) #output energy of the weak shower
	    f_csv.write(NumberReader(line))

        if "N Showers" in line:#dont load this with extra delimiter
	    special = [int(s) for s in line.split() if s.isdigit()][0]
	    f_csv.write(str(special)+"\n")

        line = fp.readline()#Next line
    fp.close()
    f_csv.close()
    print("Successful output: "+ output_file)


#FOR Analyzer only
def NumberReader(current_line):#Read off number from a line and insert a space behind
    import re
    string = re.findall(r"\d*\.\d+|\d+",current_line)[0]#including decimal
    output =str(string) + ","
    return output

#EVENT GENERATION
def EventGenerator(fclfile):
    #exclude case of 0 degree at 150 MeV
    unusual_events = 0 #keep track of unusual events (4+ tracks or showrs)
    for angle in (0,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,120,150,180):
	for p1 in (0.025,0.05,0.075,0.1,0.125,0.15):

	    subprocess.call('echo "Angle: ' + str(angle) +'" >> result.txt',shell=True)
	    subprocess.call('echo "Energy: ' + str(p1) +'" >> result.txt',shell=True)
            p2 = 0.3 - p1
	    print("Producing events with Angle: "+str(angle)+", Energy: "+ str(p1)+".")

	    file = open("epem_pair.fcl","r") #Fixed as reference
	    fLar = open(fclfile,"w+")
            line_fcl = file.readline()
            while line_fcl:
                if "P0" in line_fcl:
                    fLar.write("physics.producers.generator.P0: [" + str(p1) + "," + str(p2) +"]\n") #change momentum
                elif "Theta0XZ" in line_fcl:
                    fLar.write("physics.producers.generator.Theta0XZ: [" + str(angle) + ",0]\n") #change angle
                else:
                    fLar.write(line_fcl)
                line_fcl = file.readline()
            file.close()
            fLar.close()
            subprocess.call('. generate.sh', shell=True)
	    #pick out suspecious events
#	    subprocess.call('echo "N Tracks: 3" >> result.txt',shell=True)
#	    subprocess.call('echo "N Showers: 4" >> result.txt',shell=True)
	    suspicious_count = inspector("result.txt")

	    if (suspicious_count > unusual_events):
		unusual_events = suspicious_count		
#		subprocess.call('echo "BANG"',shell=True)
		subprocess.call('mv ./*reco2.root ./events/',shell=True)

##This is used to check result.txt
def inspector(file_name):
    fp = open(file_name,"r")
    line = fp.readline() #line is a string
    suspicious_count = 0
    while line:
	if ("N Tracks" in line) or ("N Showers" in line):
	    number = [int(s) for s in line.split() if s.isdigit()][0]
	    if (number > 3):
		suspicious_count = suspicious_count + 1
	line = fp.readline() #line is a string
	if line=='':
	    fp.close()
	    return suspicious_count
	   

#-------------------------------------------EXECUTION HERE-----------------------------------------
#1. The following generate events, produce an result.txt
##Format: (<str> fcl_file)
#EventGenerator('./e_plus_e_minus.fcl')

#2. The following extracts information from the result.txt and produce a *.csv file
##Format: (<str>input_file, <str> output_file, <int> n) Same n as Event Generator
#Analyzer("./result.txt","./result.csv")

#3. The following sumarizes the extracted info. in *.csv and produce two plots in pngs format.
##Format: (<str> input)
Summarizer("summary.csv") #NO PANDAS IN FERMILAB SERVER...
