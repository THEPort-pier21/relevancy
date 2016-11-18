import json

json_db_file_path = "json_db_all_new.json"

def add_doc_to_json_db(text, title, relevancy=-1, relevancy_feedback=-1, 
                       url="", cluster=-1, clustering_feedback=-1):
    """Adds the given record to the JSON DB."""
    
    with open(json_db_file_path) as f:
        db = json.load(f)
        
        new_record = {}
        new_record["text"] = text
        new_record["title"] = title
        new_record["relevancy"] = relevancy
        new_record["relevancy_feedback"] = relevancy_feedback
        new_record["url"] = url
        new_record["cluster"] = cluster
        new_record["clustering_feedback"] = clustering_feedback
        
        db.append(new_record)
        
    with open(json_db_file_path, 'w') as f:
        json.dump(db, f, indent=4)
