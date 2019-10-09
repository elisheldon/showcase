// posts a request with the input url to the preview endpoint, which returns meta info as JSON used to render url preview
const getUrlPreview = async url => {
  const csrftoken = Cookies.get('csrftoken')

  // if http or https protocol not provided, assume http
  if(url.substring(0,4) != 'http'){
    url = 'http://' + url
  }

  const response = await fetch(window.previewUrl,{
    method: 'post',
    body: JSON.stringify({'url': url}),
    headers: { "X-CSRFToken": csrftoken },
  })

  // server will return 400 error if link is unreachable; return null when that happens
  if(!response.ok){
    return null
  }
  const data = await response.json()

  // if we don't get a title back, return nothing
  if(!data.title){
    return null
  }

  if(data.title && data.title.length > 128){
    data.title = data.title.substring(0, 125) + '...'
  }

  if(data.description && data.description.length > 256){
    data.description = data.description.substring(0, 253) + '...'
  }

  return data
}