#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l mem=5gb
#PBS -l walltime=100:00:00

cd $PBS_O_WORKDIR
export PYTHONPATH=$PYTHONPATH:/rhome/cjinfeng/software/tools/breakseq-1.3/lib;

python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svState/svState.py HEG4.Deletion.final.gff ./svState_Deletion_top 500
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svState/svState.py HEG4.insertion.SV.gff ./svState_Insertion_top 500

echo "Done"
