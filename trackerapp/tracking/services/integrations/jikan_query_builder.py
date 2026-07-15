from ...forms import SearchForm
from typing import Any

def build_search_params(search_form : SearchForm) -> tuple[dict[str, Any], list]:
    params = {key : value for key,value in search_form.cleaned_data.items() if not key in ["type", "themes", "demographics"]}
    params['sfw'] = str(params['sfw']).lower()
    params['order_by'] = 'popularity'
    all_classifications = []
    for param_field in ['themes', 'demographics', 'genres']:
        selected_classifications = search_form.cleaned_data[param_field]
        if selected_classifications:
            all_classifications += [classification for classification in selected_classifications]
    return params, all_classifications

def build_search_params_anime(search_form : SearchForm) -> dict[str, Any]:
    params, all_classifications = build_search_params(search_form)
    params["genres"] = ",".join([str(tag.mal_id_anime) for tag in all_classifications])
    return params

def build_search_params_manga(search_form : SearchForm) -> dict[str, Any]:
    params, all_classifications = build_search_params(search_form)
    params["genres"] = ",".join([str(tag.mal_id_manga) for tag in all_classifications])
    return params