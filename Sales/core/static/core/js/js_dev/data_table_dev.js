(function(doc,win){
    doc.addEventListener("DOMContentLoaded", function() {
        'use strict';
        var $search = doc.querySelector('[data-js="search"]');
        var $lines = doc.querySelector('[data-js="select_lines"]');
        var $table = doc.querySelector('#table_list');        
        var $modal_link = doc.querySelector('[data-js="modal_link_delete"]');
        var page = 1;    
        
        var $button_checkbox = doc.querySelector('[data-js="click_checkbox"]'); 
        var $check_all = doc.querySelector('[data-js="check_all"]');         
        var $modal_link_delete_all = doc.querySelector('[data-js="modal_link_delete_all"]');
        

        function handleSearch(e){        
            $.ajax({
                type: "GET",                
                url: $table.getAttribute("data-url"),
                data: {'q': $search.value, 'l':$lines.value, 'page': page },
                dataType: "json",
                beforeSend : function(){
                    
                },
                success: function(data){                                
                    $table.innerHTML = data.html_signup_list;                    
                    on('[data-js="click_checkbox"]', 'click', getCheckBoxSelected);
                    on('[data-js="check_all"]', 'click', handleClickCheckBoxAll);
                    on('.click_page', 'click', handlePage);  
                    handleClickDelete();
                },
                failure: function(data){
                    
                },
            });                         
        }        

        function handlePage(e) {        
            e.preventDefault();
            page = e.target.href.slice(35);
            handleSearch();                
        };

        function handleClickDelete(){
            var elementoAtual = doc.querySelectorAll('[data-js="link_delete"');
            Array.prototype.slice.call(elementoAtual).forEach(function(pegaElementoAtual){
                pegaElementoAtual.addEventListener('click', function(e){
                        e.preventDefault();                        
                        $modal_link.setAttribute('href',e.target.href);
                        $('[data-js="modal_delete"]').modal();
                });                             
            }); 
        }   

        function on(element, event, callback){
            doc.querySelector(element).addEventListener(event,callback,false);
        }
        
        function getCheckBox(checkbox){
            var ac = [];
            for (var i=0; i < checkbox.length; i++){
                if(checkbox[i].checked === true){                    
                    ac.push(checkbox[i].value);
                    console.log('clicado',checkbox[i].value);
                    console.log('acumulador', ac);                 
                }                  
            }
            return ac;
        }

        function getCheckBoxSelected(e){
            e.preventDefault();               
            var $checkbox = doc.querySelectorAll('input[name="check_id"]');
            var ac = [];                       

            ac = getCheckBox($checkbox)

            if (ac.length == 0){
                $('[data-js="modal_checkbox"]').modal();
            }
            else{
                $('[data-js="modal_delete_all"]').modal();
            }
        }
        function handleClickCheckBox(e){
            e.preventDefault();
            var $checkbox = doc.querySelectorAll('input[name="check_id"]');
            var ac = [];                      
            ac = getCheckBox($checkbox)
            ac = JSON.stringify(ac);
            console.log("valor do ac",ac)
            var url = $button_checkbox.getAttribute('data-url');

            $.ajax({
                type: "GET",                
                url: url,
                data: {'del': ac },
                dataType: "json",
                beforeSend : function(){
                    
                },
                success: function(data){                                         
                    document.location.reload(true);//Recarrega a página atual        
                },
                failure: function(data){
                    
                },
            });
        }
    
        function handleClickCheckBoxAll(e){        
            var $checkbox = doc.querySelectorAll('input[name="check_id"]');
            if (e.target.checked === true){
                mark_or_unmark(true)
            }
            else{
                mark_or_unmark(false)
            }
            function mark_or_unmark(check){
                for (var i=0; i < $checkbox.length; i++){
                    $checkbox[i].checked = check;            
                }
            }
        }        
        
        $search.addEventListener('input', handleSearch,false);
        $lines.addEventListener('change', handleSearch,false);
        on('.click_page', 'click', handlePage);
        handleClickDelete();                                    
        on('[data-js="click_checkbox"]', 'click', getCheckBoxSelected);
        on('[data-js="check_all"]', 'click', handleClickCheckBoxAll);
        $modal_link_delete_all.addEventListener('click',handleClickCheckBox,false); 

    });//DOMContentLoaded

})(document,window);