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
    if(data){
      document.getElementById('id_image').value = data.image
      document.getElementById('id_url').value = data.url // in case link shortener was resolved on server
      if(!titleManuallyChanged){
        document.getElementById('id_title').value = data.title
      }
      if(!descriptionManuallyChanged){
        document.getElementById('id_description').value = data.description
      }
      const html = renderCard(data)
      $('#previewDiv').html(html)
    }
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

// https://www.w3resource.com/javascript-exercises/javascript-regexp-exercise-9.php
const validUrl = url => {
  const regexp =  /^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$/;
  return regexp.test(url)
}