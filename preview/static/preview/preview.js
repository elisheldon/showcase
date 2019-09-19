const getUrlPreview = async url => {
  let csrftoken = Cookies.get('csrftoken');
  let response = await fetch(window.previewUrl,{
    method: 'post',
    body: JSON.stringify({'url': url}),
    headers: { "X-CSRFToken": csrftoken },
  })
  data = await response.json()
  console.log(data)
}