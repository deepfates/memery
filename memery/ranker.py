__all__ = ['ranker', 'nns_to_files']

def ranker(query_vec, treemap):
    nn_indexes = treemap.get_nns_by_vector(query_vec[0], treemap.get_n_items())
    return(nn_indexes)

def nns_to_files(db, indexes):
#     return([[v['fpath'] for k,v in db.items() if v['index'] == ind][0] for ind in indexes])
    return([db[ind]['fpath'] for ind in indexes])