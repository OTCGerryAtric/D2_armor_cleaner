import pandas as pd
import streamlit as st
import clipboard as cb
from clipboard import ClipboardException
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

#Set page config
st.set_page_config(page_title="Exotic Build Tool", page_icon=None, layout="wide", initial_sidebar_state="expanded", menu_items=None)

@st.cache_data
def dim_upload(file):
    cols_to_use = ['Name', 'Hash', 'Id', 'Tier', 'Type', 'Equippable', 'Masterwork Type', 'Masterwork Tier',
                   'Mobility (Base)', 'Resilience (Base)', 'Recovery (Base)', 'Discipline (Base)', 'Intellect (Base)',
                   'Strength (Base)', 'Total (Base)']
    col_names = {'Name': 'name', 'Hash': 'hash', 'Id': 'id', 'Tier': 'tier', 'Type': 'type', 'Equippable': 'character',
                 'Masterwork Type': 'element', 'Masterwork Tier': 'mw_tier', 'Mobility (Base)': 'base_mob',
                 'Resilience (Base)': 'base_res', 'Recovery (Base)': 'base_rec', 'Discipline (Base)': 'base_dis',
                 'Intellect (Base)': 'base_int', 'Strength (Base)': 'base_str', 'Total (Base)': 'base_total'}
    file = pd.read_csv(file, usecols=cols_to_use)
    file = file.rename(columns=col_names)
    file['type'] = file['type'].replace({'Hunter Cloak', 'Warlock Bond', 'Titan Mark'}, 'Class Item').replace('Chest Armor', 'Chest').replace('Leg Armor', 'Legs')
    file["base_mob_res"] = file['base_mob'] + file['base_res']
    file["base_mob_rec"] = file['base_mob'] + file['base_rec']
    file["base_res_rec"] = file['base_res'] + file['base_rec']
    file["base_group_1"] = file['base_mob'] + file['base_res'] + file['base_rec']
    file["base_group_2"] = file['base_dis'] + file['base_int'] + file['base_str']
    file["mw_mob"] = file['base_mob'] + 2
    file["mw_res"] = file['base_res'] + 2
    file["mw_rec"] = file['base_rec'] + 2
    file["mw_dis"] = file['base_dis'] + 2
    file["mw_int"] = file['base_int'] + 2
    file["mw_str"] = file['base_str'] + 2
    file["mw_total"] = file['base_total'] + 12
    file["mw_mob_res"] = file['mw_mob'] + file['mw_res']
    file["mw_mob_rec"] = file['mw_mob'] + file['mw_rec']
    file["mw_res_rec"] = file['mw_res'] + file['mw_rec']
    file["mw_group_1"] = file['mw_mob'] + file['mw_res'] + file['mw_rec']
    file["mw_group_2"] = file['mw_dis'] + file['mw_int'] + file['mw_str']
    return file

armor_pieces = None  # Remember this!!!!!
armor_df = None

with st.sidebar:
    uploaded_file = st.file_uploader('Upload CSV File', type='csv')
    if uploaded_file is not None:
        try:
            armor_pieces = dim_upload(uploaded_file)
            st.write("CSV file is loaded")
        except pd.errors.EmptyDataError:
            st.write('Please upload the CSV file')
            st.stop()
    else:
        st.write("Please upload the CSV file")
        st.stop()
    character_select = st.sidebar.selectbox('Character', ('All', 'Hunter', 'Titan', 'Warlock'))
    armor_tier = st.sidebar.selectbox('Tier', ('All', 'Exotic', 'Legendary'))
    armor_type = st.sidebar.selectbox('Type', ('All', 'Helmet', 'Gauntlets', 'Chest', 'Legs', 'Class Item'))
    armor_element = st.sidebar.selectbox('Element', ('All', 'Arc', 'Solar', 'Void', 'Stasis'))

