// copy(JSON.stringify(localStorage));

let data = {
  column_added_on_width_torrentsTableDiv: '72',
  column_category_visible_torrentsTableDiv: '0',
  selected_filter: 'downloading',
  column_port_width_torrentPeersTableDiv: '52',
  column_num_seeds_width_torrentsTableDiv: '46',
  column_relevance_width_torrentPeersTableDiv: '74',
  column_size_width_torrentsTableDiv: '67',
  reverse_sort_torrentsTableDiv: '0',
  column_num_leechs_width_torrentsTableDiv: '47',
  sorted_column_torrentsTableDiv: 'eta',
  columns_order_torrentsTableDiv:
    'priority,state_icon,name,size,total_size,progress,status,num_seeds,num_leechs,dlspeed,upspeed,eta,ratio,category,tags,time_active,added_on,completion_on,tracker,dl_limit,up_limit,downloaded,uploaded,downloaded_session,uploaded_session,amount_left,save_path,completed,max_ratio,seen_complete,last_activity',
  column_client_width_torrentPeersTableDiv: '156',
  column_completion_on_width_torrentsTableDiv: '101',
  column_upspeed_width_torrentsTableDiv: '75',
  column_ratio_visible_torrentsTableDiv: '0',
  column_completion_on_visible_torrentsTableDiv: '1',
  filters_width: '120',
  column_time_active_visible_torrentsTableDiv: '1',
  column_dl_speed_width_torrentPeersTableDiv: '88',
  column_up_speed_width_torrentPeersTableDiv: '73',
  column_tags_visible_torrentsTableDiv: '0',
  column_progress_width_torrentsTableDiv: '59',
  column_time_active_width_torrentsTableDiv: '77',
  speed_in_browser_title_bar: 'false',
  properties_height_rel: '0.4969843184559711',
  column_ip_width_torrentPeersTableDiv: '110',
  column_connection_width_torrentPeersTableDiv: '84',
  column_progress_width_torrentPeersTableDiv: '72',
  column_uploaded_width_torrentPeersTableDiv: '74',
  column_flags_width_torrentPeersTableDiv: '97',
  column_status_width_torrentsTableDiv: '77',
  column_name_width_torrentsTableDiv: '379',
  column_dlspeed_width_torrentsTableDiv: '83',
  column_downloaded_width_torrentPeersTableDiv: '86',
  column_country_width_torrentPeersTableDiv: '59',
  selected_tab: 'PropFilesLink',
  column_eta_width_torrentsTableDiv: '55',
};

// let data = JSON.parse(settings);
Object.keys(data).forEach(function(k) {
  localStorage.setItem(k, data[k]);
});
location.reload();
