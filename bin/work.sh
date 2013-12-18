head -n 20 ../../SV_postprocess/SV_merge/bin/Deletion/HEG4.Deletion.final.gff > test.gff
head -n 20 ../../SV_postprocess/SV_merge/bin/Deletion/HEG4.insertion.final.gff > test.insertion.gff
python Iseq.py --gff test.insertion.gff

echo "python module in local"
export PYTHONPATH=$PYTHONPATH:/rhome/cjinfeng/software/tools/breakseq-1.3/lib;

echo "create reference genome sequence"
python SplitFasta.py --fasta /rhome/cjinfeng/BigData/00.RD/seqlib/MSU_r7.fa --outdir MSU7_unmask
python SplitFasta.py --fasta /rhome/cjinfeng/BigData/00.RD/GenomeAlign/Lastz/input/mask/MSU_r7.fa.RepeatMasker.masked --outdir MSU7_masked

echo "create ancestor genome sequence"
python ChrName.py --input /rhome/cjinfeng/BigData/00.RD/Transposon_Oryza/OGE_genomes/O.glaberrima/O.glaberrima.v1.0.fa --output ./Oryza_genome/Ogla.fa
faToTwoBit Oryza_genome/Ogla.fa Oryza_genome/Ogla.2bit

python ChrName.py --input /rhome/cjinfeng/BigData/00.RD/Transposon_Oryza/OGE_genomes/O.punctata/O.punctata.v1.0.fasta --output ./Oryza_genome/Opun.fa
faToTwoBit Oryza_genome/Opun.fa Oryza_genome/Opun.2bit

echo "creat chain_net for genome alignment"
mkdir chain_net/MSU7_OGL.all_net_level1
cat /rhome/cjinfeng/BigData/00.RD/GenomeAlign/Lastz/output/MSU7vsOPU/prenet_net/Chr* > chain_net/MSU7_OGL.all_net_level1/net.level
python Net_ChrName.py --input chain_net/MSU7_OGL.all_net_level1/net.level

mkdir chain_net/MSU7_OPU.all_net_level1
cat /rhome/cjinfeng/BigData/00.RD/GenomeAlign/Lastz/output/MSU7vsOPU/prenet_net/Chr* > chain_net/MSU7_OPU.all_net_level1/net.level
python Net_ChrName.py --input chain_net/MSU7_OPU.all_net_level1/net.level

echo "test run svState.py"
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svState/svState.py test.gff ./win200 200 > log 2> log2
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svState/svState.py test.gff ./win1000 > log 2> log2
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svState/svState.py test.insertion.gff ./win50_insertion/ 50 > log 2> log2

