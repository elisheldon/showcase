// posts a request with the input url to the preview endpoint, which returns meta info as JSON used to render url preview
const getUrlPreview = async url => {
  const csrftoken = Cookies.get('csrftoken');
  const response = await fetch(window.previewUrl,{
    method: 'post',
    body: JSON.stringify({'url': url}),
    headers: { "X-CSRFToken": csrftoken },
  })
  const data = await response.json()
  // if we get a title and no image, try to get an image from thum.io
  if(data.title && !data.image){
    if(url.substring(0,3) != 'http'){
      url = 'http://' + url
    }
    console.log('using thum.io')
    data.image = '//image.thum.io/get/width/300/crop/600/' + url
  }
  return data
}

// fills input div with input url's preview, using handlebars template defined in student_base.html
const renderPreview = async (url, div_id) => {
  if(div_id[0] != '#'){
    div_id = '#'+div_id
  }
  const template = $('#hb_url_preview').html()
  const templateScript = Handlebars.compile(template)
  const context = await getUrlPreview(url)
  const html = templateScript(context)
  $(div_id).html(html)
}