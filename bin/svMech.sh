#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l mem=5gb
#PBS -l walltime=100:00:00

cd $PBS_O_WORKDIR
export PYTHONPATH=$PYTHONPATH:/rhome/cjinfeng/software/tools/breakseq-1.3/lib;

python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svMech/svMech.py HEG4.rectify.Deletion.SV.gff ./svMech_Deletion_rectify 50
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svMech/svMech.py HEG4.rectify.Insertion.SV.gff ./svMech_Insertion_rectify 50

python SumMech_Basic.py --input svMech_Deletion_rectify/HEG4.rectify.Deletion.SV.gff --output HEG4.rectify.Deletion
python SumMech_Basic.py --input svMech_Insertion_rectify/HEG4.rectify.Insertion.SV.gff --output HEG4.rectify.Insertion

echo "Done"
