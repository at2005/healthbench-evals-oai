import json
import os
from pathlib import Path
from flask import Flask, render_template, redirect, url_for, request, jsonify, abort

app = Flask(__name__)

# Path to the metadata directory
METADATA_DIR = Path("dashboard/data")
RESULTS_DIR = Path("results")

@app.route('/')
def index():
    """Display the main dashboard page with a list of all evaluations."""
    if not METADATA_DIR.exists():
        return render_template('no_data.html')
    
    # Load the index of all evaluations
    index_path = METADATA_DIR / "index.json"
    if not index_path.exists():
        return render_template('no_data.html')
    
    try:
        with open(index_path, 'r') as f:
            data = json.load(f)
        evaluations = data.get('evaluations', [])
    except (json.JSONDecodeError, FileNotFoundError):
        evaluations = []
    
    return render_template('index.html', evaluations=evaluations)

@app.route('/eval/<eval_id>')
def evaluation_detail(eval_id):
    """Display detailed information about a specific evaluation."""
    # Load the metadata for this evaluation
    eval_path = METADATA_DIR / f"{eval_id}.json"
    if not eval_path.exists():
        return abort(404)
    
    try:
        with open(eval_path, 'r') as f:
            eval_data = json.load(f)
    except json.JSONDecodeError:
        return abort(500)
    
    # Load the full results data
    full_results_path = Path(eval_data.get('full_results_path', ''))
    if full_results_path.exists():
        try:
            with open(full_results_path, 'r') as f:
                full_results = json.load(f)
        except json.JSONDecodeError:
            full_results = {}
    else:
        full_results = {}
    
    # Extract category scores for visualization
    category_scores = eval_data.get('category_scores', {})
    
    # Get the list of examples/conversations
    convos = full_results.get('convos', [])
    metadata_items = full_results.get('metadata', {}).get('example_level_metadata', [])
    
    return render_template(
        'evaluation_detail.html', 
        eval=eval_data,
        category_scores=category_scores,
        convos=convos,
        metadata_items=metadata_items,
        full_results=full_results
    )

@app.route('/api/category_scores/<eval_id>')
def api_category_scores(eval_id):
    """API endpoint to get category scores for a specific evaluation."""
    eval_path = METADATA_DIR / f"{eval_id}.json"
    if not eval_path.exists():
        return jsonify({"error": "Evaluation not found"}), 404
    
    try:
        with open(eval_path, 'r') as f:
            eval_data = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON data"}), 500
    
    category_scores = eval_data.get('category_scores', {})
    return jsonify(category_scores)

@app.route('/compare', methods=['GET', 'POST'])
def compare_evaluations():
    """Compare multiple evaluations side by side."""
    if request.method == 'POST':
        selected_evals = request.form.getlist('selected_evals')
        if not selected_evals:
            return redirect(url_for('index'))
        
        eval_data = []
        for eval_id in selected_evals:
            eval_path = METADATA_DIR / f"{eval_id}.json"
            if eval_path.exists():
                try:
                    with open(eval_path, 'r') as f:
                        eval_item = json.load(f)
                        
                        # Load the full results data for example comparison
                        full_results_path = Path(eval_item.get('full_results_path', ''))
                        if full_results_path.exists():
                            try:
                                with open(full_results_path, 'r') as rf:
                                    full_results = json.load(rf)
                                    eval_item['convos'] = full_results.get('convos', [])
                                    eval_item['metadata_items'] = full_results.get('metadata', {}).get('example_level_metadata', [])
                            except json.JSONDecodeError:
                                eval_item['convos'] = []
                                eval_item['metadata_items'] = []
                        else:
                            eval_item['convos'] = []
                            eval_item['metadata_items'] = []
                            
                        eval_data.append(eval_item)
                except json.JSONDecodeError:
                    continue
        
        return render_template('compare.html', evaluations=eval_data)
    
    # GET request - show the selection form
    index_path = METADATA_DIR / "index.json"
    if not index_path.exists():
        return render_template('no_data.html')
    
    try:
        with open(index_path, 'r') as f:
            data = json.load(f)
        evaluations = data.get('evaluations', [])
    except (json.JSONDecodeError, FileNotFoundError):
        evaluations = []
    
    return render_template('select_compare.html', evaluations=evaluations)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 