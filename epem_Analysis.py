import os, subprocess, random
#filename = "/Users/simontsui/Desktop/result.txt"
#fclfile = "/Users/simontsui/Desktop/epem_pair.fcl"

def Analyzer(filename):
    fp = open(filename,"r")
    f_csv = open("shower_count.csv","w+")
    line = fp.readline()
    while line:
	if "Angle:" in line:
	    f_csv.write(line)
        elif "N Showers" in line:
            n_shower = [int(s) for s in line.split() if s.isdigit()][0]
            f_csv.write(str(n_shower))
            f_csv.write("\n")
        line = fp.readline()
    fp.close()
    f_csv.close()

def EventGenerator(fclfile, angle_min, angle_max, step, n):
    for angle in range(angle_min, angle_max + 1, step):
	    subprocess.call('echo "Angle: '+str(angle)+'" >> result.txt',shell=True)
            for i in range (n):
                p1 = random.uniform(0, 300)
                p2 = 300 - p1
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
                subprocess.call('. generate.sh',shell=True)

EventGenerator('./e_plus_e_minus.fcl',0,5,1,10)
Analyzer('./result.txt')
