#!/usr/bin/env python3

import argparse
import os
import subprocess

def my_helper_function(input_file, output_file, option_value, flag_value):
    # Print helper functions 
    print(f"Input file - a .txt file with sample name and file-path {input_file}")
    print(f"Output file: {output_file}")
    print(f"Option value: {option_value}")
    print(f"Flag value: {flag_value}")

def main():
    parser = argparse.ArgumentParser(description = "A simple script to create a PopPUNK database and fit a range of k-values")
    parser.add_argument('--output', "-o", dest="output", help="Name of output directory")
    parser.add_argument('--sample-list', '-r', dest = "sample_list", required = True, help = "File containing the sample names and path to files")
    parser.add_argument('--threads', '-t', dest = "threads", type = int, default = 1, help = "Number of Threads for PopPUNK")
    parser.add_argument('--start-K', dest = "start_K", type=int, default = 1, help = "Start value for model fit")
    parser.add_argument('--end-K', dest =  "end_K", type = int, help = "End value for model fitting")
    parser.add_argument('--model', '-m', dest = 'model', help = "type of model")
    args = parser.parse_args()

    # Flag error if a model isn't specified
    if not args.model: 
        print('Error: Model Specified is Missing. Please input model using --model')
        parser.print_help()
        exit(1)

    print('User-defined parameters:')
    print(f'Output database name: {args.output}')
    print(f'Path to sample information file: {args.sample_list}')
    print(f'Number of threads: {args.threads}')
    print(f'Starting value of K: {args.start_K}')
    print(f'Ending value of K: {args.end_K}')
    print(f'Model to fit to the database: {args.model}')

    # Ask confirmation 
    confirmation = input("Do you want to proceed with this command? (y/n)")
    if confirmation.lower() != 'y': 
        print("Command cancelled.")
    else:
        # Check if the output database already exists 
        if os.path.isfile(f'{args.output}.h5'):
            print(f'Databse found at: {os.path.abspath(args.output)}')
            fit_model = True
        else: 
            # Run Poppunk Create    
            create_command = f'poppunk --create-db --output {args.output} --r-files {args.sample_list} --threads {args.threads}'
            subprocess.run(create_command, shell=True, check=True)

        # Create empty list to store output of each iteration 
        output_list = []

        # Loop over range of K for Model Fitting 
        # Writes stout to output where database is located
        for k_value in range(args.start_K, args.end_K+1):
            output_name = f'bgmm_K_{k_value}'
            output_file = os.path.join(args.output, output_name, f'{output_name}.txt')
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            fit_command = f'poppunk --fit-model {args.model} --ref-db {args.output} --K {k_value} --output "{output_name}"'
            with open(output_file, 'w') as f:
                process = subprocess.Popen(fit_command, shell=True, stdout=f, stderr=subprocess.STDOUT)
                error = process.communicate()[1]
            if error: 
                print(f"Error running command for k={k_value}")
            else: 
                print(f"Model fit complete for K={k_value}")
            
if __name__ == "__main__":
    main()