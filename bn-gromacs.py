#!/usr/bin/python
from optparse import OptionParser
import os
import sys
import shutil
import subprocess


# user settings 
g_prefix='g_'


#developer var
version = "1.0a"

def LicenseInfo(): 
    print """
            ***************************************
            [  BIONERD GROMACS AUTOMATION SCRIPT  ]
            ***************************************
            Version """+ version +"""
            Author: Ravi Raja T. Merugu
            raviraja.merugu@gmail.com
            Copyrights (c) 2013, RSquareLabs Org
            check out http://www.rsquarelabs.org/works/bngromacs-py/index for more information.
            
              **** CHEERS & HAPPY RESEARCH :) ****
    
This program is free software; you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the  rsquarelabs.org;
either version 2 of the License, or (at your option) any later version.Do not remove
the original authors name & credits in redistributions or modified version.

    """
def CheckFile(filename):
    try:
        open(filename)
        print "CHEERS: %s found" % filename
    except IOError as e:
        print "ERROR: %s" % e
        #errflag=1
    

LicenseInfo()
parser = OptionParser(usage="usage: %prog [options] filename", version="%prog "+version)
parser.add_option("-l", "--ligand",
                      action="store",
                      metavar=" ",
                      dest="LigFilename",
                      default="ligand.gro",
                      help="Input a ligand file [*.gro]")
parser.add_option("-i", "--itp",
                      action="store",
                      metavar=" ",
                      dest="LigFilename2",
                      default="ligand.itp",
                      help="Input a ligand topology file [*.itp]")
parser.add_option("-p", "--protein",
                      action="store",
                      metavar=" ",
                      dest="ProtFilename",
                      default="protein.pdb",
                      help="Input a protein file (default:protein.pdb)")
parser.add_option("-w", "--wdir",
                      action="store",
                      metavar=" ",
                      dest="wdir",
                      default="work",
                      help="Working Directory of project (default:work)")
parser.add_option("-v","--verbose",
                       action="store_true",
                       dest="verbose",
                       default=True,
                       help="Loud and Noisy[default]")
parser.add_option("-q","--quiet", 
                      action="store_false",
                      dest="verbose",
                      help="Be vewwy quit")

(options, args) = parser.parse_args()
print "args "+ str(len(args))
if len(args) == 3:
    parser.error("wrong number of arguments")
    
global protein, ligand, liganditp
protein=options.ProtFilename
ligand=options.LigFilename
liganditp=options.LigFilename2
wdir=options.wdir+"/"


def ExitProgram():
    print """
    *****************************************************
     HEADS UP: PROGRAM ENCOUTERED SERIOUS ERRORS
    *****************************************************
    THANKS FOR USING BNGROMACS version"""+ version + """
            DONT FORGET TO CITE bngromacs.py 
                raviraja.merugu@gmail.com
            Copyright (c) 2012, rsquarelabs.org
      Find more info at http://www.rsquarelabs.org/tools/bngromacs.php
    ******************************************************
"""
    sys.exit()
    
"""
def RunProcess(StepNo, StepName,command):
    print "\n\n"
    print "INFO: Attempting to execute "+ StepName + " [STEP:"+StepNo+"]" 
    #print "................................................................."
    #command
    #print command
    if (os.system(command)):
        print "HEADS UP: FAILED/INTEREPTED TO COMPLETE STEP["+StepNo+"] :( "
    else:
        print "CHEERS: STEP["+StepNo+"] SUCCESSFULLY COMPLETED :)"
        print "******************************************************************\n\n\n"
    #print command
""" 
def RunProcess(StepNo, StepName,command):
    print "\n\n"
    print "INFO: Attempting to execute "+ StepName + " [STEP:"+StepNo+"]" 
    ret=subprocess.call(command,shell=True)
    if ret!=0:
        if ret<0:
            print "HEADS UP: Killed by signal :(",-ret
            ExitProgram()
        else:
            print "HEADS UP: Command failed with return code",ret
            ExitProgram()
    else:
        print "CHEERS: STEP["+StepNo+"] SUCCESSFULLY COMPLETED :)"
        print "******************************************************************\n\n\n"
 

