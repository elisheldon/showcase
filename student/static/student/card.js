// returns html of preview card using handlebars template defined in student_base.html
const renderCard = (context) => {
  const template = $('#hb_card').html()
  const templateScript = Handlebars.compile(template)
  const html = templateScript(context)
  return html
}

// swaps broken link image for link icon
const linkImgError = (image) => {
  image.outerHTML = "<i class='fas fa-link item-icon'></i>"
  return true
}

document.addEventListener('DOMContentLoaded', () => {
  const csrftoken = Cookies.get('csrftoken')
  // https://getbootstrap.com/docs/4.3/components/modal/
  $(document).on('show.bs.modal', '#removeModal', function (event) {
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
      if(response.status == 202){
        modal.modal('hide')
        $('#card-' + itemId).remove()
        $('#removeButton').unbind() // unregister the click event so future deletions don't repeat old post requests
      }
    })
  })

  $('.pinCard').click( async (event) => {
    const icon = $(event.target) // Icon that triggered the modal
    const item_id = icon.data('item-id')
    const response = await fetch(window.pinUrl, {
      method: 'post',
      body: JSON.stringify({'item_id': item_id}),
      headers: {"X-CSRFTOKEN": csrftoken},
    })
    if(response.status == 202){
      location.reload()
    }
  })

  $(document).on('show.bs.modal', '#editModal', function (event) {
    const button = $(event.relatedTarget) // Button that triggered the modal
    const itemTitle = button.data('item-title')
    const itemDescription = button.data('item-description')
    const itemId = button.data('item-id')
    document.getElementById('editItemTitle').value = itemTitle
    document.getElementById('editItemDescription').value = itemDescription
    const modal = $(this)
    modal.find('#edit-modal-title-item').html(itemTitle)
    $('#saveButton').click( async () => {
      const newItemTitle = document.getElementById('editItemTitle').value
      const newItemDescription = document.getElementById('editItemDescription').value
      const response = await fetch(window.editUrl,{
        method: 'post',
        body: JSON.stringify({'item_id': itemId, 'item_title': newItemTitle, 'item_description': newItemDescription}),
        headers: { "X-CSRFToken": csrftoken },
      })
      if(response.status == 202){
        location.reload()
      }
      else{
        modal.modal('hide')
      }
    })
  })
})