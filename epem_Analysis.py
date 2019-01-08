import os, subprocess

def Analyzer(filename):
    
    number_repeat = 3 #number of events in each production circle (generate.sh)
    energy_repeat = 6 #number of steps in energy

    fp = open(filename,"r")
    output_file = "shower_count_new.csv"
    f_csv = open(output_file , "w+")#output file name
    line = fp.readline() #line is a string
    f_csv.write("Angle E1 Number_of_track Number_of_shower\n")
    energy_count = 1 #Track energy
    event_repeat = 0 #Track each event

    while line:
	if "Angle:" in line:
	    angle=line
	   # energy_count = 0 #Reset energy 
	    energy_count = 1

	if "N Tracks" in line:
	    energy = 0.15*((energy_count+1.0)/energy_repeat)#6 is given by the value n of the EventGenerator
	    energy_output = str(energy) + " "
	    
	    f_csv.write(NumberReader(angle))
	    f_csv.write(energy_output) #output energy of the weak shower
	    f_csv.write(NumberReader(line))

        if "N Showers" in line:
	    f_csv.write(NumberReader(line))

	    f_csv.write("\n")#read the shoower as the last input in row
	    event_repeat=event_repeat+1
	    if event_repeat == number_repeat:
		#Update energy if the event_repeat reach 33 (0~32 events have been proceeded)
		energy_count=energy_count + 1
		event_repeat=0

	    #if energy_count == 6:#A energy loop is finished
	    #	energy_count=0

        line = fp.readline()#Next line
    fp.close()
    f_csv.close()
    print("Successful output: "+ output_file)


def NumberReader(current_line):#Read off number from a line and insert a space behind
    string = [int(s) for s in current_line.split() if s.isdigit()][0]
    output =str(string) + " "
    return output


def EventGenerator(fclfile, angle_min, angle_max, step, n):
    #step is the angle step
    #n is the energy step, 33 events in each n
#    for angle in range(angle_min, angle_max + 1, step):
    for angle in (0,10,30,90,180):
	    subprocess.call('echo "Angle: ' + str(angle) +'" >> result.txt',shell=True)
#            for i in range (n):#from 0 to n-1
            for i in range (1,n-1):#from 0 to n-1
                p1 = 0.15 *((i + 1.0) / n)
                p2 = 0.3 - p1
		print("Producing events with Angle: "+str(angle)+", Energy: "+ str(p1)+".")
		r = p1 / p2
                file = open(fclfile,"r")
                fLar = open("epem_pair.fcl","w+")
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
EventGenerator('./e_plus_e_minus.fcl',100,180,10,6)
Analyzer("./result.txt")
