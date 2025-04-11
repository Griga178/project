let mDateFormat = function(date_string){
  let arr = date_string.split('-')
  return arr[2]+'.'+arr[1]+'.'+arr[0]
}

let fill_common_info = function(responce_objest) {
  inp_end_date.value = responce_objest.end_date
  inp_start_date.value = responce_objest.start_date
  common_info_last_update_date.innerHTML = mDateFormat(responce_objest.last_update_date)
  common_info_last_update_date_2.innerHTML = mDateFormat(responce_objest.last_update_date)
  common_info_first_contract_date.innerHTML = mDateFormat(responce_objest.first_contract_date)
  common_info_last_contract_date.innerHTML = mDateFormat(responce_objest.last_contract_date)
  common_info_contract_amount.innerHTML = responce_objest.contract_amount + ' шт'
  common_info_empty_contract_amount.innerHTML = responce_objest.empty_contract_amount + ' шт'
  common_info_empty_contract_amount_2.innerHTML = responce_objest.empty_contract_amount
  common_info_product_amount.innerHTML = responce_objest.product_amount + ' шт'

  if (responce_objest.empty_contract_amount > 0)
  btn_parse_products_start.removeAttribute('disabled')
}

$.ajax({
  url: '/get_sum_info',
  type: 'get',
  before: function() {  },
  success: function (response){
    console.log(response)
    ci_message_small.hidden = true
    fill_common_info(response)
  }
})


if (app_active === 1){
  console.log('parse_numbers')
  change_number_parse_menu_start()
}
else if (app_active === 11){
  console.log('stop_parse_numbers')
  change_number_parse_menu_stop()
}
else if (app_active === 2)
console.log('parse_products')
else if (app_active === 3)
console.log('update_contracts')
else
console.log('have not start - zero')

setInterval(
  function(){
    if (app_active === 1){
      console.log('parse_numbers')

      $.ajax({
        url: '/check_info',
        type: 'get',
        success: function (response){
          progress_bar_parse_number.style = `width:${response.parse_progress}%`
          progressbar_date.innerHTML = mDateFormat(response.parse_date_from)
          console.log(response)
          }
      })}
    else if (app_active === 11){
      console.log('stop_parse_numbers')
        $.ajax({
        url: '/check_info',
        type: 'get',
        success: function (response){
          progress_bar_parse_number.style = `width:${response.parse_progress}%`
          }
      })}
    else if (app_active === 2)
    console.log('parse_products')
    else if (app_active === 3)
    console.log('update_contracts')
    else
    console.log('have not start - zero')

},
   5000);
