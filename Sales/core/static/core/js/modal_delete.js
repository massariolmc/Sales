(function(win,doc)
    {
        "use strict";       
        doc.addEventListener('DOMContentLoaded', function() {  
        
            var $del = doc.querySelectorAll('[data-js="link_delete"]')          
            var $link = doc.querySelector('[data-js="insert_link"]')                          
             
            var Modalelem = doc.querySelector('#modal_delete');
            var instance = M.Modal.init(Modalelem)                  
         
            function atribuirEvento(id){
                doc.getElementById(id).addEventListener("click", function(event){
                    event.preventDefault();                    
                    var $url = doc.querySelector('#'+id)                   
                    $link.innerHTML = '<a href="'+$url.getAttribute('href')+'" class="modal-close waves-effect green btn-flat" id="url_modal">Sim</a> <a class="modal-close waves-effect red btn-flat">Não</a>'                    
                    instance.open();
                })
            }
            for(var i=0; i < $del.length; i++){                
                atribuirEvento($del[i].id)
            }  

        });      
})(window, document);