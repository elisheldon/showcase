let titleManuallyChanged = false
let descriptionManuallyChanged = false

document.addEventListener('DOMContentLoaded', () => {
  // hide form elements not related to first item type immediately
  renderItemOptions(0)

  // add event to hide form elements not related to selected item type over 300ms
  document.getElementById('id_item_type').addEventListener('change', () => renderItemOptions(300))

  // add event to preview url after user stops typing for 500ms
  $('#id_url').typeWatch( typewatch_options )

  // add event to update card preview's title text when user changes title in form
  document.getElementById('id_title').addEventListener('keyup', () => {
    titleManuallyChanged = document.getElementById('id_title').value ? true : false
    // handles case where user tabs out of url field into title field
    if(document.getElementById('card_title')){
      document.getElementById('card_title').innerHTML = document.getElementById('id_title').value
    }
  })
  
  // add event to update card preview's description text when user changes description in form
  document.getElementById('id_description').addEventListener('keyup', () => {
    descriptionManuallyChanged = document.getElementById('id_description').value ? true : false
    document.getElementById('card_description').innerHTML = document.getElementById('id_description').value
  })
  
  // add event to clear form when user clicks clear button
  document.getElementById('clear_form_btn').addEventListener('click', clearForm)
})

// submit url to server to pull title, description and image link into form via /preview routes
const loadUrlPreview = async () => {
  const url = document.getElementById('id_url').value
  if(validUrl(url)){
    const data = await getUrlPreview(url)
    document.getElementById('id_image').value = data.image
    if(!titleManuallyChanged){
      document.getElementById('id_title').value = data.title
    }
    if(!descriptionManuallyChanged){
      document.getElementById('id_description').value = data.description
    }
    const html = renderCard(data)
    $('#previewDiv').html(html)
  }
  else{
    $('#previewDiv').html('')
    if(!titleManuallyChanged ){
      document.getElementById('id_title').value = ''
    }
    if(!descriptionManuallyChanged){
      document.getElementById('id_description').value = ''   
    }
  }
}

const typewatch_options = {
  callback: loadUrlPreview,
  wait: 500,
  highlight: true,
  allowSubmit: false,
  captureLength: 4
}

// hide and show relevant form inputs based on item type
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

// resets form, manuallychanged booleans and preview card
const clearForm = () => {
  document.getElementById('add_form').reset()
  titleManuallyChanged = false
  descriptionManuallyChanged = false
  $('#previewDiv').html('')
}

// https://stackoverflow.com/questions/5717093/check-if-a-javascript-string-is-a-url
const validUrl = url => {
  var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
    '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
    '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
    '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
  return !!pattern.test(url);
}