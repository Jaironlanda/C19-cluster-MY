# Load dataset
import pandas as pd
from datetime import datetime


cluster_dataset = pd.read_csv("https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/clusters.csv")
cluster_dataset = pd.DataFrame(cluster_dataset)
new_cluster_dataset = cluster_dataset.reset_index(inplace=True)
new_cluster_dataset = cluster_dataset.rename(columns = {'index': 'cluster_id'})


"""
    Get list of cluster based on id, category, and state

    Example category: 
    [workplace, import, community, highRisk, religious, detentionCenter]

    parameter: c_id = int, cat_name = string, state_name = string
    return type: Dictionary / Lists
"""
def get_cluster_by(c_id=None, cat_name=None, state_name=None):
    if cat_name is not None:
        try:
            
            return new_cluster_dataset.loc[cluster_dataset['category'].isin([cat_name])].to_dict('records')
        except IndexError as e:
            return e
        
    elif c_id is not None:
        try:
            return new_cluster_dataset.iloc[c_id].to_dict()  # return single data
        except IndexError as e:
            return e
    
    elif state_name is not None:
        try:
            return new_cluster_dataset.loc[cluster_dataset['state'].str.contains(state_name)].to_dict('records')
        except IndexError as e:
            return e
    
    else:
        
        return {'error':'No data is selected'}


"""
    Count cluster by category (workplace, community, education, highRisk, religous, detentionCenter, import)
    Count total active and total overall cluster

"""
def cluster_count():
    cat_count_total = cluster_dataset['category'].value_counts().to_dict()
    total_active = cluster_dataset[cluster_dataset['status'] == 'active'].index.size
    total_cluster = cluster_dataset.index.size
    
    return {
        'total_active': total_active, 
        'total_cluster': total_cluster,
        'total_cluster_by_cat': cat_count_total,
        'total_cat_count': len(cat_count_total) 
    }

"""
    Chartjs config and data for cluster base on category
"""
def chart():
    
    chart_title= "Cluster Category"
    chart_config = 'doughnut' # Chart.js config
    cat_labels = cluster_dataset['category'].value_counts().index.tolist()
    cat_data = cluster_dataset['category'].value_counts().tolist()

    return {
        'chart_title': chart_title,
        'chart_config': chart_config,
        'cat_labels': cat_labels,
        'cat_data': cat_data
    }


"""
    Get update date dataset from github
    Ref: https://github.com/MoH-Malaysia/covid19-public/tree/main/epidemic#cluster-analysis
    
     Get latest cluster record base on announced_date from dataset
"""
def update_date():
    
    return cluster_dataset.iloc[-1:]['date_announced'].item()


"""
    Get latest cluster record base on announced_date from dataset
    select important columns only, to reduce load time.
"""

def new_cluster():
    
    # last update date
    lastupdate = update_date()
    
    new_cluster_list = pd.DataFrame(
            new_cluster_dataset, columns=[
                'cluster', 
                'state', 
                'district',
                'date_announced',
                'category', 
                'status', 
                'cases_new', 
                'cases_total',
                'cluster_id'
            ])
    
    try:
        #get cluster from high case to low case
        cluster_list_data = new_cluster_list.query(f"date_announced == '{lastupdate}' and status == 'active'").sort_values('cases_total', ascending=False)
        
        return {
            'total_new_cluster': len(cluster_list_data), 
            'cluster_list_data': cluster_list_data.to_dict('records'), 
        }
    
    except IndexError as e:
        return e



"""
    Search scope cluster name, state, and district
    parameter string
"""
def search_cluster_data(search):
    
    if search is not None:
        try:
            compile_data = pd.DataFrame(compile_search())
            result = compile_data.loc[compile_data['cluster'].str.contains(search, case=False)].to_dict('records')
            
            return {
                'result': result,
                'len_result': len(result)
            }
           
        except IndexError as e:
            return e



"""
    count cluster by state name
"""
def count_state_cluster(state_name):
    
    return new_cluster_dataset.loc[cluster_dataset['state'].str.contains(state_name)].index.size
    
"""
    ajax call

    list of cluster
"""
def cluster_list():

    try:
        
        cluster_list = pd.DataFrame(new_cluster_dataset, 
            columns=[
                'date_announced', 
                'cluster', 
                'state', 
                'district', 
                'category', 
                'status',
                'cluster_id'
            ])
        
        return cluster_list.to_dict('records')
    except IndexError as e:
        print(e)
    
    return e

"""
    Combine cluster name, state, and district data in one column `cluster`
    return dictionary
"""
def compile_search():
    search_data = []
    try:
        
        cluster_list = pd.DataFrame(new_cluster_dataset, 
            columns=[
                'cluster', 
                'state', 
                'district', 
                'cluster_id'
            ])
        
        compile_data = cluster_list.to_dict('index')
        for key, _ in compile_data.items():
            cluster_id = str(compile_data[key]['cluster_id'])
            search_data.append(
                {
                    'cluster': compile_data[key]['cluster'].rstrip() + " | " + compile_data[key]['state'].rstrip() + " | " + compile_data[key]['district'].rstrip(),
                    'cluster_id' : cluster_id
                }
            )

        return search_data
    except IndexError as e:
        return e