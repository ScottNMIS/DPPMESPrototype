import requests

def get_company_data(beauhurst_api_key, company_id):
    url = f"https://platform.beauhurst.com/_api/v1/companies?company_ids={company_id}&includes=name&includes=registered_name&includes=registration_date&includes=other_trading_names&includes=companies_house_id&includes=employee_count_range&includes=last_modified_date&includes=beauhurst_url&includes=website&includes=tracked_status&includes=started_tracking_at&includes=company_status&includes=is_sme&includes=sectors&includes=top_level_sector_groups&includes=description&includes=ultimate_parent_company&includes=industries&includes=top_level_industry_groups&includes=buzzwords&includes=latest_stage_of_evolution&includes=stage_of_evolution_transitions&includes=tracking_reasons&includes=target_markets&includes=founder_female_percentage&includes=sic_codes&includes=actively_hiring&includes=legal_form&includes=signals&includes=n_fundraisings&includes=total_amount_fundraisings&includes=n_grants&includes=latest_valuation&includes=country&includes=lep&includes=region&includes=postcode&includes=address&includes=emails&includes=telephone&includes=registered_address&includes=key_contacts&includes=directors&includes=twitter_handle&includes=instagram_handle&includes=pinterest_handle&includes=facebook_url&includes=googleplay_url&includes=itunes_url&includes=linkedin_url&includes=year_end_date&includes=turnover&includes=ebitda&includes=total_assets&includes=number_of_employees&includes=cash&includes=total_liabilities&includes=net_assets&includes=research_and_development&includes=export&includes=auditor&includes=audit_fees"
    headers = {
        "accept": "application/json",
        "Authorization": f"APIKey {beauhurst_api_key}"
    }

    response = requests.get(url, headers=headers)
    return response
