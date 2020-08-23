$(function () {     
    $('#id_birthday').inputmask('dd/mm/yyyy', { 'placeholder': 'dd/mm/yyyy' })    
    $('#id_drivers_license_validate').inputmask('dd/mm/yyyy', { 'placeholder': 'dd/mm/yyyy' })    
    $('#id_phone_1').inputmask(['(999) 9999-9999','(999) 99999-9999'], { 'placeholder': '(___) ____-____)' })    
    $('#id_phone_2').inputmask(['(999) 9999-9999','(999) 99999-9999'], { 'placeholder': '(___) ____-____)' })
  })