let start_parse_number = function() {
  // console.log(response)
  app_active = 1
  change_number_parse_menu_start()
    $.ajax({
      url: '/start_parse_numbers',
      data: {
        "date_from": inp_start_date.value,
        "date_to": inp_end_date.value,
      },
      type: 'post',
      success: function (response){
        app_active = response.app_status
        change_number_parse_menu_stop()
        fill_common_info(response)
      },
      error: function() {
        alert("error")
      }
    })
}
let stop_parse_number = function() {
  $.ajax({
    url: '/stop_parse_numbers',
    type: 'get',
    success: function (response){
      console.log(response)
      app_active = response.app_status
      progress_bar_parse_number.style = `width:${response.parse_progress}%`
      change_number_parse_menu_stop()
    }
  })
}
let refresh_parse_number = function() {
  $.ajax({
    url: '/refresh_parse_numbers',
    type: 'get',
    success: function (response){
      console.log(response)
      app_active = response.app_status
      progress_bar_parse_number.style = `width:${response.parse_progress}%`
      change_number_parse_menu_refresh()
    }
  })
}

let change_number_parse_menu_start = function () {
  fldst_contract_dates.disabled = true
  btn_parse_number_start.hidden = true
  div_number_progres.hidden = false
  btn_parse_number_stop.hidden = false
}

let change_number_parse_menu_stop = function () {
  btn_parse_number_start.hidden = true
  btn_parse_number_stop.hidden = true
  btn_parse_number_refresh.hidden = false
}

let change_number_parse_menu_refresh = function () {
  fldst_contract_dates.removeAttribute('disabled')
  btn_parse_number_start.hidden = false
  div_number_progres.hidden = true
  btn_parse_number_stop.hidden = true
  btn_parse_number_refresh.hidden = true
}

btn_parse_number_start.onclick = function () {
  start_parse_number()
}
btn_parse_number_stop.onclick = function () {
  stop_parse_number()
}
btn_parse_number_refresh.onclick = function () {
  refresh_parse_number()
}
