import os
import sys
from pathlib import Path

_root_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(_root_dir))

import requests
import argparse
import json


from config import Config

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--api-key", type=str, default=None,
                        help="api key allocated by esologs.com")

    parser.add_argument('-s', "--target-spec", type=str, required=True,
                        help="target spec: tank, magicka, stamina, werewolf, healer, or all")
    parser.add_argument('-c', "--target-class", type=str, required=True,
                        help="target class: dragonknight, nightblade, necromancer, sorcerer, templar, warden, or all")
    parser.add_argument('-p', "--target-patch", type=str, default='all',
                        help="patch number to consider: 22 to 34, or 'all' will pull data from every patch")
    

    parser.add_argument('-o', "--output-directory", type=str, default="./output_files",
                        help="path to output the data files")

    parser.add_argument("-n", "--num-pages",  type=int, default=1,
                        help="number of pages to consider (each page <= 20 characters)")
    parser.add_argument("-d", "--min-dps",  type=float, default=40000.0,
                        help="ignore parses below this value")
 
    return parser


def build_query(api_key, update_num=34, spec_name='magicka', class_name='nightblade',  n=1):
    """
    Args 
    ----   
        update_num (str): the patch number to consider. Values can be 22 through 34
        spec_name (str): the build spec. Values can be tank, mag, stam, ww, healer.
        class_name (str): class name ending. Values can be any of the keys in $CLASSES.
        n (int): number of pages to consider (each page == 20 characters) 
        
    """
    # currently update 22 (Elsweyr) -> 34 (rising tide) as of June 2022 
    UPDATE={22 + i: str(i+1) for i in range(13)}
    CLASSES={'dragonknight':'1', 
             'nightblade': '2',
             'necromancer': '3',
             'sorcerer': '4',
             'templar': '5',
             'warden': '6'}

    SPECS={'tank': '1',
            'magicka': '2',
            'stamina': '3',
            'werewolf': '4',
            'healer': '5'}


    update_num = int(update_num)
    update_idx = UPDATE[update_num]
    class_idx = CLASSES[class_name]
    spec_idx = SPECS[spec_name]
    query = "https://www.esologs.com:443/v1/rankings/encounter/3009?metric=dps&partition=" + update_idx + "&class=" + class_idx + "&spec=" + spec_idx + "&page=" + str(n) + "&includeCombatantInfo=true&api_key=" + str(api_key)
    output_filename = '-'.join([str(update_num), spec_name, class_name]) + ".json"

    return query, output_filename


def execute_query(query, output_fp, dps_cutoff=80000.0):
    """
    cutoff (float): drop builds that do not achieve at least this ammount of DPS 
    """
    response = requests.get(query)
    data = response.json()
    characters = [k for k in data['rankings']]
    valid_characters = [c for c in characters if float(c['total']) > dps_cutoff]

    update_num, spec_name, class_name = output_fp.split('/')[-1][:-5].split('-')
    dps_cutoff = str(int(dps_cutoff / 1000.0)) + 'k'
    n_valid = str(len(valid_characters))

    print("[update " + str(update_num) + '] ' + spec_name + ' ' + class_name)
    print(" * found " + n_valid +  " parses over " + str(dps_cutoff) + " dps")
    print(" * query: " + str(query))

    output_data = json.dumps(valid_characters, indent=4)
    #output_data = valid_characters

    with open(output_fp, 'w') as f:
        print(output_data, file=f)


if __name__ == "__main__":
    args = get_args().parse_args()

    tgt_spec = args.target_spec
    tgt_class = args.target_class
    tgt_patch = args.target_patch 
    min_dps = args.min_dps
    n = args.num_pages

    outdir = args.output_directory
    api_key = args.api_key or Config.API_KEY 

    if not api_key:
        print("Please specify an esologs v1 api key. These are allocated by esologs.com")

    os.makedirs(outdir, exist_ok=True)

    query, fname = build_query(api_key, update_num=tgt_patch, spec_name=tgt_spec, class_name=tgt_class,  n=1)

    output_fp = os.path.join(outdir, fname) 
    
    execute_query(query, output_fp, dps_cutoff=min_dps)
