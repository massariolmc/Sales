(function(doc,win){
    doc.addEventListener("DOMContentLoaded", function() {
        $search = doc.querySelector('[data-js="search"]');
        $lines = doc.querySelector('[data-js="select_lines"]');
        $table = doc.querySelector('#table_list');        
        var $modal_link = doc.querySelector('[data-js="modal_link_delete"]');
        var page = 1;    
        
        var $button_checkbox = doc.querySelector('[data-js="click_checkbox"]'); 
        var $check_all = doc.querySelector('[data-js="check_all"]'); 

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
        
        function handleClickCheckBox(e){
            e.preventDefault();               
            var $checkbox = doc.querySelectorAll('input[name="check_id"]');
            var ac = [];
            var marc = false;
            var $modal_checkbox = doc.querySelector('[data-js="modal_checkbox"]')
        
            for (var i=0; i < $checkbox.length; i++){
                if($checkbox[i].checked === true){
                    marc = true;
                    ac.push($checkbox[i].value);
                    console.log('clicado',$checkbox[i].value);
                    console.log('acumulador', ac);
    
                }
                else
                    console.log('nada clicado');
                    
            }
            if (marc === false){
                $('[data-js="modal_checkbox"]').modal();
            }
    
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

        $button_checkbox.addEventListener('click',handleClickCheckBox,false);
        $check_all.addEventListener('click',handleClickCheckBoxAll,false); 
        
    });//DOMContentLoaded

})(document,window);