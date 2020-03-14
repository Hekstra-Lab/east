data_dir_glob=/home/kmdalton/xtal/kiw/20200313/? 
results_filename=/home/kmdalton/opt/east/log.txt 
cwd=`pwd`

procs=10 #number of processors to use for spot finding
sg=19 #space group number

dir=`dirname $0`
axes_script="`readlink -f $dir`"/axes.py

glob0=../?_0_1_000??.mccd
glob90=../?_90_2_000??.mccd



for i in $data_dir_glob;do
  cd $i
  mkdir dials
  cd dials
  dials.import $glob0 $glob90 
  dials.find_spots imported.expt spotfinder.threshold.dispersion.gain=4 spotfinder.mp.nproc=$procs
  dials.split_experiments imported.expt strong.refl

  dials.combine_experiments split_* \
    reference_from_experiment.beam=0 \
    reference_from_experiment.goniometer=0 \
    reference_from_experiment.detector=0 

  dials.index combined.* space_group=$sg
  dials.refine scan_varying=False indexed.*

  printf "



##########################################################
%s
##########################################################" $i >> $results_filename
  $axes_script >> $results_filename
  cd $cwd
done

