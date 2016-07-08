#!/usr/bin/gnuplot

set terminal png size 1200,800

EXPERIMENTAL_REPORT_DIR='results'

#set yrange [0:500]

set datafile separator ","

set output EXPERIMENTAL_REPORT_DIR.'/compare_workflows_mtf.png'

set ylabel 'average mean time to failure'
set xlabel 'p not finish'

plot \
 EXPERIMENTAL_REPORT_DIR.'/compare_workflows.csv' every  ::41::60 using 5:6 with lines lt rgb "red" title "Waterfall,p_miss_step=0.0,res=250", \
 EXPERIMENTAL_REPORT_DIR.'/compare_workflows.csv' every  ::61::80 using 5:6 with lines lt rgb "orange" title "Waterfall,p_miss_step=0.5,res=250", \
 EXPERIMENTAL_REPORT_DIR.'/compare_workflows.csv' every ::121::140 using 5:6 with lines lt rgb "blue" title "TDD,p_miss_step=0.0,res=250", \
 EXPERIMENTAL_REPORT_DIR.'/compare_workflows.csv' every ::141::160 using 5:6 with lines lt rgb "green" title "TDD,p_miss_step=0.5,res=250"

 # EXPERIMENTAL_REPORT_DIR.'/compare_workflows.csv' every   ::1::20 using 5:6 with lines lt rgb "red" title "Waterfall,p_miss_step=0.0,res=50", \
# EXPERIMENTAL_REPORT_DIR.'/compare_workflows.csv' every  ::21::40 using 5:6 with lines lt rgb "orange" title "Waterfall,p_miss_step=0.5,res=50", \
# EXPERIMENTAL_REPORT_DIR.'/compare_workflows.csv' every  ::81::100 using 5:6 with lines lt rgb "blue" title "TDD,p_miss_step=0.0,res=50", \
# EXPERIMENTAL_REPORT_DIR.'/compare_workflows.csv' every ::101::120 using 5:6 with lines lt rgb "green" title "TDD,p_miss_step=0.5,res=50"
