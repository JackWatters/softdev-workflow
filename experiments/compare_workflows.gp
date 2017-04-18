#!/usr/bin/gnuplot

set terminal png size 300,200

#set yrange [0:120]

set datafile separator ","

set output './compare_workflows_mtf.png'

set ylabel 'average mean time to failure'
set xlabel 'fuzzings'

set nokey

# 'compare_workflows.csv' every  ::1::8 using 22:31 with points lt rgb "red", \

plot 'compare_workflows.csv' every  ::1::10 using 22:31 with points lt rgb "green", \
 'compare_workflows.csv' every  ::11::20 using 22:31 with points lt rgb "black",
# 'compare_workflows.csv' every  ::75::96 using 22:31 with points lt rgb "blue", \

