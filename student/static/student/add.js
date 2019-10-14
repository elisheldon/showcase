let titleManuallyChanged = false
let descriptionManuallyChanged = false
const maxPhotoSize = 5 //MB
const maxFileSize = 2 //MB

document.addEventListener('DOMContentLoaded', () => {
  // hide form elements not related to first item type immediately
  renderSubItemOptions(0)
  $('#photoSizeAlert').hide()
  $('#fileSizeAlert').hide()

  // add event to hide form elements not related to selected item type over 300ms
  document.getElementById('id_sub_item_type').addEventListener('change', () => {
    clearForm()
    renderSubItemOptions(300)
  })

  // add event to preview url after user stops typing for 500ms
  $('#id_url').typeWatch( typewatch_options )

  // add event to check photo uploads
  document.getElementById('id_photos').addEventListener('input', () => {
    renderGalleryPreview()
    checkSubmitReady()
  })

  // add event to check photo uploads
  document.getElementById('id_file').addEventListener('input', () => {
    renderFilePreview()
    checkSubmitReady()
  })

  // add event to update card preview's title text when user changes title in form
  document.getElementById('id_title').addEventListener('keyup', () => {
    titleManuallyChanged = document.getElementById('id_title').value ? true : false
    // handles case where user tabs out of url field into title field
    if(document.getElementById('card_title')){
      document.getElementById('card_title').innerHTML = document.getElementById('id_title').value
    }
    checkSubmitReady()
  })
  
  // add event to update card preview's description text when user changes description in form
  document.getElementById('id_description').addEventListener('keyup', () => {
    descriptionManuallyChanged = document.getElementById('id_description').value ? true : false
    if(document.getElementById('card_description')){
      document.getElementById('card_description').innerHTML = document.getElementById('id_description').value
    }
  })
  
  // add event to clear form when user clicks clear button
  document.getElementById('clear_form_btn').addEventListener('click', clearForm)

  // add event to hide alerts when user closes then
  $('#hidePhotoSizeAlert').click(() => $('#photoSizeAlert').fadeOut(250))
  $('#hideFileSizeAlert').click(() => $('#fileSizeAlert').fadeOut(250))
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
      else{
        data.title = document.getElementById('id_title').value
      }
      if(!descriptionManuallyChanged){
        document.getElementById('id_description').value = data.description
      }
      else{
        data.description = document.getElementById('id_description').value
      }
      data.linkType = true
      prerenderCard(data)
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
  checkSubmitReady()
}

const renderGalleryPreview = () => {
  const data = {title: document.getElementById('id_title').value, description: document.getElementById('id_description').value}
  const input = document.getElementById('id_photos')
  if (input.files && input.files[0]) {
    data.image = URL.createObjectURL(input.files[0])
  }
  if (input.files && input.files[0] && !titleManuallyChanged) {
    document.getElementById('id_title').value = input.files[0].name.replace(/\.[^/.]+$/, "") // removes file extension from filename
  }
  data.galleryType = true
  prerenderCard(data)
}

const renderFilePreview = () => {
  const data = {description: document.getElementById('id_description').value}
  const input = document.getElementById('id_file')
  if (input.files && input.files[0] && !titleManuallyChanged) {
    document.getElementById('id_title').value = input.files[0].name.replace(/\.[^/.]+$/, "") // removes file extension from filename
  }
  data.title = document.getElementById('id_title').value
  data.fileType = true
  prerenderCard(data)
}

const prerenderCard = data => {
  const today = new Date // to render footer on preview card
  data.date = today.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
  const html = renderCard(data)
  $('#previewDiv').html(html)
}

const typewatch_options = {
  callback: loadUrlPreview,
  wait: 500,
  highlight: true,
  allowSubmit: false,
  captureLength: 4
}

// hide and show relevant form inputs based on item type
const renderSubItemOptions = duration => {
  const sub_item_type = document.getElementById('id_sub_item_type').value
  document.getElementById('id_url').removeEventListener('click', createGooglePicker)
  switch(sub_item_type){
    case 'link':
      $('#div_id_photos, #div_id_file').fadeOut(duration).promise().done(function(){
        $('#div_id_url').fadeIn(duration)
      })
      break
    case 'gallery':
      $('#div_id_url, #div_id_file').fadeOut(duration).promise().done(function(){
        $('#div_id_photos').fadeIn(duration)
      })
      break
    case 'document':
      $('#div_id_url, #div_id_photos').fadeOut(duration).promise().done(function(){
        $('#div_id_file').fadeIn(duration)
      })
      break
    case 'drive':
      $('#div_id_photos, #div_id_file').fadeOut(duration).promise().done(function(){
        $('#div_id_url').fadeIn(duration)
      })
      getGoogleOAuthToken()
      break
  }
}

// checks to see if the form is ready for submission, enabling or disabling submit button
const checkSubmitReady = () => {
  let ready = true
  if(!document.getElementById('id_title').value){
    ready = false
  }
  const sub_item_type = document.getElementById('id_sub_item_type').value
  switch(sub_item_type){
    case 'link':
      if(!validUrl(document.getElementById('id_url').value)){
        ready = false
      }
      break
    case 'gallery':
      if(document.getElementById('id_photos').files.length == 0){
        ready = false
      }
      else{
        files = document.getElementById('id_photos').files
        for (let i = 0; i < files.length; i++){
          if(files[i].size>1024*1024*maxPhotoSize){
            $('#photoSizeAlert').show()
            document.getElementById('id_photos').value = ''
            if(!titleManuallyChanged){
              document.getElementById('id_title').value = ''
            }
          }
        }
      }
      break
    case 'document':
      if(document.getElementById('id_file').files.length == 0){
        ready = false
      }
      else{
        file = document.getElementById('id_file').files[0]
        if(file.size>1024*1024*maxFileSize){
          $('#fileSizeAlert').show()
          document.getElementById('id_file').value = ''
          if(!titleManuallyChanged){
            document.getElementById('id_title').value = ''
          }
        }
      }
      break
  }
  document.getElementById('submit_form_btn').disabled = !ready
}

// resets form, manuallychanged booleans and preview card
const clearForm = () => {
  const subitem = document.getElementById('id_sub_item_type').value
  document.getElementById('add_form').reset()
  document.getElementById('id_sub_item_type').value = subitem
  titleManuallyChanged = false
  descriptionManuallyChanged = false
  $('#previewDiv').html('')
  checkSubmitReady()
}

// https://www.w3resource.com/javascript-exercises/javascript-regexp-exercise-9.php
const validUrl = url => {
  const regexp =  /^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$/;
  return regexp.test(url)
}

const googleApiKey = 'AIzaSyCP-EcWv3seHzCc6g862LMtSk3cdqN5yFM'
const googlePickerScope = 'https://www.googleapis.com/auth/drive.metadata.readonly'
// const googlePickerScope = 'https://www.googleapis.com/auth/drive.file'
let googlePickerApiLoaded = 'false'
let googleOAuthToken

function onGoogleApiLoad() {
  //gapi.load('auth2', onGoogleAuthApiLoad)
  gapi.load('picker', onGooglePickerApiLoad)
}

/*function onGoogleAuthApiLoad() {
  const googleAuthBtn = document.getElementById('googleAuthBtn')
  googleAuthBtn.disabled = false
  googleAuthBtn.addEventListener('click', function() {
    gapi.auth2.init({ client_id: googleClientId }).then(function(googleAuth) {
      googleAuth.signIn({ scope: googlePickerScope }).then(function(result) {
        handleGoogleAuthResult(result.getAuthResponse())
      })
    })
  })
}*/

function onGooglePickerApiLoad() {
  googlePickerApiLoaded = true
}


function createGooglePicker() {
  if (googlePickerApiLoaded && window.googleOAuthToken) {
    const googlePicker = new google.picker.PickerBuilder().
        addView(google.picker.ViewId.DOCS).
        setOAuthToken(window.googleOAuthToken).
        setDeveloperKey(googleApiKey).
        setCallback(googlePickerCallback).
        build()
    googlePicker.setVisible(true)
  }
}

function googlePickerCallback(data) {
  let url = '';
  if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
    const doc = data[google.picker.Response.DOCUMENTS][0]
    url = doc[google.picker.Document.URL]
  }
  document.getElementById('id_url').value = url
  document.getElementById('id_url').addEventListener('click', createGooglePicker)
  loadUrlPreview()
}

const getGoogleOAuthToken = async () => {
  // check if we have a valid oauth token for the required scope; if not, get it from google
  response = await fetch('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=' + window.googleOAuthToken)
  data = await response.json()
  if(!data.error && data.scope.includes(googlePickerScope)){
    createGooglePicker()
  }
  else{
    window.open(window.getGoogleScopesUrl + '?scope=' + googlePickerScope, '_blank', 'location=yes,height=570,width=520,scrollbars=yes,status=yes')
  }
}

window.launchGooglePicker = token => {
  window.googleOAuthToken = token
  createGooglePicker()
}