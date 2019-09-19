const getUrlPreview = async url => {
  const csrftoken = Cookies.get('csrftoken');
  const response = await fetch(window.previewUrl,{
    method: 'post',
    body: JSON.stringify({'url': url}),
    headers: { "X-CSRFToken": csrftoken },
  })
  data = await response.json()
  return data
}

const renderPreview = async (url, div_id) => {
  const template = $('#hb_url_preview').html()
  const templateScript = Handlebars.compile(template)
  const context = await getUrlPreview(url)
  //const context = {"title" : "Google", "description": "Search the world's information, including webpages…to help you find exactly what you're looking for.", "image": null}
  const html = templateScript(context)
  $('#'+div_id).html(html)
}