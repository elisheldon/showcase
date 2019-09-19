document.addEventListener('DOMContentLoaded', () => {
  renderItemOptions(0)
  document.getElementById('id_item_type').addEventListener('change', () => renderItemOptions(300))
  /*document.getElementById('id_url').addEventListener('change', () => {

  })*/
})

const renderItemOptions = duration => {
  const item_type = document.getElementById('id_item_type').value
  switch(item_type){
    case 'link':
      $('#div_id_temp_location').fadeOut(duration, function(){
        $('#div_id_url').fadeIn(duration)
      })
      break
    case 'gallery':
      $('#div_id_url').fadeOut(duration, function(){
        $('#div_id_temp_location').fadeIn(duration)
      })
      break
  }
}