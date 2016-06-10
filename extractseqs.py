import re, os
qsub_command = "qsub"
qsub_command2 = "echo"

list1 = ["Acorus", "Burmannia", "Chamaedorea", "Costus", "Cypripedium", "Dasypogon",
        "Gymnosiphon", "Hanguana", "Japos", "Joinvillea", "Lacodonia", "Lilium",
        "Neoregelia", "Pandanus", "Saurattum", "Tacca", "Talbotia", "Triuris", "Typha"]
list2 = ["Aletris", "Anemarrhena", "Anomochloa", "Aphelia", "Aphyllanthes", "Aponogeton",
         "Apostasia", "Astelia", "Baxteria", "Behnia", "Calectasia", "Campynemante",
         "Centromono", "Centrostri", "Chlorophytum", "Croomia", "Cyperus", "Dendrobium",
         "Doryanthes", "Ecdeiocolea", "Elegia", "Flagellaria", "Hemiphylacus", "Hosta",
         "Ixiolirion",  "Juncus", "Kingia", "Lachocaulan", "Lanaria", "Leochilus",
        "Mayaca", "Mexipedium", "Molinaria",  "Paphiopedilum", "Parasitaxus", "Paris",
        "Phragmipedium", "Sagittaria", "Saurattum", "Stegolepis", "Streptochaeta",
        "Tradescantia", "Trithuria", "Triurfem", "Triuris", "Triurmal", "Uvularia", "Xyris"]
list3 = list1 + list2


for name in list3:
	script = """
	#PBS -l nodes=1:ppn=1
	#PBS -l walltime=01:00:00
	#PBS -l pmem=4gb
	#PBS -m bea


	cd /gpfs/home/prt119/biostar/projects/monatol/Single_copy_analysis/work_2016_Feb/{0}_orthos
	cat SC_orthos.ids  | xargs -I {} grep -w {}  {0}_genes_and_orthos_sorted | sort -k2 | uniq > Orthos_{0}.ids 
	mkdir Orthos_{0}
	perl -e' %seq; $id; open(IN, "{0}_gtcleaned.fasta.cds"); while(<IN>){chomp; if(/^>(\S+)/){$id=$1;} else{s/\s+//g; $seq{$id}{fna} .= $_;} } close IN; open(IN, "{0}_gtcleaned.fasta.pep"); while(<IN>){chomp; if(/^>(\S+)/){$id=$1;} else{s/\s+//g; $seq{$id}{faa} .= $_;} } close IN; %orthos; while(<>){chomp; @F=split(/\t/, $_); $orthos{$F[1]}{$F[0]} = $F[0]; } foreach $ortho_id (keys %orthos){open(F1, ">Orthos_{0}/$ortho_id.fna");  open(F2, ">Orthos_{0}/$ortho_id.faa"); foreach $seq_id(keys %{$orthos{$ortho_id}}){print F1 ">$seq_id\n$seq{$seq_id}{fna}\n"; print F2 ">$seq_id\n$seq{$seq_id}{faa}\n"; } close F1; close F2;}' < {0}_genes_and_orthos_sorted
	#mv Orthos_{0}.ids Orthos_{0}
	cp /gpfs/home/prt119/biostar/projects/monatol/Single_copy_analysis/SC_orthos.ids /gpfs/home/prt119/biostar/projects/monatol/Single_copy_analysis/work_2016_Feb/{0}_orthos/Orthos_{0}
	cd /gpfs/home/prt119/biostar/projects/monatol/Single_copy_analysis/work_2016_Feb/{0}_orthos/Orthos_{0}
	mkdir {0}_single_copies
	cat SC_orthos.ids | xargs -I {} cp {}.fna {0}_single_copies/
	cat SC_orthos.ids | xargs -I {} cp {}.faa {0}_single_copies/

	"""

	names = re.sub('\{0\}', name, script)
	names = re.sub('\{1\}', name[:4], names)
	print names
	filename = "extracting_" + name + ".pbs"
	fh = open(filename, "w")
	fh.write(names)
	fh.write("\n")
	fh.close()

	os.system('%s %s' % (qsub_command, filename))
	os.system('sleep 1')


