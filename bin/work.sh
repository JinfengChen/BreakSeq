head -n 20 ../../SV_postprocess/SV_merge/bin/Deletion/HEG4.Deletion.final.gff > test.gff
head -n 20 ../../SV_postprocess/SV_merge/bin/Deletion/HEG4.insertion.final.gff > test.insertion.gff
cat /rhome/cjinfeng/BigData/00.RD/Variations/SV_postprocess/SV_merge/bin/Deletion/HEG4.Deletion.final.gff /rhome/cjinfeng/BigData/00.RD/Variations/SV_postprocess/SV_merge/bin/Insertion/HEG4.insertion.final.gff > HEG4.SV.gff
cp /rhome/cjinfeng/BigData/00.RD/Variations/SV_postprocess/SV_merge/bin/Insertion/HEG4.insertion.final.gff HEG4.insertion.SV.gff
python Iseq.py --gff test.insertion.gff
python Iseq.py --gff HEG4.SV.gff
python Iseq.py --gff HEG4.insertion.SV.gff

echo "python module in local"
export PYTHONPATH=$PYTHONPATH:/rhome/cjinfeng/software/tools/breakseq-1.3/lib;

echo "create reference genome sequence"
python SplitFasta.py --fasta /rhome/cjinfeng/BigData/00.RD/seqlib/MSU_r7.fa --outdir MSU7_unmask
python SplitRM.py --RM /rhome/cjinfeng/BigData/00.RD/GenomeAlign/Lastz/input/mask/MSU_r7.fa.RepeatMasker.out

echo "create ancestor genome sequence"
python ChrName.py --input /rhome/cjinfeng/BigData/00.RD/Transposon_Oryza/OGE_genomes/O.glaberrima/O.glaberrima.v1.0.fa --output ./Oryza_genome/Ogla.fa
faToTwoBit Oryza_genome/Ogla.fa Oryza_genome/Ogla.2bit

python ChrName.py --input /rhome/cjinfeng/BigData/00.RD/Transposon_Oryza/OGE_genomes/O.punctata/O.punctata.v1.0.fasta --output ./Oryza_genome/Opun.fa
faToTwoBit Oryza_genome/Opun.fa Oryza_genome/Opun.2bit

echo "creat chain_net for genome alignment"
mkdir chain_net/MSU7_OGL.all_net_level1
cat /rhome/cjinfeng/BigData/00.RD/GenomeAlign/Lastz/output/MSU7vsOPU/prenet_net/Chr* > chain_net/MSU7_OGL.all_net_level1/net.level
python Net_ChrName.py --input chain_net/MSU7_OGL.all_net_level1/net.level
/opt/kentsrc/live/bin/netFilter -type=top chain_net/MSU7_OGL.all_net_level1/net.level.rename > chain_net/MSU7_OGL.all_net_level1/net.level.rename.top

mkdir chain_net/MSU7_OPU.all_net_level1
cat /rhome/cjinfeng/BigData/00.RD/GenomeAlign/Lastz/output/MSU7vsOPU/prenet_net/Chr* > chain_net/MSU7_OPU.all_net_level1/net.level
python Net_ChrName.py --input chain_net/MSU7_OPU.all_net_level1/net.level
/opt/kentsrc/live/bin/netFilter -type=top chain_net/MSU7_OPU.all_net_level1/net.level.rename > chain_net/MSU7_OPU.all_net_level1/net.level.rename.top

echo "test run svState.py"
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svState/svState.py test.gff ./win200 200 > log 2> log2
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svState/svState.py test.gff ./win1000 > log 2> log2
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svState/svState.py test.insertion.gff ./win50_insertion/ 50 > log 2> log2
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svState/svState.py HEG4.Deletion.final.gff ./svState_Deletion 500 > log 2> log2 &
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svState/svState.py HEG4.insertion.SV.gff ./svState_Insertion 500 > log 2> log2 &
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svState/svState.py HEG4.Deletion.final.gff ./svState_Deletion_top 500 > log 2> log2 &
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svState/svState.py HEG4.insertion.SV.gff ./svState_Insertion_top 500 > log 2> log2 &

echo "parse rectified gff"
python Rectify_gff.py --insertion svState_Insertion/HEG4.insertion.SV.gff --deletion svState_Deletion/HEG4.Deletion.final.gff
python Iseq.py --gff HEG4.rectify.Insertion.SV.gff

echo "test run svMech.py"
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svMech/svMech.py test.gff ./svMech/ 50
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svMech/svMech.py test.insertion.gff ./svMech/ 50 > log 2> log2 &
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svMech/svMech.py HEG4.SV.gff ./svMech/ 50 > log 2> log2 &
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svMech/svMech.py HEG4.insertion.SV.gff ./svMech 50 > log 2> log2 &
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svMech/svMech.py HEG4.Deletion.final.gff ./svMech_Deletion 50 > log 2> log2 &
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svMech/svMech.py HEG4.insertion.SV.gff ./svMech_Insertion 50 > log 2> log2 &
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svMech/svMech.py HEG4.rectify.Deletion.SV.gff ./svMech_Deletion_rectify 50 > log 2> log2 &
python /rhome/cjinfeng/software/tools/breakseq-1.3/bin/svMech/svMech.py HEG4.rectify.Insertion.SV.gff ./svMech_Insertion_rectify 50 > log 2> log2 &

echo "summary the mech"
python SumMech_Basic.py --input svMech_Deletion/HEG4.Deletion.SV.gff
python SumMech_Basic.py --input svMech_Insertion/HEG4.insertion.SV.gff --output Mech.Basic.Insertion
python SumMech_Basic.py --input svMech_Deletion_rectify/HEG4.rectify.Deletion.SV.gff --output HEG4.rectify.Deletion
python SumMech_Basic.py --input svMech_Insertion_rectify/HEG4.rectify.Insertion.SV.gff --output HEG4.rectify.Insertion