def GatherFiles():
    print "STEP0: Checking Files needed for Simulation"
    print "Checking Protein File" 
    global protein, ligand, liganditp
   
    print protein
    print ligand
    print liganditp
    try:
        open(protein)
        print "CHEERS: PROTEIN FILE \t\t'"+ protein +"' FOUND "
    except IOError as e:
        print "ERROR: PROTEIN FILE \t\t'" + protein +"' NOT FOUND"
        print e
    #print "Checking Ligand File"
    try:
        open(ligand)
        print "CHEERS: LIGAND FILE \t\t'"+ ligand +"' FOUND"
    except IOError as e:
        print "ERROR: LIGAND FILE \t\t'"+ ligand + "' NOT FOUND"
        
    #print "Checking Ligand topology file"
    try:
        open(liganditp)
        print "CHEERS: LIGAND TOPOLOGY FILE \t'"+ liganditp + "' FOUND"
    except IOError as e:
        print "ERROR: LIGAND TOPOLOGY FILE \t'"+ liganditp + "' NOT FOUND"
    #print "\n"
    print "CREATING A WORKING DIRECTORY WITH NAME "+ wdir +" ."
    if os.path.isdir(wdir):
        print "Folder '"+wdir + "' Aready exist"
        if os.path.isdir("BACKUP"):
            print "ERROR: Backup folder already exists :( "
            print """
POSSIBLE SOLUTION: A backup folder already present. 
You may loose your work if we replace , so change your 
Working Directory (other than '"""+wdir+ """' ) or delete the
folder BACKUP"""
            ExitProgram()
        else:
            if (os.rename(wdir, "BACKUP")):
                print "Old "+wdir +" was moved to BACKUP/"
        #ExitProgram()
        
    os.mkdir(wdir)
    print "CHEERS: Working Directory "+ wdir +" created Successfully :)"
    print "Moving the files to Working Directory" + wdir
    shutil.copy2(protein,wdir+"protein.pdb")
    shutil.copy2(ligand,wdir+"ligand.gro")
    shutil.copy2(liganditp,wdir+"ligand.itp")
    
    print "***********************************************"
    print "SCRIPT LOADED WITH AMMO *** TIME TO ROCK N ROLL"
    print "***********************************************"
    print "GOOD LUCK :)"
    print "\n"
        
# generating topology of protein
def pdb2gmx_proc():
    print ">STEP1 : Initiating Procedure to generate topology for protein"
    pdb2gmx = g_prefix+"pdb2gmx"
    StepNo = "1"
    StepName = "Topology Generation"
    command=pdb2gmx+" -f "+ wdir+"protein.pdb -o "+wdir+"protein.gro -ignh -p "+ wdir+"topol.top -i "+ wdir+"posre.itp -ff gromos53a6 -water spc >> " + wdir+"step1.log 2>&1"    
    RunProcess(StepNo, StepName, command)
    #system.


def PrepareSystem():
    print ">STEP2 : Initiating Precedure to make system[Protein+Ligand]"
    startFromLine = 3 # or whatever line I need to jump to
    protein=wdir+"protein.gro"
    system=wdir+"system.gro"
    ligand=wdir+"ligand.gro"
    ProteinFh = open(protein, "r", 0)
    LigandFh = open(ligand, "r", 0)
    SystemFh = open(system,'wa',0)

    #get the last line of protein 

    #get the count of Protein and Ligand files 
    CountProteinLines = len(ProteinFh.readlines())
    CountLigandLines = len(LigandFh.readlines())

    #print CountProteinLines 
    #print CountLigandLines

    #count of the system
    SystemCount= CountProteinLines + CountLigandLines -6
    #print SystemCount
    ProteinFh.close()
    LigandFh.close()
    
    #open files for reading 
    ProteinFh = open(protein, "r", 0)
    LigandFh = open(ligand, "r", 0)

    SystemFh.write("System.gro Designed for Simulation by [bngromacs.py]\n")
    SystemFh.write(str(SystemCount)+"\n")

    linesCounter = 1
    for line in ProteinFh:
        if linesCounter in range(startFromLine, CountProteinLines):# startFromLine :
            #print line
            SystemFh.write(line)
        linesCounter += 1
    ProteinFh.close()


    linesCounter = 1
    for line in LigandFh:
        if linesCounter in range(startFromLine, CountLigandLines):
            #print line
            SystemFh.write(line)
        linesCounter +=1

            #get the last line of protein [the coordinates of the center]    
    ProteinFh = open(protein, "r", 0)    
    LastLine = ProteinFh.readlines()[-1]
    #print LastLine
    SystemFh.write(LastLine)
    print "CHEERS: system.gro WAS GENERATED SUCCESSFULLY"

    
    
    f1 = open(wdir+'topol.top', 'r')
    f2 = open(wdir+'topol_temp.top', 'w')
    for line in f1:
        f2.write(line.replace('; Include water topology', '; Include Ligand topology\n #include "ligand.itp"\n\n\n; Include water topology '))
    f1.close()
    f2.close()
    #swaping the files to get the original file    
    f1 = open(wdir+'topol.top', 'w')
    f2 = open(wdir+'topol_temp.top', 'r')
    for line in f2:
        f1.write(line)
    f1.write("UNK        1\n")
    f1.close()
    f2.close()
    os.unlink(wdir+'topol_temp.top')
    print "INFO: Topology File Updated with Ligand topology info "
    print "CHEERS: STEP[2] SUCCESSFULLY COMPLETED :)\n\n\n"

