document.addEventListener('DOMContentLoaded', () => {
  renderItemOptions(0)
  document.getElementById('id_itemType').addEventListener('change', () => renderItemOptions(300))
})

const renderItemOptions = duration => {
  const itemType = document.getElementById('id_itemType').value
  switch(itemType){
    case 'link':
      $('#div_id_url').show(duration)
      $('#div_id_tempLocation').hide(duration)
      break
    case 'gallery':
      $('#div_id_url').hide(duration)
      $('#div_id_tempLocation').show(duration)
      break
  }
}