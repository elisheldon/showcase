document.addEventListener('DOMContentLoaded', () => {
  renderItemOptions(0)
  document.getElementById('id_item_type').addEventListener('change', () => renderItemOptions(300))
  document.getElementById('id_url').addEventListener('keyup', () => {
    url = document.getElementById('id_url').value
    if(validUrl(url)){
      renderPreview(url, '#previewDiv')
    }
  })
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