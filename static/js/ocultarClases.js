function verMusculos(id){
    $.ajax({
        data : {'id' : id},
        url : '/rutinas/obtener_cantidad_musculos_ajax/', //El id que estoy guardando en data se va a enviar en esa url
        type : 'get',
        success : function(musculos){
            Object.keys(musculos).forEach(function(key) {
                console.log(key, musculos[key])
                labelsMusculos.push(key);
                dataMusculos.push(parseInt(musculos[key]));
              })
            
        }

    });              
}