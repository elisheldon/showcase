document.addEventListener('DOMContentLoaded', () => {
  const csrftoken = Cookies.get('csrftoken')
  $('#changePublicButton').click( async () => {
    const response = await fetch(window.publicUrl,{
      method: 'post',
      body: JSON.stringify({'public': $('#changePublicButton').data('public')}),
      headers: { "X-CSRFToken": csrftoken },
    })
    if(response.status == 202){
      location.reload(); 
    }
  })
})