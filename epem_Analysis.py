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

#    Normalized = True #If false, the final result will be original event rate
    first_time = True #this is to initiate the Dataframe
     
    #Dataframe: count 0,1,2,2+ track and shower one by one
    column_header = ['Number_of_track','Number_of_shower']#column from the dataframe sorted_data
    
    ##---First, make a 2D histogram (ref: https://python-graph-gallery.com/83-basic-2d-histograms-with-matplotlib/)
    plt.hist2d(data[column_header[0]], y=data[column_header[1]],bins=(4,4),cmap=plt.cm.BuPu)
    plt.colorbar()
    plt.title('Correlation btw Number of Tracks and Number of Showers')
    plt.xlabel('Number of Tracks',fontsize=12)
    plt.ylabel('Number of Showers',fontsize=12)

    plt.savefig('2d_histogram.png', bbox_inches='tight')
    plt.clf()

    if True:#do more 2d_histogram!
	dir = '2dhistogram'
	if os.path.exists(dir)==False:
	    subprocess.call('mkdir '+dir ,shell=True)
	    print("A directory is created: " + os.getcwd() +"/"+dir)
	for angle in (0,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,120,150,180):
	    selected_data = data.loc[data['Angle'] == angle]
	    if selected_data.empty==False: 
	    	plt.hist2d(x=selected_data[column_header[0]], y=selected_data[column_header[1]],bins=(4,4),cmap=plt.cm.BuPu)
		plt.colorbar()
    	    	plt.title('Correlation btw Number of Tracks and Number of Showers: '+str(angle)+' degrees')
    	    	plt.xlabel('Number of Tracks',fontsize=12)
    	    	plt.ylabel('Number of Showers',fontsize=12)
	    	name = './2dhistogram/2d_histogram_angle_'+str(angle)+'.png'
    	    	plt.savefig(name, bbox_inches='tight',type='png',dpi=100)
		plt.clf()

	for p1 in (0.025,0.05,0.075,0.1,0.125,0.15):
	    selected_data = data.loc[data['E1'] == p1]
	    if selected_data.empty==False: 
		plt.hist2d(x=selected_data[column_header[0]], y=selected_data[column_header[1]],bins=(4,4),cmap=plt.cm.BuPu)
		plt.colorbar()
    	    	plt.title('Correlation btw Number of Tracks and Number of Showers: '+str(p1)+' GeV')
    	    	plt.xlabel('Number of Tracks',fontsize=12)
    	    	plt.ylabel('Number of Showers',fontsize=12)
	    	name = './2dhistogram/2d_histogram_energy_'+str(p1)+'.png'
    	    	plt.savefig(name, bbox_inches='tight')
		plt.clf()

    ##---2D histogram is made at this point, then continue counting 0,1,2,2+ track and shower one by one
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
	
    
    ##Set normalization for the plot
    ###Reference: (https://stackoverflow.com/questions/33791026/calculate-percent-value-across-a-row-in-a-dataframe)
    
    result.to_csv("sorted.csv", index = False)
    print("Sorted csv data see: sorted.csv")


    #plot event rate respected to energy
    for normalization in (0,1):
	Normalized = True if normalization == 0 else False

    	###delete 'Angle' column after summation respected to 'E1' column
    	energy_plot = result.groupby(['E1']).sum()
    	###drop the 'Angle' column
    	energy_plot = energy_plot.drop(energy_plot.columns[0],axis=1)#axis=1 is for column

    	if(Normalized):
    	    energy_plot = energy_plot.div(energy_plot.sum(1)/100.0,axis=0)#axis=0 is for index

    	energy_plot.plot(kind='bar',stacked=True,rot=0)#plot it!
    	energy_plot.to_csv("energy_plot.csv",index=True)#output it

    	####Below are configuration of the plot
    	#####Some tips: https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot/43439132#43439132

    	plt.xlabel('Energy of the Weak Shower (total energy is 0.3GeV) [Unit: GeV]',fontsize=12)
    	plt.ylabel('Event Rate',fontsize=12,rotation=0,position=(0,1))
    	plt.legend(bbox_to_anchor=(1.04,1),loc = "upper left")

    	if(Normalized):
    	    plt.title('Event Rate vs the Weak Shower Energy (normalized)')
    	    plt.savefig('energy_plot_nor.png', bbox_inches='tight')
    	else:
    	    plt.title('Event Rate vs the Weak Shower Energy')
    	    plt.savefig('energy_plot.png', bbox_inches='tight')
    	plt.clf()
    	
    	##REPEAT the plot by deleting 'E1'
    	angle_plot = result.groupby(['Angle']).sum()
    	angle_plot = angle_plot.drop(angle_plot.columns[0],axis=1)

    	if(Normalized):
    	    angle_plot = angle_plot.div(angle_plot.sum(1)/100.0,axis=0)

    	angle_plot.plot(kind='bar',stacked=True)#plot it!
    	angle_plot.to_csv("angle_plot.csv",index=True)#output it


    	plt.xlabel('Shower Open Angle [Unit: Degrees]',fontsize=12)
    	plt.ylabel('Event Rate',fontsize=12,rotation=0,position=(0,1))
    	plt.legend(bbox_to_anchor=(1.04,1),loc = "upper left")

    	if(Normalized):
    	    plt.title('Event Rate vs the Angle between e+e- (normalized)')
    	    plt.savefig('angle_plot_nor.png', bbox_inches='tight')
    	else:
    	    plt.title('Event Rate vs the Angle between e+e-')
    	    plt.savefig('angle_plot.png', bbox_inches='tight')
    	    
    	plt.clf()
    
    print("See two sets of pngs (with normalized plot as *nor.png): energy_plot.png and angle_plot.png, ")



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
    for (angle,event_rate) in [(26,18),(46,9),(60,5),(73,4),(84,3)]:# forwarding angle respected to z
				#26
	for energy_index in range(1,10): #[1,10), energy of the electron
	    for repeating in range(1,event_rate):
		unusual_events = counter(unusual_events)

		p1 = 0.3*energy_index/10.0
		#print("Angle: ",angle," with weight:",event_rate,"; electron energy:",p1)
		
		#Calculate e+e- angles (On shell):
		import math as math
		import random

		m = 0.064 # mass of Z' Boson
		pz=math.sqrt(math.pow(0.3,2)-math.pow(m,2)) # Z' Boson momentum
		p2=0.3-p1 # energy/momentum of positron
		
		# angles respected to z-axis
		angle_ep=math.acos((p1*p1+pz*pz-p2*p2)/(2*p1*pz))+math.radians(angle) #all in radiants
		angle_em=math.asin((pz*math.sin(math.radians(angle))-p1*math.sin(angle_ep))/p2)
		if 2*math.radians(angle)-angle_ep-angle_em>0.001:
		    # two values for the asin function.
		    angle_em=math.pi - math.asin((pz*math.sin(math.radians(angle))-p1*math.sin(angle_ep))/p2)
		
		#print("angles")
		#print(math.degrees(angle_ep),math.degrees(angle_em))

		open_angle=math.degrees(math.fabs(angle_ep-angle_em)) #(in radiants)
		
		### The projected unit vector of ep & em to xy-plane:
		u_ep = math.sin(angle_ep)
		u_em = math.sin(angle_em)
		
		### The orintation of the projected unit vector is random:
		rotation = random.random()*math.pi

		proj_xz= u_ep*math.cos(rotation)
		proj_yz= u_ep*math.sin(rotation)
		proj_xz2= u_em*math.cos(rotation)
		proj_yz2= u_em*math.sin(rotation)
		
		xz =math.degrees(math.atan2(proj_xz,math.cos(angle_ep))) #Theta0xz
		yz =math.degrees(math.atan2(proj_yz,math.cos(angle_ep))) #Theta0yz

		xz2=math.degrees(math.atan2(proj_xz2,math.cos(angle_em))) #Theta0xz2
		yz2=math.degrees(math.atan2(proj_yz2,math.cos(angle_em))) #Theta0yz2
		
