#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --time=1:00:00
#SBATCH --mem=8GB
#SBATCH --job-name=green15
#SBATCH --mail-type=END
#SBATCH --mail-user=ayw255@nyu.edu
#SBATCH --output=slurm_%j.out

module load spark/2.2.0
module load python3/intel/3.6.3

cd /scratch/ayw255/
spark-submit --conf spark.pyspark.python=/share/apps/python3/3.6.3/intel/bin/python3 uniqueness_by_MapReduce.py green16_trip.csv



