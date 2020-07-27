$(document).ready(function () {
    'use strict'; 
    var url = document.querySelector("table").getAttribute("data-lang");          
    $('[data-js="dataTables"]').DataTable({    
      "paging": true,
      "lengthChange": true,
      "searching": true,
      "ordering": true,
      "info": true,
      "autoWidth": false,
      "responsive": true,
      "bJQueryUI": true,
      "oLanguage": {
        "sUrl":          url,
    }

    });
});
