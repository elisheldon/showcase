// returns html of preview card using handlebars template defined in student_base.html
const renderCard = (context) => {
  const template = $('#hb_card').html()
  const templateScript = Handlebars.compile(template)
  const html = templateScript(context)
  return html
}

document.addEventListener('DOMContentLoaded', () => {
  const csrftoken = Cookies.get('csrftoken')
  // https://getbootstrap.com/docs/4.3/components/modal/
  $('#removeModal').on('show.bs.modal', function (event) {
    const button = $(event.relatedTarget) // Button that triggered the modal
    const itemTitle = button.data('item-title')
    const itemId = button.data('item-id')
    const modal = $(this)
    modal.find('#modal-title-item').html(itemTitle)
    modal.find('#modal-body-item').html('<b>' + itemTitle + '</b>')
    $('#removeButton').click( async () => {
      const response = await fetch(window.removeUrl,{
        method: 'post',
        body: JSON.stringify({'item_id': itemId}),
        headers: { "X-CSRFToken": csrftoken },
      })
      if(response.status == 204){
        modal.modal('hide')
        $('#card-' + itemId).remove()
      }
    })
  })
})