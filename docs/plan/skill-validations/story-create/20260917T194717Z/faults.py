"""Synthetic live-edit trigger; this produces evaluation evidence only."""
def observes_selected_epic(event,marker):
    item=event.get('item',{})
    return (event.get('type')=='item.completed' and item.get('type')=='command_execution'
            and item.get('exit_code')==0 and 'epic.md' in item.get('command','')
            and marker in item.get('aggregated_output',''))
