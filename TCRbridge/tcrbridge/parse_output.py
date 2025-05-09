import json
import pandas as pd
from pathlib import Path
from copy import deepcopy

def read_json_file(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def get_scores(interface):
    PDE = interface['PDE']
    PMC = interface['PMC']
    ABi = interface['contact_iptm_score']
    contact_iptm_i = interface['ABi_score']
    
    return PDE ,PMC ,ABi ,contact_iptm_i
    
def get_interface_score_data(interaction):
    scores_dict = {
        'PDE' : [],
        'PMC' : [],
        'ABi' : [],
        'contact_iptm_i' : [],
        'bool_interface' : False
    } 
    interface_combination_list = ['AC','BC','CD', 'AD', 'BD']
    interface_score_data = {interface_combination: deepcopy(scores_dict) for interface_combination in interface_combination_list}

    for interface in interaction['interfaces']:
        interface_chain = interface['links'][0]['first']['asym_id'] + interface['links'][0]['second']['asym_id']
        
        if interface_chain in interface_combination_list:
            interface_score_data[interface_chain]['bool_interface'] = True
            PDE_i ,PMC_i ,ABi ,contact_iptm_i = get_scores(interface)
            interface_score_data[interface_chain]['PDE'].append(PDE_i)
            interface_score_data[interface_chain]['PMC'].append(PMC_i)
            interface_score_data[interface_chain]['ABi'].append(ABi)
            interface_score_data[interface_chain]['contact_iptm_i'].append(contact_iptm_i)
            
    for interface_combination in interface_combination_list:
        for score in ['PDE', 'PMC', 'contact_iptm_i', 'ABi']:
            if not interface_score_data[interface_combination]['bool_interface']:    
                interface_score_data[interface_combination][score] = None
            else:
                max_index = interface_score_data[interface_combination]['ABi'].index(max(interface_score_data[interface_combination]['ABi']))

                interface_score_data[interface_combination][score] = interface_score_data[interface_combination][score][max_index] 
    
    return interface_score_data

class TCR_STRUCTURE_DATA():
    def __init__(self,
                data_dir, 
                tcr_id):
        self.data_dir = Path(data_dir)
        self.tcr_id = tcr_id
        self.dir_path = self.data_dir / self.tcr_id
    
    def get_alphabridge_data(self):
        dir_path = self.dir_path
        path = dir_path / 'AlphaBridge' / 'alphabridge_data.json'
        if not path.exists():
            raise ValueError(f"alphabridge_data.json file does not exist in {path}")
        json_dict = read_json_file(path)
        
        return json_dict
    
        
    def get_structure_df(self):
        alphabridge_data = self.get_alphabridge_data()
        data = []
        PDE = alphabridge_data['structure'][0]['PDE']
        PMC= alphabridge_data['structure'][0]['PMC']
        IPTM = alphabridge_data['structure'][0]['iptm']
        contact_iptm = alphabridge_data['structure'][0]['contact_iptm']
        AB = alphabridge_data['structure'][0]['AB_score']
        
        tcr_id = self.tcr_id
        for interaction in alphabridge_data['interactions']:
            
            interface_score_data = get_interface_score_data(interaction)
            row = [PDE,
                   PMC,
                   IPTM,
                   contact_iptm,
                   AB,
                   tcr_id,
                   interaction['cut-off']]
            
            for interface_chain in interface_score_data:
                for score in interface_score_data[interface_chain]:
                            
                    row.append(interface_score_data[interface_chain][score])

            data.append(row)
        
        columns = ['PDE', 
                   'PMC', 
                   'IPTM', 
                   'contact_iptm', 
                   'AB', 
                   'tcr_id',
                   'cut-off']
        
        interface_combination_list = ['AC','BC','CD', 'AD', 'BD']
        scores_type = ['PDE', 'PMC', 'ABi', 'contact_iptm_i', 'bool_interface']
        
        for interface_chain in interface_combination_list:
                for score in scores_type:
                    
                    columns.append(f'{interface_chain}_{score}')
        structure_df = pd.DataFrame(data=data, columns=columns)
        
        return structure_df
