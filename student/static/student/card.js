// returns html of preview card using handlebars template defined in student_base.html
const renderCard = (context) => {
  const template = $('#hb_card').html()
  const templateScript = Handlebars.compile(template)
  const html = templateScript(context)
  return html
}