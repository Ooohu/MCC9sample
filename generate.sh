#! /bin/bash
# run the generator for a single proton in the MicroBooNE geometry
# all lar commands, is successful, will end with a line - Art has completed and will exit with status 0.

number=30 

rm *.root &> /dev/null

echo $'START!!! Create event generator!' | tee -a record.txt
lar -n $number -c e_plus_e_minus.fcl &>> record.txt

echo $'\nFINISH!!! Run GEANT4 to produce events based on the generator.' | tee -a record.txt
# run GEANT4 on the output of the generator made above.
lar -n $number -c wirecell_g4_uboone.fcl -s ./*gen.root &>> record.txt


# run the detector simulation on the G4 output.
# This generates waveforms on the wires, adds noise, digitizes and zero-suppresses the output
echo $'\nFINISH!!! Run detector simulation.' | tee -a record.txt
lar -n $number -c wirecell_detsim_uboone.fcl -s ./*g4.root &>> record.txt
 
echo $'\nFINISH!!! (Run reco1) Reconstruct events from the detector simulation.' | tee -a record.txt&>> record.txt
lar -n $number -c reco_uboone_mcc9_8_driver_stage1.fcl  -s ./*detsim.root &>> record.txt

echo $'\nFINISH!!! (Run mc2D) Reconstruct events from reco1 stage.' | tee -a record.txt
lar -n $number -c standard_larcv_uboone_mc2d_prod.fcl  -s ./*reco1.root &>> record.txt

echo $'\nFINISH!!! (Run reco2) Reconstruct events from postdlmc stage.' | tee -a record.txt
lar -n $number -c reco_uboone_mcc9_8_driver_stage2.fcl  -s ./*postdlmc.root &>> record.txt


echo $'\nFINISH!!! Output events info..' | tee -a record.txt
lar -n $number -c run_PandoraEventDump.fcl -s ./*reco2.root | tee -a result.txt

#the following line cost too much memory
#mv ./*reco2.root ./events/

echo $'\nGEORGIAK with' $number 'events' >> result.txt
date >> result.txt

echo $'\n\n\nFINISH!!! and see result.txt for detail!'




