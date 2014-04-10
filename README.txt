##############################################################
BioNerd GROMACS AUTOMATION SCRIPT(bn-gromacs.py)
Verion 0.9a
raviraj@rsquarelabs.com
http://www.rsquarelabs.com
##############################################################

This script currently works for Protein-Ligand Minimisation only. Its pretty easy to extend it further till dynamics, I'm working on it and will be released soon, but I'am looking for some suggestions before I move further.

#Requirements :
1. Linux (works only in Linux)
2. gromacs 4.5.x (tested in 4.5.4)
3. python 2.7.x (written in python 2.7.5)

#Here is how it works, 
1. you should provide protein, ligand structure files(pdb/gro) along with ligand topology file (.itp) as input 
2. you can provide a folder name as an option, but by default it creates a working dir - "work", if no working dir is specified
3. once the input files for minimisation are created, it will wait for the user input(y/n) to continue, this is just to make sure you check whether this script generated what you are expecting. (so please check the solv-ions.gro using vmd before saying yes.)
4. All the step wise log files are generated with names step(x).log, where (x) is the number of step



#List of steps
step1 - Creating Protein Topologies- pdb2gmx+" -f "+ wdir+"protein.pdb -o "+wdir+"protein.gro -ignh -p "+ wdir+"topol.top -i "+ wdir+"posre.itp -ff gromos53a6 -water spc >> " + wdir+"step1.log 2>&1"   
step2 - adding ligand.gro+protein.gro to make system.gro and update topol.top
step3 - Defining the box - editconf + " -f "+ wdir+"system.gro -o "+ wdir+"newbox.gro -bt cubic -d 1 -c >> " + wdir+"step3.log 2>&1"
step4 - Solvating the box - genbox + " -cp "+ wdir+"newbox.gro -p "+ wdir+"topol.top -cs spc216.gro -o "+ wdir+"solv.gro >> " +wdir+"step4.log 2>&1"
step5 - Checking the charge of complex - grompp + " -f "+ wdir+"em.mdp -c "+ wdir+"solv.gro -p "+ wdir+"topol.top -o "+wdir+"ions.tpr -po "+wdir+"mdout.mdp > "+wdir+"step5.log 2>&1"
step6 - Neutralising the complex(if +ve) - genion + " -s "+ wdir+"ions.tpr -o "+ wdir+"solv_ions.gro -p "+ wdir+"topol.top -nname CL -nn "+ str(charge) +" -g "+ wdir+"step6.log 2>&1 << EOF\nSOL\nEOF
step6 - Neutralising the complex(if -ve) - genion + " -s "+ wdir+"ions.tpr -o "+ wdir+"solv_ions.gro -p "+ wdir+"topol.top -pname NA -np "+ str(-charge)+" -g "+ wdir+"step6.log 2>&1 << EOF\nSOL\nEOF"
step7 - Preparing for Minimisation - grompp + " -f "+ wdir+"em_real.mdp -c "+ wdir+"solv_ions.gro -p "+ wdir+"topol.top -o "+wdir+"em.tpr -po "+wdir+"mdout.mdp -maxwarn 3 > "+wdir+"step7.log 2>&1"
step8 - Minimisation - mdrun + " -v  -s "+ wdir+"em.tpr -c "+ wdir+"em.gro -o "+ wdir+"em.trr -e "+wdir+"em.edr -x "+wdir+"em.xtc -g "+wdir+"em.log > "+wdir+"step8.log 2>&1"



#List of log files :
step1.log - log file for protein topology generation
step2.log - Merging ligand protein structure data
step3.log - Defining the solvent box
step4.log - Adding sovlent molecules to the box 
step5.log - Checking the number of ions need to neutralise 
step6.log - Adding ions to neutralise the complex
step7.log - Preparing the files for Minimisation
step8.log - Minimisation log


Thanks & Cheers :)
Ravi RT Merugu


#Improvements Expected in Next Release
1.Auto detect the native Ligands (HEM, PEP, etc) and treat them accordingly 
2.work directory replacement.(work from any directory other than work folder)
3.Resuming the work [currently we backup the exsting project and begin from start, if we have to run again]