with st.expander("Armor Breakdown"):
    st.write("This provides a count of all armor owned (only looks at Exotic and Legendary)")
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    if character_select == 'All':
        e_h_count = sum((armor_pieces.tier == 'Exotic') & (armor_pieces.type == 'Helmet'))
    else:
        e_h_count = sum((armor_pieces.character == character_select) & (armor_pieces.tier == 'Exotic') & (armor_pieces.type == 'Helmet'))

    if character_select == 'All':
        l_h_count = sum((armor_pieces.tier == 'Legendary') & (armor_pieces.type == 'Helmet'))
    else:
        l_h_count = sum((armor_pieces.character == character_select) & (armor_pieces.tier == 'Legendary') & (armor_pieces.type == 'Helmet'))

    col1.metric(label="Exotic Helmets", value=e_h_count)
    col1.metric(label="Legendary Helmets", value=l_h_count)
    col1.metric(label="Total Helmets", value=e_h_count + l_h_count)
    
    if character_select == 'All':
        e_g_count = sum((armor_pieces.tier == 'Exotic') & (armor_pieces.type == 'Gauntlets'))
    else:
        e_g_count = sum((armor_pieces.character == character_select) & (armor_pieces.tier == 'Exotic') & (armor_pieces.type == 'Gauntlets'))

    if character_select == 'All':
        l_g_count = sum((armor_pieces.tier == 'Legendary') & (armor_pieces.type == 'Gauntlets'))
    else:
        l_g_count = sum((armor_pieces.character == character_select) & (armor_pieces.tier == 'Legendary') & (armor_pieces.type == 'Gauntlets'))

    col2.metric(label="Exotic Gauntlets", value=e_g_count)
    col2.metric(label="Legendary Gauntlets", value=l_g_count)
    col2.metric(label="Total Gauntlets", value=e_g_count + l_g_count)
    
    if character_select == 'All':
        e_c_count = sum((armor_pieces.tier == 'Exotic') & (armor_pieces.type == 'Chest'))
    else:
        e_c_count = sum((armor_pieces.character == character_select) & (armor_pieces.tier == 'Exotic') & (armor_pieces.type == 'Chest'))

    if character_select == 'All':
        l_c_count = sum((armor_pieces.tier == 'Legendary') & (armor_pieces.type == 'Chest'))
    else:
        l_c_count = sum((armor_pieces.character == character_select) & (armor_pieces.tier == 'Legendary') & (armor_pieces.type == 'Chest'))

    col3.metric(label="Exotic Chest Armor", value=e_c_count)
    col3.metric(label="Legendary Chest Armor", value=l_c_count)
    col3.metric(label="Total Chest Armor", value=e_c_count + l_c_count)
    
    if character_select == 'All':
        e_l_count = sum((armor_pieces.tier == 'Exotic') & (armor_pieces.type == 'Legs'))
    else:
        e_l_count = sum((armor_pieces.character == character_select) & (armor_pieces.tier == 'Exotic') & (armor_pieces.type == 'Legs'))

    if character_select == 'All':
        l_l_count = sum((armor_pieces.tier == 'Legendary') & (armor_pieces.type == 'Legs'))
    else:
        l_l_count = sum((armor_pieces.character == character_select) & (armor_pieces.tier == 'Legendary') & (armor_pieces.type == 'Legs'))

    col4.metric(label="Exotic Leg Armor", value=e_l_count)
    col4.metric(label="Legendary Leg Armor", value=l_l_count)
    col4.metric(label="Total Leg Armor", value=e_l_count + l_l_count)
    
    if character_select == 'All':
        e_ci_count = sum((armor_pieces.tier == 'Exotic') & (armor_pieces.type == 'Class Item'))
    else:
        e_ci_count = sum((armor_pieces.character == character_select) & (armor_pieces.tier == 'Exotic') & (armor_pieces.type == 'Class Item'))

    if character_select == 'All':
        l_ci_count = sum((armor_pieces.tier == 'Legendary') & (armor_pieces.type == 'Class Item'))
    else:
        l_ci_count = sum((armor_pieces.character == character_select) & (armor_pieces.tier == 'Legendary') & (armor_pieces.type == 'Class Item'))

    col5.metric(label="Exotic Class Items", value=e_ci_count)
    col5.metric(label="Legendary Class Items", value=l_ci_count)
    col5.metric(label="Total Class Items", value=e_ci_count + l_ci_count)

    col6.metric(label="Total Exotic Armor", value=e_h_count + e_g_count + e_c_count + e_l_count + e_ci_count)
    col6.metric(label="Total Legendary Armor", value=l_h_count + l_g_count + l_c_count + l_l_count + l_ci_count)
    col6.metric(label="Total Armor", value=e_h_count + e_g_count + e_c_count + e_l_count + e_ci_count + l_h_count + l_g_count + l_c_count + l_l_count + l_ci_count)

with st.expander("All Armor"):
    st.write("Detailed Armor Stats")
    armor_df = armor_pieces
    if character_select == 'All':
        pass
    else:
        armor_df = armor_df.loc[armor_df['character'] == character_select]
    if armor_tier == 'All':
        pass
    else:
        armor_df = armor_df.loc[armor_df['tier'] == armor_tier]
    if armor_type == 'All':
        pass
    else:
        armor_df = armor_df.loc[armor_df['type'] == armor_type]
    if armor_element == 'All':
        pass
    else:
        armor_df = armor_df.loc[armor_df['element'] == armor_element]

    armor_df = armor_df.loc[:, ['name', 'id', 'character', 'tier', 'type', 'mw_tier', 'base_mob', 'base_res', 'base_rec', 'base_dis', 'base_int', 'base_str', 'base_total']]
    armor_df = armor_df.rename(columns={'base_mob': 'Mobility', 'base_res': 'Resilience', 'base_res': 'Resilience', 'base_rec': 'Recovery', 'base_dis': 'Discipline', 'base_int': 'Intellect', 'base_str': 'Strength', 'base_total': 'Total'})

    armor_df = armor_df.sort_values('name')
    armor_df['Custom Total'] = ''

    col1, col2, col3, col4 = st.columns([1,1,1,2])
    col1.metric(label='Armor Count', value=len(armor_df))
    # create a button to copy the string
    select_3 = col4.multiselect('Custom Totals', ('Mobility', 'Resilience', 'Recovery', 'Discipline', 'Intellect', 'Strength'))

    if select_3:
        # filter the dataframe to include only the selected columns
        filtered_df = armor_df[select_3]

        # calculate the custom total by summing the values along the row axis
        custom_total = filtered_df.sum(axis=1)

        # add the custom total as a new column in the original dataframe
        armor_df['Custom Total'] = custom_total

    armor_df = armor_df.reset_index()

    gd = GridOptionsBuilder.from_dataframe(armor_df)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()
    #
    grid_table = AgGrid(armor_df, gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED, columns_auto_size_mode='FIT_CONTENTS', height=500)
    #
    sel_row = grid_table['selected_rows']
    selected_ids = [row['id'] for row in sel_row]
    id_loop = (len(sel_row))

    export_string = ' OR id:'.join(selected_ids)

    # display the selected ids and the export string
    dim_code = (f"id:{export_string}")

    if col2.button('Copy selection as DIM Filter'):
        try:
            cb.copy(dim_code)
            col2.write('String copied to clipboard!')
            st.write(dim_code)
        except ClipboardException:
            col2.write('Copy error, copy from below')
            st.write(dim_code)