#		print(p1,xz,yz,p2,xz2,yz2)

		subprocess.call('echo "\nForwarding Angle: ' + str(angle) +'" >> result.txt',shell=True)
		subprocess.call('echo "Energy: ' + str(p1) +'" >> result.txt',shell=True)
		subprocess.call('echo "Open Angle: ' + str(open_angle) +'" >> result.txt',shell=True)
	    	print("\nProducing events with Forwarding Angle: "+str(angle)+", Electron Energy: "+ str(p1)+", Open Angle: "+str(open_angle)+".")

	    	file = open("epem_pair.fcl","r") #Fixed as reference
	    	fLar = open(fclfile,"w+")
            	line_fcl = file.readline()
            	while line_fcl:
		    if "P0" in line_fcl:
                        fLar.write("physics.producers.generator.P0: [" + str(p1) + "," + str(p2) +"]\n") #change momentum
                    elif "Theta0XZ" in line_fcl:
                        fLar.write("physics.producers.generator.Theta0XZ: [" + str(xz) + ","+str(xz2)+"]\n") #change angle
                    elif "Theta0YZ" in line_fcl:
                        fLar.write("physics.producers.generator.Theta0YZ: [" + str(yz) + ","+str(yz2)+"]\n") #change angle
                    else:
                        fLar.write(line_fcl)
                    line_fcl = file.readline()
		file.close()
            	fLar.close()
#	    	subprocess.call('. generate.sh', shell=True)
    print(unusual_events)
    

	    #pick out suspecious events
#	    subprocess.call('echo "N Tracks: 3" >> result.txt',shell=True)
#	    subprocess.call('echo "N Showers: 4" >> result.txt',shell=True)
#	    suspicious_count = inspector("result.txt")

#	    if (suspicious_count > unusual_events):
#		unusual_events = suspicious_count		
#		subprocess.call('echo "BANG"',shell=True)
#		subprocess.call('mv ./*reco2.root ./events/',shell=True)
def counter(a):
    return a+1

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
EventGenerator('./e_plus_e_minus.fcl')

#2. The following extracts information from the result.txt and produce a *.csv file
##Format: (<str>input_file, <str> output_file, <int> n) Same n as Event Generator
#Analyzer("./summary.txt","./summary.csv")

#3. The following sumarizes the extracted info. in *.csv and produce two plots in pngs format.
##Format: (<str> input)
#Summarizer("summary.csv") #NO PANDAS IN FERMILAB SERVER...
