// posts a request with the input url to the preview endpoint, which returns meta info as JSON used to render url preview
const getUrlPreview = async url => {
  const csrftoken = Cookies.get('csrftoken');
  const response = await fetch(window.previewUrl,{
    method: 'post',
    body: JSON.stringify({'url': url}),
    headers: { "X-CSRFToken": csrftoken },
  })
  const data = await response.json()

  // if we get a title (indicating a working url) and no image, use default link image (commented out: try to get an image from thum.io)
  if(data.title && !data.image){
    if(url.substring(0,3) != 'http'){
      url = 'http://' + url
    }
    console.log('would be using thum.io for ' + url)
    data.image = '/static/student/default_images/link.svg'
    //data.image = '//image.thum.io/get/width/300/crop/600/' + url
  }

  return data
}