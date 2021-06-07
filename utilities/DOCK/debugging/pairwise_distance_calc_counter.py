#Script Name: pairwise_distance_calc_counter.py
#Script Purpose: Takes an input mol2 and calculates distances between all atoms pairwise,
## outputting any distances shorter than a user-specified value.
#Author Name: John Bickel
#Affiliation: Rizzo Lab, Stony Brook University
#Create date: 2019/07/08
#Last edit: 2020/05/03 John Bickel/SBU

import math
import sys
from math import sqrt
import os
import pathlib
import glob

def check_distances(name, atom_desc):
    distance_list=[]
    # goes through each atom pair top to bottom
    for i in range(len(atom_desc) - 1):
        atom1 = atom_desc[i]
        for y in range(i + 1, len(atom_desc)):
            atom2 = atom_desc[y]

            x1 = atom1[2]
            x2 = atom2[2]
            y1 = atom1[3]
            y2 = atom2[3]
            z1 = atom1[4]
            z2 = atom2[4]

            distance = sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) + (z1 - z2) * (z1 - z2))
            # this distance can be changed to adjust your search cutoff
            if distance < 0.89:
                distance_list.append(["%0s, | %0s %0s || %0s %0s %0s | %0s %0s %0s ||  %0s %0s | %0s" % (name, atom1[0], atom1[1], atom1[2], atom1[3], atom1[4], atom2[2], atom2[3], atom2[4],atom2[1], atom2[0], distance)])
    #you could return a list here instead of the state, then do the logic testing OUTSIDE of this, where it makes... more sense.
    return(distance_list)


def main():
    filenames = []
    filenames_sorted=[]
    bad_distances_list=[]
    molecule_check=True
    total_molecule_counter=0
    # gathers filenames from the current directory
    for currentFile in glob.glob("./*"):
        filenames.append(currentFile)
    # extracts all lines from one filefile
    for i in range(0,len(filenames)-1):
        for unsorted in filenames:
            #if (("restart%0s.mol2" % i in unsorted) or ("crossover%0s.mol2" % i in unsorted)):
            if ("restart%0s" % (i) in unsorted):
                print(unsorted)
                filenames_sorted.append(unsorted)
    for filename in filenames_sorted:
        molecule_counter=0
        print(filename)
        mol2_file = open(filename, 'r')
        lines = mol2_file.readlines()
        mol2_file.close()

        for line in lines:
            if "##########                                Name:" in line:
                linesplit=line.split(":")
            else:
                linesplit = line.split()
            
            linesplitLen = len(linesplit)
            # extracts molecule name from the DOCK header, and also resets atom_desc for a new molecule
            
            if ((len(linesplit) == 2) and ("Name" in line)):
                name = linesplit[1]
                atom_desc = []
            # extracts from the lines for each atom: [atom number, atom name, x, y, z]
            if (linesplitLen == 9) and linesplit[8] != "ROOT":
                atom_desc.append(
                    [linesplit[0], linesplit[1], float(linesplit[2]), float(linesplit[3]), float(linesplit[4])])
            # this is the last line of the molecule - passes to function to calculated pairwise distances
            if line.strip() == "@<TRIPOS>SUBSTRUCTURE":
                #calls check_distances, returns a list of bad distances
                bad_distances_list=check_distances(name, atom_desc)
                #if any bad distances are present, proceed with counter incrementing
                if len(bad_distances_list) > 0:
                    molecule_counter+=1
                    total_molecule_counter+=1
                    for i in range(len(bad_distances_list)):
                        print(bad_distances_list[i-1][0])
                        
                    ##prints the total for the file and the running total after each molecule containing a bad distance
                    ##uncomment if you want that - I thought the output was bloated.
                    #print('Total bad molecules for this file: '+ str(molecule_counter))
                    #print('Running total of bad molecules: ' + str(total_molecule_counter))
                    
        ##you can uncomment this line if you just want a final count at the end, not per file.
        ##reduces bloat.
        print('Total bad molecules for this file: '+ str(molecule_counter))
        
        ##this will print the total line after every single file. Uncomment if you want that - I thought it bloated
        ##the file output too much
        #print('Running total of bad molecules: ' + str(total_molecule_counter))
    print('Final total of bad molecules: '+ str(total_molecule_counter))
    return

main()
