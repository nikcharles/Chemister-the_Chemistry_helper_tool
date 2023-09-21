function getVars(){
    //global vars not working for some reason
    const r1 = document.getElementById("r1");
    const w1 = document.getElementById("w1");
    const r2 = document.getElementById("r2");
    const w2 = document.getElementById("w2");
    const p1 = document.getElementById("p1");
    const w3 = document.getElementById("w3");
    const ex = document.getElementById("ex");
    const cat = document.getElementById("cat"); //is now a paragraph <p>
    const selected = document.getElementById("selected"); //0 for none, 1 for 1st, 2 for 2nd, 3 for 3rd. 
    //If none selected, fetch all matching for other 2.  If one selected, fetch final matching and set cat,ex + enabled w1,w2,w3
    return r1, w1, r2, w2, p1, w3, ex, cat, selected;
}




function reset(){
    r1, w1, r2, w2, p1, w3, ex, cat, selected = getVars();
    selected.value = 0;
    r1.innerHTML = "<option> Select an option </option>";
    r1.disabled = false;
    w1.value = "";
    w1.disabled = true;
    r2.innerHTML = "<option> Select an option </option>";
    r2.disabled = false;
    w2.value = "";
    w2.disabled = true;
    p1.innerHTML = "<option> Select an option </option>";
    p1.disabled = false;
    w3.value = "";    
    w3.disabled = true;
    cat.innerHTML = "Catalyst";
    ex.value = "Extra information";

    var values = {
        boxNo: [],
        value: 0
    }
    $.ajax({
        type: "POST",
        url: "/update",
        data: JSON.stringify(values),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            //result = JSON.parse(result);
            for(word of result[0]){
            $("#r1").append("<option>" + word + "</option>");
            }
            for(word of result[1]){
            $("#r2").append("<option>" + word + "</option>");
            }
            for(word of result[2]){
            $("#p1").append("<option>" + word + "</option>");
            }
        } 
      });
}

function changeFirst(num){
    r1, w1, r2, w2, p1, w3, ex, cat, selected = getVars();
    if(num == 1){
        var val = r1.value;
        r1.disabled = true;
    }else if(num == 2){
        var val = r2.value;
        r2.disabled = true;
    }else if(num == 3){
        var val = p1.value;
        p1.disabled = true;
    }
    var values = {
        boxNo : [num,],
        value : val
    }
    $.ajax({
        type: "POST",
        url: "/update",
        data: JSON.stringify(values),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            // result = JSON.parse(result);
            if(num != 1){
                $("#r1").html("<option> Select an option </option>");
                for(word of result[0]){
                    $("#r1").append("<option>" + word + "</option>");
                }
            }
            if(num != 2){
                if(num == 1){a = result[0]} else {a = result[1]}
                $("#r2").html("<option> Select an option </option>");
                for(word of a){
                    $("#r2").append("<option>" + word + "</option>");
                }
            }
            if(num != 3){
                $("#p1").html("<option> Select an option </option>");
                for(word of result[1]){
                    
                    $("#p1").append("<option>" + word + "</option>");
                }
            }        
            $("#selected").val(num);
        } 
      });
    
}

function changeSecond(num1, num2){
    r1, w1, r2, w2, p1, w3, ex, cat, selected = getVars();
    var val1, val2;
    r1.disabled = true;
    r2.disabled = true;
    p1.disabled = true;
    if(num1 == 1){
        val1 = r1.value;
        if(num2 == 2){
            val2 = r2.value;
        }
        else if(num2 == 3){
            val2 = p1.value;
        }

    }
    else if(num1 == 2){
        val1 = r2.value;
        val2 = p1.value;
    }
    var values = {
        boxNo: [num1, num2],
        value : [val1, val2],
    }

    $.ajax({
        type: "POST",
        url: "/update",
        data: JSON.stringify(values),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
        //   result = JSON.parse(result);
            if(num1 != 1 && num2 != 1){
                $("#r1").val(result[0]);
            }
            else if(num1 != 2 && num2 != 2){
                $("#r2").val(result[0]);
            }
            else if(num1 != 3 && num2 != 3){
                $("#p1").val(result[0]);
            }
            $("#ex").val(result[1]);
            $("#cat").html(result[2]);
            $("#w1").val(result[3][0]);
            $("#w2").val(result[3][1]);
            $("#w3").val(result[3][2]);
        } 
      });

}

$(document).ready(() => { 
    reset();
    $("#r1").change(() => {
        const selected = parseInt(document.getElementById("selected").value);
        if(selected == 0 || selected == 1)
            changeFirst(1);
        else
            changeSecond(1, selected);
    })

    $("#r2").change(() => {
        const selected = parseInt(document.getElementById("selected").value);
        if(selected == 0 || selected == 2)
            changeFirst(2);
        else{
            if(selected == 1)
                changeSecond(selected, 2);
            else
                changeSecond(2, selected);
        }
    })

    $("#p1").change(() => {
        const selected = parseInt(document.getElementById("selected").value);
        if(selected == 0 || selected == 3)
            changeFirst(3);
        else
            changeSecond(selected, 3)
    })

})






// generic ajax format
// $.ajax({
//     type: "POST",
//     url: "/update",
//     data: JSON.stringify(values),
//     contentType: "application/json",
//     dataType: 'json',
//     success: function(result) {
//       JSON.parse(result);
//     } 
//   });

