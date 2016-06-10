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
	#PBS -l walltime=08:00:00
	#PBS -l pmem=4gb
	#PBS -m bea

	cd /gpfs/home/prt119/biostar/projects/monatol/Single_copy_analysis/work_2016_Feb/{0}_orthos/Orthos_{0}/{0}_single_copies/
	cp -r /gpfs/home/prt119/biostar/projects/monatol/Single_copy_analysis/banana/*.fna.ban .
	mkdir concatenated
	ls *.fna |  cut -d "." -f1 | xargs -I {} echo "cat {}.fna {}.fna.ban > concatenated/{}.con.fna" > concat.sh
	sh concat.sh
	cd concatenated/
	module load mafft/7.215
	perl -e 'foreach(<*.fna>) {chomp; if(/^(\d+)/) {$id = $1}; system "mafft --maxiterate 1000 --localpair $id.con.fna >$_.mafft";}'
	mkdir -p {0}/scaffold
	mv *.mafft {0}/scaffold
	perl /gpfs/home/prt119/biostar/software/scaffolding_script.NEW.pl {0} {0}_scaffold_summary.txt {0}_scaffolds


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


