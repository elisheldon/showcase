document.addEventListener('DOMContentLoaded', () => {
  toggleAge() // hides age when a teacher tries to register and gets an error
  document.getElementById('id_register-user_type').addEventListener('change', () => {
    toggleAge()
  })
})

const toggleAge = () =>{
  user_type = document.getElementById('id_register-user_type').value
  if(user_type=='student'){
    $('#div_id_register-age').show()
    document.getElementById('id_register-age').required = true
  }
  else{
    $('#div_id_register-age').hide()
    document.getElementById('id_register-age').required = false
  }
}