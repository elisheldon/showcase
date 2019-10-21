document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('hint_id_pf_public').innerHTML += '<a href="' + window.publicUrl + '">' + window.publicUrl
  if (document.getElementById('current_school')){
    document.getElementById('div_id_code').setAttribute('style', 'margin-bottom: 0px !important;')
  }
})