#!/bin/bash - 
#===============================================================================
#
#          FILE: list_serial_ports.sh
# 
#         USAGE: ./list_serial_ports.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Dilawar Singh (), dilawars@ncbs.res.in
#  ORGANIZATION: NCBS Bangalore
#       CREATED: Thursday 08 December 2016 10:23:47  IST
#      REVISION:  ---
#===============================================================================

python -m serial.tools.list_ports -q | head -n 1
