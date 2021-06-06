#!/bin/bash

first_pos=${1}
second_pos=${2}
sed -i "s/first/${first_pos}/g" ./*.in
sed -i "s/second/${second_pos}/g" ./*.in


cpptraj -i 001.cpptraj_stripparm.in
cpptraj -i 002.cpptraj_stripcrd.in
cpptraj -i 003.cpptraj_stripfit.in
cpptraj -i 004.cpptraj_rmsdlig.in
