#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
from numpy import *
import re
import os
import argparse
from Bio import SeqIO

def usage():
    test="name"
    message='''
python SumMech_Basic.py --input HEG4.insertion.SV.gff

    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid

'''
Chr1	SVpipe	Deletion	66133	66245	.	.	.	INDEL=Deletio "INDEL=Deletion"; Mech "NAHR"; Method=soaps "Method=soapsv"; Seq=GGCGGGCGGGAGAGGCGGGGCGGCGGCCGGCAGGAGAGGAGGCGCGCGGCCGGCGGGCGGGAGAGGAGGCGCGCGGCCGGCGGGCGGCGGGAGAGGGGGCGCGGCGGCGGGC "Seq=GGCGGGCGGGAGAGGCGGGGCGGCGGCCGGCAGGAGAGGAGGCGCGCGGCCGGCGGGCGGGAGAGGAGGCGCGCGGCCGGCGGGCGGCGGGAGAGGGGGCGCGGCGGCGGGCG"; Size=11 "Size=113"
'''

def drawLengthclass(Rfile):
    pdf = Rfile.replace('.table', '.pdf')
    R   = Rfile.replace('.table', '.R')
    Rcmd='''
pdf("''' + pdf  + '''")
par(mar=c(6,4,4,10))
par(xpd=TRUE)

barlegend <- function(x,y,height,length,name,color){
    rect(x,y-0.04*height,x+0.05*length,y,col=color,border=FALSE)
    text(x+0.15*length,y-0.02*height,labels=name)
}


x <- read.table("'''+ Rfile +'''", skip = 1, sep = '\\t')
data <- rbind(x[,3]/x[,2],x[,4]/x[,2],x[,5]/x[,2],x[,6]/x[,2],x[,7]/x[,2],x[,8]/x[,2])
xx <- barplot(data,ylab="Proportion",border=FALSE,space=1,ylim=c(0,1),col=c("blue","orange","#A0522D","green","gray","black"))
axis(1,c(0.9,max(xx)+0.6),line=0,labels=c("",""))
text(xx,rep(-0.08,6),offset=2,labels=x[,1],srt=55,xpd=TRUE)
legend(10,0.8,bty="n",lty=c(0,0),border="NA",cex=1.2,c("NHR","NAHR","VNTR","MTEI","STEI","UNSURE"),fill=c("blue","orange","#A0522D","green","gray","black"))

#barlegend(10,0.7,1,10,"CDS","red")

mtext("Indel Length (bp)",side=1, at=5.2,line=4)
dev.off()
'''
    ofile = open (R, 'w')
    print >> ofile, Rcmd
    ofile.close()
    os.system('cat %s | R --slave' % (R))



def drawPie(Rfile):
    pdf = Rfile.replace('.table', '.pdf')
    R   = Rfile.replace('.table', '.R')
    Rcmd='''
pdf("''' + pdf  + '''")
options(digits=2)
read.table("''' + Rfile  + '''",skip=1,sep='\\t') -> anno
pie(anno[,3],border = NA, init.angle = 40,labels=anno[,1],radius=0.8,col=c("#FA8072","orange","green","blue","gray","black")) -> x
#legend(0.6,1,cex=1,anno[,1],bty="n",fill=c("#FFA07A","orange","green","blue","gray","black"))
dev.off() 
'''
    ofile = open (R, 'w')
    print >> ofile, Rcmd
    ofile.close()
    os.system('cat %s | R --slave' % (R))

def sumMech(infile, outfile):
    data = defaultdict(int)
    lengthclass = defaultdict(lambda : defaultdict(int))
    total = 0
    s = re.compile(r'Mech \"(\w+)\".*\"Size=(\d+)\"')
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 or not line.startswith('#'): 
                unit = re.split(r'\t',line)
                m = s.search(unit[8])
                if m:
                    mech   = m.groups(0)[0].replace('_EXT','')
                    size   = m.groups(0)[1]
                    data[mech] = data[mech] + 1
                    total = total + 1
                    if int(size) <= 100:
                        lengthclass['50'][mech] = lengthclass['50'][mech] + 1
                    elif int(size) <= 500:
                        lengthclass['100'][mech] = lengthclass['100'][mech] + 1
                    elif int(size) <= 1000:
                        lengthclass['500'][mech] = lengthclass['500'][mech] + 1
                    elif int(size) <= 5000:
                        lengthclass['1000'][mech] = lengthclass['1000'][mech] + 1
                    else: 
                        lengthclass['5000'][mech] = lengthclass['5000'][mech] + 1
                
    mechs = ['NHR', 'NAHR', 'VNTR', 'MTEI', 'STEI', 'UNSURE']
    ofile = open(outfile + '.Pie.table', 'w') 
    print >> ofile, 'Mechanism Percent%	Number#'
    for mech in mechs:
        if data.has_key(mech):
            print >> ofile, '%s %d%%\t%s\t%s' % (mech, int(100.00*float(data[mech])/float(total)), data[mech], float(data[mech])/float(total))
    ofile.close()
    drawPie(outfile + '.Pie.table')

    lengths = {'50':'50-100', '100':'100-500', '500':'500-1000', '1000':'1000-5000', '5000':'>5000'}
    ofile = open (outfile + '.LengthClass.table', 'w')
    print >> ofile, 'Lenth	#Total	#NHR	#NAHR	#VNTR	#MTEI	#STEI	#UNSURE'
    for length in sorted(lengthclass.keys(), key=int):
        line = lengths[length]
        temp = []
        suml = 0
        for mech in mechs:
            num = lengthclass[length][mech] if lengthclass[length][mech] > 0 else 0
            suml = suml + num
            temp.append(str(num))
        line = line + '\t' + str(suml) + '\t' + '\t'.join(temp)
        print >> ofile, line
    ofile.close()
    drawLengthclass(outfile + '.LengthClass.table')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.input) > 0
    except:
        usage()
        sys.exit(2)
    
    if args.output is None:
        args.output = 'Mech.Basic'
     
    sumMech(args.input, args.output)

if __name__ == '__main__':
    main()

