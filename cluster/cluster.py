from flask import (
        Blueprint, 
        render_template, 
        url_for, 
        jsonify, 
        request, 
        redirect
    )
from cluster.form import searchCluster
from flask_wtf.csrf import CSRFProtect
from cluster.data_pandas import (
        get_cluster_by, 
        cluster_count, 
        chart, 
        update_date, 
        new_cluster,
        search_cluster_data,
        cluster_list,
        count_state_cluster
    )
from cluster.models import state_list, category_list

bp = Blueprint('cluster', __name__)

@bp.context_processor
def context_processor():
    web_config = {
        'meta_description': 'Malaysia COVID-19 Cluster', 
        'theme_color': '#0E86D4',
        'web_author': 'Jairon Landa',
        'brand': 'Malaysia COVID-19 Cluster',
    }
    return dict(lastupdate=update_date(), form=searchCluster(), web_config=web_config)

# Cluster Dashboard page
@bp.route('/')
def index():
    
    page_name = 'Dashboard'
    return render_template('dashboard.html', 
        title=page_name, 
        page_name=page_name,
        total=cluster_count(), 
        chart=chart(),
        new_cluster=new_cluster(),
        state_list=state_list(),
        count_state_cluster=count_state_cluster
    )

#  Cluster Search Page
@bp.route('/search', methods=['POST', 'GET'])
def search_cluster():
    page_name="Search Result(s)"
    form = searchCluster()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            search_input = form.search_cluster.data
            search = search_cluster_data(search_input)
            return render_template('search.html', page_name=page_name, result=search['result'], len_result=search['len_result'], search_input=search_input)
    else:
        return redirect(url_for('.index'))

    
# Cluster Detail page
@bp.route('/cluster/<int:c_id>')
def cluster_detail(c_id):
    page_name = 'Cluster Detail'
    cluster_data = get_cluster_by(c_id=c_id)
    if cluster_data is not None:
        return render_template('cluster_data.html', 
            title=page_name, 
            page_name=page_name, 
            cluster_data=cluster_data
        )
    else:
        return "Page Not Found", 404

# Cluster Category page
@bp.route('/cluster/<string:cluster_category>/category')
def cluster_category(cluster_category):
    page_name= cluster_category.capitalize() +' Cluster(s)'
    cluster_list_cat = get_cluster_by(cat_name=cluster_category)
    
    if cluster_list_cat is not None:
        return render_template('cluster_cat.html', 
            title=page_name,
            page_name=page_name,
            cluster_list_cat=cluster_list_cat,
            len_cluster_cat= len(cluster_list_cat),
            cluster_category_name=cluster_category
        )
    else:
        return "Page Not Found", 404

# Cluster State page
@bp.route('/cluster/<string:cluster_state>/state')
def cluster_state(cluster_state):
    page_name =  "State: " + cluster_state.capitalize()
    cluster_list_state = get_cluster_by(state_name=cluster_state)
    if cluster_state is not None:
        return render_template('cluster_state.html',
            title=page_name,
            page_name=page_name,
            cluster_list_state=cluster_list_state,
            len_cluster_state=len(cluster_list_state)
        )
    else:
        return "Page Not Found", 404

# Cluster Index page 
@bp.route('/cluster/index')
def cluster_index():
    page_name="Cluster Index"

    return render_template('cluster_all.html', 
        title=page_name, 
        page_name=page_name, 
        lastupdate=update_date()
    )

# Cluster API for Ajax call from DataTables
@bp.route('/cluster/api')
def cluster_api():
    return jsonify(data=cluster_list())