echo "python module in local"
export PYTHONPATH=$PYTHONPATH:/rhome/cjinfeng/software/tools/breakseq-1.3/lib;

echo "create genome sequence"
python SplitFasta.py --fasta /rhome/cjinfeng/BigData/00.RD/seqlib/MSU_r7.fa --outdir MSU7_unmask
python SplitFasta.py --fasta /rhome/cjinfeng/BigData/00.RD/GenomeAlign/Lastz/input/mask/MSU_r7.fa.RepeatMasker.masked --outdir MSU7_masked


