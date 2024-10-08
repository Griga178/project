let start_parse_products = function(){
  $.ajax({
    url: '/start_parse_products',
    type: 'get',
    before: function() {  },
    success: function (response){
      console.log(response)
      
    }
  })
}
btn_parse_products_start.onclick = function () {
  start_parse_products()
}