def SolvateComplex():
    #editconf -f system.gro -o newbox.gro -bt cubic -d 1 -c
    #genbox -cp newbox.gro -cs spc216.gro -p topol.top -o solv.gro


    print ">STEP3 : Initiating Procedure to Solvate Complex"
    editconf = g_prefix+"editconf"
    StepNo = "3"
    StepName = "Defining the Box"
    command = editconf + " -f "+ wdir+"system.gro -o "+ wdir+"newbox.gro -bt cubic -d 1 -c >> " + wdir+"step3.log 2>&1"
    RunProcess(StepNo, StepName, command)   

    print ">STEP4 : Initiating Procedure to Solvate Complex"
    genbox = g_prefix+"genbox"
    StepNo = "4"
    StepName = "Solvating the Box"
    command = genbox + " -cp "+ wdir+"newbox.gro -p "+ wdir+"topol.top -cs spc216.gro -o "+ wdir+"solv.gro >> " +wdir+"step4.log 2>&1"
    RunProcess(StepNo, StepName, command)           

def WriteEmMdp():
    print ">NOTE: Writing em.mdp"
    fh=open(wdir+"em.mdp","w")
    data="""
; LINES STARTING WITH ';' ARE COMMENTS
title         = Minimization    ; Title of run

; Parameters describing what to do, when to stop and what to save
integrator    = steep        ; Algorithm (steep = steepest descent minimization)
emtol         = 100.0      ; Stop minimization when the maximum force < 1.0 kJ/mol
emstep        = 0.01      ; Energy step size
nsteps        = 50000          ; Maximum number of (minimization) steps to perform
energygrps    = system    ; Which energy group(s) to write to disk

; Parameters describing how to find the neighbors of each atom and how to calculate the interactions
nstlist       = 1            ; Frequency to update the neighbor list and long range forces
ns_type       = grid        ; Method to determine neighbor list (simple, grid)
rlist         = 1.0        ; Cut-off for making neighbor list (short range forces)
coulombtype   = PME        ; Treatment of long range electrostatic interactions
rcoulomb      = 1.0        ; long range electrostatic cut-off
rvdw          = 1.0        ; long range Van der Waals cut-off
pbc           = xyz         ; Periodic Boundary Conditions (yes/no)
"""
    fh.write(str(data))
    fh.close()

        
def file_copy(source, dest):
    in_file = open(source, 'r')
    out_file = open(dest, 'w')
    temp = in_file.read()
    out_file.write(temp)
    in_file.close()
    out_file.close()    

