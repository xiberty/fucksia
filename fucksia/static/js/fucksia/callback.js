function resCombi(data) {
    console.log(data.listgen);
    // alert("numero de combinaciones de materias: " + data.combinaciones);
    // alert("numero de horaios: " + data.horarios);
    var lists = data.listgen;
    $(".wrap .wrap_gen").remove()
    $(".wrap .div_res").remove()
    var wrap = $(".wrap");
    var divRes = document.createElement("div");
    divRes.innerHTML = "Horarios Generados: " + lists.length;
    divRes.setAttribute('class', 'div_res');
    wrap.append(divRes);
    var sectionM = document.createElement("section");
    sectionM.setAttribute("class", "wrap_gen");
    // lista de horarios combinados
    for (var i = 0; i < lists.length; i++) {
        // horarios
        var sectionH = document.createElement("section");
        var horario = lists[i];
        // cada item es un dia del horario
        for (var j = 0; j < horario.length; j++) {
            var article = document.createElement("article");
            article.setAttribute("class", "rowgen");
            var dia = horario[j];
            // cada item es una hora de clase
            for (var k = 0; k < dia.length; k++) {
                var div = document.createElement("div");
                div.setAttribute("class", "dia");
                hora = dia[k];
                if (hora.length > 1) {
                    div.setAttribute("class", "hora");
                };
                div.innerHTML = hora;
                article.appendChild(div);
            };
            sectionH.appendChild(article);
        };
        sectionM.appendChild(sectionH);
    };
    wrap.append(sectionM);
}

function put_horario (data) {
    var per = data.periodos;
    limpiar_materia(data.mat);
    console.log(per);
    var sw = false;
    for (var i = 0; i < per.length; i++) {
        if ($('#'+per[i].per)[0].innerHTML != '&nbsp;') {
            sw = false;
        } else{
            sw = true;
        };
    };
    if (sw) {
        for (var i = 0; i < per.length; i++) {
            var td = $('#'+per[i].per)[0];
            td.setAttribute('style', 'background: #2ECC71;');
            td.innerHTML = data.mat;
        };  
    } else {
        alert('CHOQUE!!!');
    };
}

function limpiar_materia (materia) {
    var per = $('.periodo');
    for (var i = 0; i < per.length; i++) {
        if (materia == per[i].innerHTML) {
            per[i].innerHTML = '&nbsp;'
            per[i].removeAttribute("style");
        };
    };
}