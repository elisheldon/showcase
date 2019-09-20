let titleManuallyChanged = false
let descriptionManuallyChanged = false

document.addEventListener('DOMContentLoaded', () => {
  renderItemOptions(0)
  document.getElementById('id_item_type').addEventListener('change', () => renderItemOptions(300))
  $('#id_url').typeWatch( typewatch_options )
  document.getElementById('id_title').addEventListener('keyup', () => {
    titleManuallyChanged = true
    document.getElementById('card_title').innerHTML = document.getElementById('id_title').value
  })
  document.getElementById('id_description').addEventListener('keyup', () => {
    descriptionManuallyChanged = true
    document.getElementById('card_description').innerHTML = document.getElementById('id_description').value
  })
  document.getElementById('clear_form_btn').addEventListener('click', clearForm)
})

const createUrlPreview = async () => {
  const url = document.getElementById('id_url').value
  if(validUrl(url)){
    const data = await renderUrlPreview(url, '#previewDiv')
    if(!titleManuallyChanged && !descriptionManuallyChanged){
      document.getElementById('id_title').value = data.title
      document.getElementById('id_description').value = data.description
    }
  }
}

const typewatch_options = {
  callback: createUrlPreview,
  wait: 500,
  highlight: true,
  allowSubmit: false,
  captureLength: 4
}

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

const clearForm = () => {
  document.getElementById('add_form').reset()
  titleManuallyChanged = false
  descriptionManuallyChanged = false
  $('#previewDiv').html('')
}

//https://stackoverflow.com/questions/5717093/check-if-a-javascript-string-is-a-url
const validUrl = url => {
  var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
    '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
    '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
    '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
  return !!pattern.test(url);
}