def AddIons():
    print ">STEP5 : Initiating Procedure to Add Ions & Neutralise the Complex"
    #grompp -f em.mdp -c solv.gro -p topol.top -o ions.tpr
    #genion -s ions.tpr -o solv_ions.gro -p topol.top -pname NA -nname CL -nn X -np X
    grompp = g_prefix+"grompp"
    StepNo = "5"
    StepName = "Check Ions "
    command = grompp + " -f "+ wdir+"em.mdp -c "+ wdir+"solv.gro -p "+ wdir+"topol.top -o "+wdir+"ions.tpr -po "+wdir+"mdout.mdp > "+wdir+"step5.log 2>&1"
    RunProcess(StepNo, StepName, command)
    
    #calculating the charge of the system
    word = 'total' #Your word
    
    with open(wdir+'step5.log') as f:
        for line in f:
            if word in line:
                s_line = line.strip().split()
                two_words = (s_line[s_line.index(word) + 1],s_line[s_line.index(word) + 2])
                charge = two_words[1]
                #print "Charge is " + charge
                break
    
    #print type(charge)
    print "Charge of the system is "+ charge
    charge= float(charge)          
    charge =round(charge)
    #print charge

    if charge > 0:
        print "System has positive charge ."
        print "Adding "+ str(charge) +" CL ions to Neutralize the system"
        genion=g_prefix+"genion"
        #genion -s ions.tpr -o solv_ions.gro -p topol.top -pname NA -nname CL -nn X -np X
        StepNo = "6"
        StepName = "Adding Negative Ions "
        command = genion + " -s "+ wdir+"ions.tpr -o "+ wdir+"solv_ions.gro -p "+ wdir+"topol.top -nname CL -nn "+ str(charge) +" -g "+ wdir+"step6.log 2>&1 << EOF\nSOL\nEOF"
        RunProcess(StepNo, StepName, command)
               
    elif charge < 0:
        print "charge is negative"
        print "Adding "+ str(-charge) +" CL ions to Neutralize the system"
        genion=g_prefix+"genion"
        #genion -s ions.tpr -o solv_ions.gro -p topol.top -pname NA -nname CL -nn X -np X
        StepNo = "6"
        StepName = "Adding Positive Ions "
        command = genion + " -s "+ wdir+"ions.tpr -o "+ wdir+"solv_ions.gro -p "+ wdir+"topol.top -pname NA -np "+ str(-charge)+" -g "+ wdir+"step6.log 2>&1 << EOF\nSOL\nEOF"
        RunProcess(StepNo, StepName, command)
    
    elif charge == 0:
        print "System has Neutral charge , No adjustments Required :)"
        file_copy('work/ions.tpr', "work/solv_ions.tpr")
    
    print "DOUBLE CHEERS: SUCCESFULY PREPARED SYSTEM FOR SIMULATION"
    

def CreateEmMdp():
    fh=open(wdir+"em_real.mdp","w")
    EmMdp="""
; LINES STARTING WITH ';' ARE COMMENTS
title        = Minimization    ; Title of run

; Parameters describing what to do, when to stop and what to save
integrator     = steep        ; Algorithm (steep = steepest descent minimization)
emtol          = 100.0      ; Stop minimization when the maximum force < 1.0 kJ/mol
emstep         = 0.01      ; Energy step size
nsteps         = 50000          ; Maximum number of (minimization) steps to perform
energygrps     = Protein UNK    ; Which energy group(s) to write to disk

; Parameters describing how to find the neighbors of each atom and how to calculate the interactions
nstlist        = 1            ; Frequency to update the neighbor list and long range forces
ns_type        = grid        ; Method to determine neighbor list (simple, grid)
rlist          = 1.0        ; Cut-off for making neighbor list (short range forces)
coulombtype    = PME        ; Treatment of long range electrostatic interactions
rcoulomb       = 1.0        ; long range electrostatic cut-off
rvdw           = 1.0        ; long range Van der Waals cut-off
pbc            = xyz         ; Periodic Boundary Conditions (yes/no)
"""
    fh.write(EmMdp)
    print "CHEERS: em_real.mdp SUCCESSFULLY GENERATED :)"
    
def Minimise():
    print ">STEP7 : Initiating Procedure to Add Ions & Neutralise the Complex"
    #grompp -f em_real.mdp -c solv_ions.gro -p topol.top -o em.tpr
    #mdrun -v -deffnm em
    grompp = g_prefix+"grompp"
    mdrun = g_prefix+"mdrun"
    StepNo = "7"
    StepName = "Prepare files for Minimisation"
    #max warn 3 only for now
    command = grompp + " -f "+ wdir+"em_real.mdp -c "+ wdir+"solv_ions.gro -p "+ wdir+"topol.top -o "+wdir+"em.tpr -po "+wdir+"mdout.mdp -maxwarn 3 > "+wdir+"step7.log 2>&1"
    RunProcess(StepNo, StepName, command)    
            
    StepNo = "8"
    StepName = " Minimisation"
    #$command="g_mdrun -v -nt ".$nproc." -s ".$path.$tpr." -c ".$path.$out." -o ".$path.$trr." -x ".$path.$xtc ."-g ".$path.$logfile." > ".$path.$clog." 2>&1";
    command = mdrun + " -v  -s "+ wdir+"em.tpr -c "+ wdir+"em.gro -o "+ wdir+"em.trr -e "+wdir+"em.edr -x "+wdir+"em.xtc -g "+wdir+"em.log > "+wdir+"step8.log 2>&1"
    RunProcess(StepNo, StepName, command)  

def Nvt():
    print ">STEP9 : Initiating the Procedure to Equiliberate the System"
    print "Beginging Equiliberation with NVT Ensemble"
    grompp= g_prefix+"grompp"
    mdrun=g_prefix+"mdrun"
    StepNo = "9"
    StepName ="Preparing files for NVT Equiliberation"
    #grompp -f nvt.mdp -c em.gro -p topol.top -o nvt.tpr
    command = grompp + "-f "+wdir+"nvt.mdp -c "+ wdir+"em.gro -p "+ wdir+"topol.top -o "+wdir+"nvt.tpr -po "+wdir+"mdout.mdp -maxwarn 3 > "+wdir+"step9.log 2>&1"
    RunProcess(StepNo,StepName, command)
    
    StepNo="10"
    StepName="NVT Equiliberation"
    command = mdrun + " -v  -s "+ wdir+"nvt.tpr -c "+ wdir+"nvt.gro -o "+ wdir+"nvt.trr -e "+wdir+"nvt.edr -x "+wdir+"nvt.xtc -g "+wdir+"nvt.log > "+wdir+"step10.log 2>&1"
    RunProcess(StepNo,StepName, command)
   
def Npt():
    print ">STEP11 : Initiating the Procedure to Equiliberate the System"
    print "Beginging Equiliberation with NPT Ensemble"
    grompp= g_prefix+"grompp"
    mdrun=g_prefix+"mdrun"
    StepNo = "11"
    StepName ="Preparing files for NPT Equiliberation"
    #grompp -f nvt.mdp -c em.gro -p topol.top -o nvt.tpr
    command = grompp + "-f "+wdir+"npt.mdp -c "+ wdir+"nvt.gro -p "+ wdir+"topol.top -o "+wdir+"npt.tpr -po "+wdir+"mdout.mdp -maxwarn 3 > "+wdir+"step11.log 2>&1"
    RunProcess(StepNo,StepName, command)
    
    StepNo="12"
    StepName="NPT Equiliberation"
    command = mdrun + " -v  -s "+ wdir+"npt.tpr -c "+ wdir+"npt.gro -o "+ wdir+"npt.trr -e "+wdir+"npt.edr -x "+wdir+"npt.xtc -g "+wdir+"npt.log > "+wdir+"step12.log 2>&1"
    RunProcess(StepNo,StepName, command)

def Md():
    print "CHEERS :) WE ARE CLOSE TO SUCCESS :):)"
    print ">STEP13 : Initiating the Production Run"
    grompp= g_prefix+"grompp"
    mdrun=g_prefix+"mdrun"
    StepNo = "13"
    StepName ="Preparing files for NPT Equiliberation"
    #grompp -f nvt.mdp -c em.gro -p topol.top -o nvt.tpr
    command = grompp + "-f "+wdir+"md.mdp -c "+ wdir+"npt.gro -p "+ wdir+"topol.top -o "+wdir+"md.tpr -po "+wdir+"mdout.mdp -maxwarn 3 > "+wdir+"step13.log 2>&1"
    RunProcess(StepNo,StepName, command)
    
    StepNo="14"
    StepName="NPT Equiliberation"
    command = mdrun + " -v  -s "+ wdir+"md.tpr -c "+ wdir+"md.gro -o "+ wdir+"md.trr -e "+wdir+"md.edr -x "+wdir+"md.xtc -g "+wdir+"md.log > "+wdir+"step14.log 2>&1"
    RunProcess(StepNo,StepName, command)

    
if __name__ == '__main__':
    LicenseInfo()
    #options()
    GatherFiles()
    pdb2gmx_proc()
    PrepareSystem()
    SolvateComplex()
    WriteEmMdp()
    AddIons()
    CreateEmMdp()
    Minimise()
    #Nvt()
    #Npt()
    #Md()
    print """
    *****************************************************
                   COMPLETED SUCCESSFULLY 
    *****************************************************
    THANKS FOR USING BNGROMACS version"""+ version + """
            DONT FORGET TO CITE bngromacs.py :)
                raviraja.merugu@gmail.com
            RSquareLabs (c) 2012, rsquarelabs.org
Find more info at http://www.rsquarelabs.org/works/bngromacs-py/index
    ******************************************************
"""
